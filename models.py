from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# ================= User Model =================
class User(UserMixin, db.Model):
    """نموذج المستخدم الرئيسي"""
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer, default=0, index=True)
    level = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # العلاقات مع الجداول الأخرى
    uploads = db.relationship('Upload', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    quiz_results = db.relationship('QuizResult', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    battle_participations = db.relationship('BattleParticipant', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    puzzle_games = db.relationship('PuzzleGame', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    subjects = db.relationship('Subject', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_total_uploads(self):
        """الحصول على عدد الملفات المرفوعة"""
        return self.uploads.count()
    
    def get_total_quizzes(self):
        """الحصول على عدد الاختبارات المكتملة"""
        return self.quiz_results.count()
    
    def get_average_score(self):
        """حساب متوسط الدرجات"""
        results = self.quiz_results.all()
        if not results:
            return 0
        total_score = sum(r.score for r in results)
        total_possible = sum(r.total_questions * 10 for r in results)
        return round((total_score / total_possible * 100), 2) if total_possible > 0 else 0
    
    def update_level(self):
        """تحديث المستوى بناءً على النقاط"""
        self.level = (self.score // 100) + 1
        return self.level

# ================= Upload Model =================
class Upload(db.Model):
    """نموذج الملفات المرفوعة"""
    __tablename__ = 'upload'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    quiz_data = db.Column(db.Text, nullable=True)  # JSON string للكويز
    keywords = db.Column(db.Text, nullable=True)   # JSON string للكلمات المفتاحية
    is_shared = db.Column(db.Boolean, default=False, index=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id', ondelete='SET NULL'), nullable=True, index=True)
    
    # العلاقات
    reviews = db.relationship('Review', backref='upload', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Upload {self.filename}>'
    
    def get_average_rating(self):
        """حساب متوسط التقييمات"""
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.rating for r in reviews) / len(reviews), 1)
    
    def get_review_count(self):
        """الحصول على عدد المراجعات"""
        return self.reviews.count()

# ================= Subject Model =================
class Subject(db.Model):
    """نموذج المواد الدراسية"""
    __tablename__ = 'subject'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(50), default='📘')
    color = db.Column(db.String(20), default='#5DBAA4')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # العلاقات
    chapters = db.relationship('Chapter', backref='subject', lazy='dynamic', cascade='all, delete-orphan', order_by='Chapter.order')
    
    def __repr__(self):
        return f'<Subject {self.name}>'
    
    def get_chapter_count(self):
        """عدد الشباتر"""
        return self.chapters.count()
    
    def get_total_uploads(self):
        """عدد الملفات في كل الشباتر"""
        total = 0
        for chapter in self.chapters:
            total += chapter.get_upload_count()
        return total
    
    def get_progress_percentage(self):
        """نسبة الإنجاز (بناءً على عدد الملفات)"""
        total_chapters = self.get_chapter_count()
        if total_chapters == 0:
            return 0
        chapters_with_uploads = sum(1 for c in self.chapters if c.get_upload_count() > 0)
        return round((chapters_with_uploads / total_chapters) * 100, 1)

# ================= Chapter Model =================
class Chapter(db.Model):
    """نموذج الشباتر (الفصول الدراسية)"""
    __tablename__ = 'chapter'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, default=1, index=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # العلاقات
    uploads = db.relationship('Upload', backref='chapter', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Chapter {self.name}>'
    
    def get_upload_count(self):
        """عدد الملفات في هذا الشابتر"""
        return self.uploads.count()
    
    def get_latest_upload(self):
        """آخر ملف تم رفعه"""
        return self.uploads.order_by(Upload.uploaded_at.desc()).first()
    
    def is_completed(self):
        """التحقق من اكتمال الشابتر (إذا كان فيه 3 ملفات على الأقل)"""
        return self.get_upload_count() >= 3

# ================= QuizResult Model =================
class QuizResult(db.Model):
    """نموذج نتائج الاختبارات"""
    __tablename__ = 'quiz_result'
    
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    
    def __repr__(self):
        return f'<QuizResult User:{self.user_id} Score:{self.score}/{self.total_questions * 10}>'
    
    def get_percentage(self):
        """حساب النسبة المئوية"""
        if self.total_questions == 0:
            return 0
        return round((self.score / (self.total_questions * 10)) * 100, 2)
    
    def get_grade(self):
        """الحصول على التقدير"""
        percentage = self.get_percentage()
        if percentage >= 90:
            return 'A+'
        elif percentage >= 80:
            return 'A'
        elif percentage >= 70:
            return 'B'
        elif percentage >= 60:
            return 'C'
        else:
            return 'D'

# ================= DailyChallenge Model =================
class DailyChallenge(db.Model):
    """نموذج التحديات اليومية"""
    __tablename__ = 'daily_challenge'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    points = db.Column(db.Integer, default=50)
    date = db.Column(db.Date, default=datetime.utcnow, index=True, unique=True)
    active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DailyChallenge {self.title} - {self.date}>'
    
    def is_today(self):
        """التحقق من أن التحدي لليوم"""
        return self.date == datetime.utcnow().date()

# ================= QuizBattle Model =================
class QuizBattle(db.Model):
    """نموذج معارك الاختبارات"""
    __tablename__ = 'quiz_battle'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    status = db.Column(db.String(50), default='active', index=True)  # active, completed, cancelled
    winner_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    
    # العلاقات
    participants = db.relationship('BattleParticipant', backref='battle', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<QuizBattle {self.title} - {self.status}>'
    
    def get_participant_count(self):
        """عدد المشاركين"""
        return self.participants.count()
    
    def get_top_score(self):
        """أعلى نقاط"""
        participants = self.participants.all()
        if not participants:
            return 0
        return max(p.score for p in participants)
    
    def is_completed(self):
        """التحقق من اكتمال المعركة"""
        return self.status == 'completed'
    
    def check_completion(self):
        """فحص إذا كان جميع المشاركين أنهوا"""
        participants = self.participants.all()
        if not participants:
            return False
        return all(p.completed for p in participants)

# ================= BattleParticipant Model =================
class BattleParticipant(db.Model):
    """نموذج المشاركين في المعارك"""
    __tablename__ = 'battle_participant'
    
    id = db.Column(db.Integer, primary_key=True)
    battle_id = db.Column(db.Integer, db.ForeignKey('quiz_battle.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    score = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False, index=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint لمنع المستخدم من الانضمام مرتين
    __table_args__ = (
        db.UniqueConstraint('battle_id', 'user_id', name='unique_battle_participant'),
    )
    
    def __repr__(self):
        return f'<BattleParticipant User:{self.user_id} Battle:{self.battle_id} Score:{self.score}>'
    
    def get_rank(self):
        """الحصول على الترتيب في المعركة"""
        participants = BattleParticipant.query.filter_by(
            battle_id=self.battle_id
        ).order_by(BattleParticipant.score.desc()).all()
        
        for index, participant in enumerate(participants, 1):
            if participant.id == self.id:
                return index
        return None

# ================= Review Model =================
class Review(db.Model):
    """نموذج المراجعات والتقييمات"""
    __tablename__ = 'review'
    
    id = db.Column(db.Integer, primary_key=True)
    upload_id = db.Column(db.Integer, db.ForeignKey('upload.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Unique constraint لمنع المستخدم من مراجعة نفس الملف مرتين
    __table_args__ = (
        db.UniqueConstraint('upload_id', 'user_id', name='unique_user_review'),
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='valid_rating')
    )
    
    def __repr__(self):
        return f'<Review {self.rating}★ by User:{self.user_id} for Upload:{self.upload_id}>'
    
    def get_stars_html(self):
        """HTML للنجوم"""
        filled = '★' * self.rating
        empty = '☆' * (5 - self.rating)
        return filled + empty

# ================= PuzzleGame Model =================
class PuzzleGame(db.Model):
    """نموذج ألعاب الأحجية"""
    __tablename__ = 'puzzle_game'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    scrambled_words = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<PuzzleGame {self.id} - User:{self.user_id} - Score:{self.score}%>'
    
    def complete(self, score):
        """إكمال اللعبة"""
        self.completed = True
        self.score = score
        self.completed_at = datetime.utcnow()
    
    def get_accuracy(self):
        """الحصول على دقة الإجابة"""
        return f"{self.score}%"

# ================= Admin Model =================
class Admin(UserMixin, db.Model):
    """نموذج المسؤولين"""
    __tablename__ = 'admin'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Admin {self.username}>'
    
    def update_last_login(self):
        """تحديث آخر تسجيل دخول"""
        self.last_login = datetime.utcnow()
    
    def get_id(self):
        """Override لـ Flask-Login"""
        return f"admin_{self.id}"

# ================= Utility Functions =================
def init_db(app):
    """تهيئة قاعدة البيانات"""
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")

def create_default_admin(app):
    """إنشاء مسؤول افتراضي"""
    from werkzeug.security import generate_password_hash
    
    with app.app_context():
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(
                username='admin',
                password=generate_password_hash('vortex2026', method='pbkdf2:sha256')
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin created!")
            print("   Username: admin")
            print("   Password: vortex2026")

def get_statistics():
    """إحصائيات عامة للمنصة"""
    return {
        'total_users': User.query.count(),
        'total_uploads': Upload.query.count(),
        'total_quizzes': QuizResult.query.count(),
        'total_battles': QuizBattle.query.count(),
        'total_reviews': Review.query.count(),
        'total_subjects': Subject.query.count(),
        'total_chapters': Chapter.query.count(),
        'active_battles': QuizBattle.query.filter_by(status='active').count()
    }

def cleanup_old_data(days=30):
    """تنظيف البيانات القديمة"""
    from datetime import timedelta
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # حذف الألعاب القديمة المكتملة
    old_puzzles = PuzzleGame.query.filter(
        PuzzleGame.completed == True,
        PuzzleGame.completed_at < cutoff_date
    ).delete()
    
    # حذف التحديات القديمة غير النشطة
    old_challenges = DailyChallenge.query.filter(
        DailyChallenge.active == False,
        DailyChallenge.created_at < cutoff_date
    ).delete()
    
    db.session.commit()
    
    return {
        'puzzles_deleted': old_puzzles,
        'challenges_deleted': old_challenges
    }