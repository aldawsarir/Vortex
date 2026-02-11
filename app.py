import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, Response, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from io import BytesIO

from models import db, User, Upload, QuizResult, DailyChallenge, QuizBattle, BattleParticipant, Review, PuzzleGame
from utils.preprocessing import preprocess_text
from utils.summarizer import summarize_text, extract_keywords
from utils.quiz import generate_quiz
from utils.visualize import create_mindmap
from utils.visualization import create_bar_chart, create_pie_chart, analyze_quiz_performance
from utils.analytics import calculate_user_stats, generate_performance_report
from utils.ocr import extract_text_from_image
from translations import get_translation

# ================= Configuration =================
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx'}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
TEMPLATES_FOLDER = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, static_folder=STATIC_FOLDER, template_folder=TEMPLATES_FOLDER)
app.secret_key = "vortex-secret-key-2026"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vortex.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create folders
for folder in [UPLOAD_FOLDER, os.path.join(STATIC_FOLDER, 'images')]:
    os.makedirs(folder, exist_ok=True)

# Create database tables
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ================= Language Support =================
@app.before_request
def set_language():
    """Set language from session or default to English"""
    if 'language' not in session:
        session['language'] = 'en'

@app.route('/change-language/<lang>')
def change_language(lang):
    """Change language"""
    if lang in ['en', 'ar']:
        session['language'] = lang
    return redirect(request.referrer or url_for('home'))

@app.context_processor
def inject_translation():
    """Make translation function available in templates"""
    lang = session.get('language', 'en')
    def t(key):
        return get_translation(lang, key)
    return dict(t=t, current_lang=lang)

# ================= Helper Functions =================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ================= Authentication Routes =================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# ================= Main Routes =================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user_uploads = Upload.query.filter_by(user_id=current_user.id).order_by(Upload.uploaded_at.desc()).all()
    user_quizzes = QuizResult.query.filter_by(user_id=current_user.id).order_by(QuizResult.completed_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', uploads=user_uploads, quizzes=user_quizzes)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/summarize', methods=['POST'])
@login_required
def summarize():
    text = ""
    file = request.files.get('file')
    filename_to_save = 'Text Input'
    
    # قراءة النص من الـ form
    form_text = request.form.get('text', '').strip()
    if form_text:
        text = form_text
        print(f"📝 Text from form: {len(text)} chars")

    # قراءة الملف
    if file and file.filename:
        filename = secure_filename(file.filename)
        filename_to_save = filename
        
        if not allowed_file(filename):
            flash("Invalid file type. Allowed: PDF, DOCX, PPTX", 'danger')
            return redirect(url_for('home'))
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        ext = filename.rsplit('.', 1)[1].lower()

        print(f"📁 File uploaded: {filename}")

        try:
            file_text = ""
            
            if ext == 'pdf':
                import PyPDF2
                with open(filepath, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    pages_to_read = min(10, len(reader.pages))
                    file_text = "\n".join(
                        page.extract_text() or "" 
                        for page in reader.pages[:pages_to_read]
                    )
                    file_text = file_text[:5000]
                print(f"✅ PDF extracted: {len(file_text)} chars (first {pages_to_read} pages)")
            
            elif ext == 'docx':
                import docx
                doc = docx.Document(filepath)
                paragraphs = [p.text.strip() for p in doc.paragraphs[:50] if p.text.strip()]
                file_text = "\n".join(paragraphs)
                file_text = file_text[:5000]
                print(f"✅ DOCX extracted: {len(file_text)} chars")
            
            elif ext == 'pptx':
                from pptx import Presentation
                prs = Presentation(filepath)
                slides_to_read = min(5, len(prs.slides))
                extracted_text = []
                
                for slide in prs.slides[:slides_to_read]:
                    for shape in slide.shapes:
                        if hasattr(shape, "text") and shape.text.strip():
                            text_content = shape.text.strip()
                            if len(text_content) <= 200:
                                if hasattr(shape, 'text_frame') and shape.text_frame.paragraphs:
                                    if len(shape.text_frame.paragraphs) == 1:
                                        extracted_text.append(text_content)
                                    else:
                                        bullets = [p.text.strip() for p in shape.text_frame.paragraphs[:3] if p.text.strip()]
                                        extracted_text.extend(bullets)
                
                file_text = "\n".join(extracted_text)
                file_text = file_text[:5000]
                print(f"✅ PPTX extracted: {len(file_text)} chars (first {slides_to_read} slides)")
            
            if file_text:
                text = file_text
                
        except Exception as e:
            print(f"❌ Error reading file: {str(e)}")
            import traceback
            traceback.print_exc()
            flash(f"Error reading file: {str(e)}", 'danger')
            return redirect(url_for('home'))
    
    if not text or len(text.strip()) < 20:
        print("❌ No text or text too short")
        flash("Please provide text or upload a file with sufficient content", 'warning')
        return redirect(url_for('home'))

    if len(text) > 5000:
        text = text[:5000]
        flash("Text was truncated to 5000 characters for better performance", 'info')

    print(f"📊 Final text length: {len(text)} chars")

    try:
        cleaned_text = preprocess_text(text)
        print(f"✅ Cleaned text: {len(cleaned_text)} chars")
        
        if len(cleaned_text) < 50:
            print("❌ Text too short after cleaning")
            flash("Text is too short. Please provide more content.", 'warning')
            return redirect(url_for('home'))
        
        summary = summarize_text(cleaned_text)
        print(f"✅ Summary: {len(summary)} chars")
        
        if not summary or len(summary.strip()) < 10:
            print("❌ Summary too short")
            flash("Could not generate summary.", 'warning')
            return redirect(url_for('home'))
        
        quiz = generate_quiz(summary)
        print(f"✅ Quiz: {len(quiz)} questions")
        
        if not quiz or len(quiz) == 0:
            print("❌ No quiz generated")
            flash("Could not generate quiz.", 'warning')
            return redirect(url_for('home'))
        
        upload = Upload(
            filename=filename_to_save,
            summary=summary,
            user_id=current_user.id
        )
        db.session.add(upload)
        db.session.commit()
        
        session['summary'] = summary
        session['quiz'] = quiz
        session['score'] = 0

        try:
            words = summary.split()
            important_words = [
                word.strip('.,;:!?"\'') 
                for word in words 
                if len(word) > 4 and word.isalpha()
            ]
            
            if len(important_words) < 6:
                important_words = [
                    word.strip('.,;:!?"\'') 
                    for word in words 
                    if word.isalpha()
                ][:6]
            else:
                important_words = important_words[:6]
            
            create_mindmap(important_words)
            print(f"✅ Mindmap created with words: {important_words}")
        except Exception as e:
            print(f"⚠️ Mindmap failed: {e}")
        
        print("🎉 SUCCESS!")
        return render_template('result.html', summary=summary, quiz=quiz)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        flash(f"Error: {str(e)}", 'danger')
        return redirect(url_for('home'))

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz_page():
    if 'quiz' not in session:
        return redirect(url_for('home'))
    
    quiz = session['quiz']
    
    if request.method == 'POST':
        score = 0
        
        for i, q in enumerate(quiz):
            q_type = q.get('type', 'fill_blank')
            
            if q_type == 'mcq':
                user_answer = request.form.get(f'answer_{i}', '').strip()
                if user_answer.lower() == q['a'].lower():
                    score += 10
            
            elif q_type == 'true_false':
                user_answer = request.form.get(f'answer_{i}', '').strip().lower()
                if user_answer == q['a'].lower():
                    score += 10
            
            elif q_type == 'fill_blank':
                user_answer = request.form.get(f'answer_{i}', '').strip()
                if user_answer.lower() == q['a'].lower():
                    score += 10
            
            elif q_type == 'matching':
                correct_matches = 0
                for j in range(len(q.get('list_a', []))):
                    user_match = request.form.get(f'answer_{i}_{j}', '').strip()
                    correct_answer = q['a'].get(j, '')
                    if user_match == correct_answer:
                        correct_matches += 1
                
                if len(q.get('list_a', [])) > 0:
                    match_score = int((correct_matches / len(q['list_a'])) * 10)
                    score += match_score
        
        quiz_result = QuizResult(
            score=score,
            total_questions=len(quiz),
            user_id=current_user.id
        )
        db.session.add(quiz_result)
        
        current_user.score += score
        current_user.level = (current_user.score // 100) + 1
        db.session.commit()
        
        session['score'] = score
        return redirect(url_for('gamification'))
    
    return render_template('quiz.html', quiz=quiz)

# ================= ✨ FLASHCARDS ROUTES ✨ =================
@app.route('/flashcards')
@login_required
def flashcards():
    if 'quiz' not in session:
        flash('Please generate a summary first to create flashcards', 'warning')
        return redirect(url_for('home'))
    
    quiz = session['quiz']
    return render_template('flashcards.html', quiz=quiz)

@app.route('/submit-flashcards', methods=['POST'])
@login_required
def submit_flashcards():
    if 'quiz' not in session:
        return redirect(url_for('home'))
    
    known_count = int(request.form.get('known_count', 0))
    total_cards = len(session['quiz'])
    score = known_count * 10
    
    quiz_result = QuizResult(
        score=score,
        total_questions=total_cards,
        user_id=current_user.id
    )
    db.session.add(quiz_result)
    
    current_user.score += score
    current_user.level = (current_user.score // 100) + 1
    db.session.commit()
    
    flash(f'Flashcards completed! You scored {score} points!', 'success')
    return redirect(url_for('gamification'))

# ================= Gamification Routes =================
@app.route('/gamification')
@login_required
def gamification():
    quiz = session.get('quiz', [])
    score = session.get('score', 0)
    return render_template('gamification.html', quiz=quiz, score=score)

@app.route('/leaderboard')
def leaderboard():
    top_users = User.query.order_by(User.score.desc()).limit(10).all()
    return render_template('leaderboard.html', users=top_users)

@app.route('/shared-library')
@login_required
def shared_library():
    shared_uploads = Upload.query.filter_by(is_shared=True).order_by(Upload.uploaded_at.desc()).all()
    return render_template('shared_library.html', uploads=shared_uploads)

@app.route('/share-upload/<int:upload_id>')
@login_required
def share_upload(upload_id):
    upload = Upload.query.get_or_404(upload_id)
    if upload.user_id == current_user.id:
        upload.is_shared = not upload.is_shared
        db.session.commit()
        flash('Upload sharing status updated', 'success')
    return redirect(url_for('dashboard'))

@app.route('/daily-challenge')
@login_required
def daily_challenge():
    today = datetime.utcnow().date()
    challenge = DailyChallenge.query.filter_by(date=today, active=True).first()
    
    if not challenge:
        challenge = DailyChallenge(
            title="Complete 3 Quizzes",
            description="Complete at least 3 quizzes today to earn bonus points!",
            points=50,
            date=today
        )
        db.session.add(challenge)
        db.session.commit()
    
    return render_template('daily_challenge.html', challenge=challenge)

# ================= Quiz Battles Routes =================
@app.route('/quiz-battles')
@login_required
def quiz_battles():
    battles = QuizBattle.query.filter_by(status='active').all()
    return render_template('quiz_battles.html', battles=battles)

@app.route('/create-battle', methods=['POST'])
@login_required
def create_battle():
    title = request.form.get('title', 'Quick Battle')
    
    battle = QuizBattle(title=title)
    db.session.add(battle)
    db.session.commit()
    
    participant = BattleParticipant(battle_id=battle.id, user_id=current_user.id)
    db.session.add(participant)
    db.session.commit()
    
    flash('Battle created successfully!', 'success')
    return redirect(url_for('battle_room', battle_id=battle.id))

@app.route('/battle/<int:battle_id>')
@login_required
def battle_room(battle_id):
    battle = QuizBattle.query.get_or_404(battle_id)
    
    participant = BattleParticipant.query.filter_by(
        battle_id=battle_id, 
        user_id=current_user.id
    ).first()
    
    if not participant:
        participant = BattleParticipant(battle_id=battle_id, user_id=current_user.id)
        db.session.add(participant)
        db.session.commit()
    
    quiz = session.get('quiz', [])
    return render_template('battle_room.html', battle=battle, quiz=quiz)

@app.route('/submit-battle/<int:battle_id>', methods=['POST'])
@login_required
def submit_battle(battle_id):
    participant = BattleParticipant.query.filter_by(
        battle_id=battle_id,
        user_id=current_user.id
    ).first_or_404()
    
    quiz = session.get('quiz', [])
    score = 0
    
    for i, q in enumerate(quiz):
        user_answer = request.form.get(f'answer_{i}', '').strip().lower()
        if user_answer == q['a'].lower():
            score += 10
    
    participant.score = score
    participant.completed = True
    
    current_user.score += score
    current_user.level = (current_user.score // 100) + 1
    
    db.session.commit()
    
    battle = QuizBattle.query.get(battle_id)
    all_completed = all(p.completed for p in battle.participants)
    
    if all_completed:
        winner = max(battle.participants, key=lambda p: p.score)
        battle.winner_id = winner.user_id
        battle.status = 'completed'
        db.session.commit()
    
    flash(f'Battle submitted! Your score: {score}', 'success')
    return redirect(url_for('quiz_battles'))

# ================= Puzzle Mode Routes =================
@app.route('/puzzle-mode')
@login_required
def puzzle_mode():
    summary = session.get('summary', 'Learning is fun. Knowledge is power. Education transforms lives.')
    
    import random
    words = summary.split()
    scrambled = words.copy()
    random.shuffle(scrambled)
    
    puzzle = PuzzleGame(
        user_id=current_user.id,
        content=summary,
        scrambled_words=' '.join(scrambled)
    )
    db.session.add(puzzle)
    db.session.commit()
    
    return render_template('puzzle_mode.html', 
                         original=summary, 
                         scrambled=scrambled,
                         puzzle_id=puzzle.id)

@app.route('/submit-puzzle/<int:puzzle_id>', methods=['POST'])
@login_required
def submit_puzzle(puzzle_id):
    puzzle = PuzzleGame.query.get_or_404(puzzle_id)
    user_answer = request.form.get('answer', '').strip()
    
    original_words = puzzle.content.lower().split()
    user_words = user_answer.lower().split()
    
    correct = sum(1 for w in user_words if w in original_words)
    score = int((correct / len(original_words)) * 100)
    
    puzzle.score = score
    puzzle.completed = True
    
    current_user.score += score
    current_user.level = (current_user.score // 100) + 1
    
    db.session.commit()
    
    flash(f'Puzzle completed! Score: {score}%', 'success')
    return redirect(url_for('gamification'))

# ================= Grading Center Routes =================
@app.route('/grading-center')
@login_required
def grading_center():
    results = QuizResult.query.filter_by(user_id=current_user.id).order_by(
        QuizResult.completed_at.desc()
    ).all()
    
    total_quizzes = len(results)
    avg_score = sum(r.score for r in results) / total_quizzes if total_quizzes > 0 else 0
    
    return render_template('grading_center.html', 
                         results=results,
                         total_quizzes=total_quizzes,
                         avg_score=avg_score)

# ================= Review System Routes =================
@app.route('/review/<int:upload_id>', methods=['GET', 'POST'])
@login_required
def review_upload(upload_id):
    upload = Upload.query.get_or_404(upload_id)
    
    if request.method == 'POST':
        rating = int(request.form.get('rating', 3))
        comment = request.form.get('comment', '')
        
        review = Review(
            upload_id=upload_id,
            user_id=current_user.id,
            rating=rating,
            comment=comment
        )
        db.session.add(review)
        db.session.commit()
        
        flash('Review submitted successfully!', 'success')
        return redirect(url_for('shared_library'))
    
    reviews = Review.query.filter_by(upload_id=upload_id).all()
    avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
    
    return render_template('review_upload.html', 
                         upload=upload, 
                         reviews=reviews,
                         avg_rating=avg_rating)

# ================= Search Routes =================
@app.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    
    if not query:
        return render_template('search.html', results=[], query='')
    
    results = Upload.query.filter(
        db.or_(
            Upload.filename.contains(query),
            Upload.summary.contains(query)
        )
    ).filter_by(is_shared=True).all()
    
    return render_template('search.html', results=results, query=query)

# ================= Export Routes =================
@app.route('/export/<int:upload_id>/<format>')
@login_required
def export_upload(upload_id, format):
    upload = Upload.query.get_or_404(upload_id)
    
    if format == 'txt':
        return Response(
            upload.summary,
            mimetype='text/plain',
            headers={'Content-Disposition': f'attachment;filename={upload.filename}.txt'}
        )
    
    elif format == 'pdf':
        buffer = BytesIO()
        buffer.write(upload.summary.encode('utf-8'))
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'{upload.filename}.txt',
            mimetype='text/plain'
        )
    
    flash('Export format not supported yet', 'warning')
    return redirect(url_for('dashboard'))

# ================= Analytics Routes =================
@app.route('/analytics')
@login_required
def analytics():
    quiz_results = QuizResult.query.filter_by(user_id=current_user.id).all()
    uploads = Upload.query.filter_by(user_id=current_user.id).all()
    
    stats = calculate_user_stats(current_user, quiz_results, uploads)
    performance_data = analyze_quiz_performance(quiz_results)
    weekly_report = generate_performance_report(current_user, quiz_results)
    
    return render_template('analytics.html', 
                         stats=stats,
                         performance=performance_data,
                         weekly_report=weekly_report)

# ================= Visualization Routes =================
@app.route('/visualize/<int:upload_id>')
@login_required
def visualize_upload(upload_id):
    upload = Upload.query.get_or_404(upload_id)
    
    keywords = extract_keywords(upload.summary)
    keyword_freq = {kw: upload.summary.lower().count(kw) for kw in keywords}
    chart_path = create_bar_chart(
        list(keyword_freq.keys()),
        list(keyword_freq.values()),
        f"Keyword Frequency: {upload.filename}"
    )
    
    return render_template('visualize.html', 
                         upload=upload,
                         chart=chart_path,
                         keywords=keywords)

# ================= OCR Route =================
@app.route('/ocr-upload', methods=['POST'])
@login_required
def ocr_upload():
    file = request.files.get('file')
    
    if not file:
        flash('No file uploaded', 'warning')
        return redirect(url_for('home'))
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    text = extract_text_from_image(filepath)
    
    if text:
        flash('Text extracted successfully!', 'success')
        cleaned_text = preprocess_text(text)
        summary = summarize_text(cleaned_text)
        quiz = generate_quiz(summary)
        
        session['summary'] = summary
        session['quiz'] = quiz
        
        return render_template('result.html', summary=summary, quiz=quiz)
    else:
        flash('Could not extract text from image', 'danger')
        return redirect(url_for('home'))

# ================= Admin Routes =================
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'vortex2026':
            session['is_admin'] = True
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials', 'danger')
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    
    total_users = User.query.count()
    total_uploads = Upload.query.count()
    total_quizzes = QuizResult.query.count()
    total_battles = QuizBattle.query.count()
    
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    recent_uploads = Upload.query.order_by(Upload.uploaded_at.desc()).limit(10).all()
    
    return render_template('admin_dashboard.html',
                         total_users=total_users,
                         total_uploads=total_uploads,
                         total_quizzes=total_quizzes,
                         total_battles=total_battles,
                         recent_users=recent_users,
                         recent_uploads=recent_uploads)

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    flash('Admin logged out', 'info')
    return redirect(url_for('home'))

@app.route('/admin/users')
def admin_users():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    
    users = User.query.order_by(User.score.desc()).all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/delete-user/<int:user_id>')
def admin_delete_user(user_id):
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    
    user = User.query.get_or_404(user_id)
    
    Upload.query.filter_by(user_id=user_id).delete()
    QuizResult.query.filter_by(user_id=user_id).delete()
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {user.username} deleted successfully', 'success')
    return redirect(url_for('admin_users'))

# ================= Run Server =================
if __name__ == '__main__':
    print("🚀 Vortex is running...")
    print("📚 Flashcards feature enabled!")
    print("✨ File processing optimized!")
    print("🌍 Arabic/English language support enabled!")
    app.run(host="0.0.0.0", port=5000, debug=True)