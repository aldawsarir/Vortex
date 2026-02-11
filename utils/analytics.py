from datetime import datetime, timedelta
from collections import Counter

def calculate_user_stats(user, quiz_results, uploads):
    total_quizzes = len(quiz_results)
    
    if total_quizzes == 0:
        return {
            'total_quizzes': 0,
            'avg_score': 0,
            'total_score': user.score,
            'level': user.level,
            'accuracy': 0,
            'total_uploads': len(uploads),
            'study_streak': 0,
            'most_active_day': 'N/A'
        }
    
    total_correct = sum(r.score for r in quiz_results)
    total_questions = sum(r.total_questions * 10 for r in quiz_results)
    
    accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0
    
    quiz_dates = [r.completed_at.date() for r in quiz_results]
    date_counter = Counter(quiz_dates)
    most_active_day = max(date_counter, key=date_counter.get).strftime('%A') if date_counter else 'N/A'
    
    study_streak = calculate_streak(quiz_dates)
    
    return {
        'total_quizzes': total_quizzes,
        'avg_score': total_correct / total_quizzes if total_quizzes > 0 else 0,
        'total_score': user.score,
        'level': user.level,
        'accuracy': round(accuracy, 1),
        'total_uploads': len(uploads),
        'study_streak': study_streak,
        'most_active_day': most_active_day
    }

def calculate_streak(dates):
    if not dates:
        return 0
    
    sorted_dates = sorted(set(dates), reverse=True)
    streak = 1
    
    for i in range(len(sorted_dates) - 1):
        diff = (sorted_dates[i] - sorted_dates[i + 1]).days
        if diff == 1:
            streak += 1
        else:
            break
    
    return streak

def generate_performance_report(user, quiz_results):
    if not quiz_results:
        return None
    
    weekly_data = {}
    for result in quiz_results:
        week = result.completed_at.strftime('%Y-W%W')
        if week not in weekly_data:
            weekly_data[week] = {'total': 0, 'correct': 0, 'count': 0}
        
        weekly_data[week]['total'] += result.total_questions
        weekly_data[week]['correct'] += result.score / 10
        weekly_data[week]['count'] += 1
    
    weekly_performance = []
    for week, data in sorted(weekly_data.items()):
        accuracy = (data['correct'] / data['total'] * 100) if data['total'] > 0 else 0
        weekly_performance.append({
            'week': week,
            'quizzes': data['count'],
            'accuracy': round(accuracy, 1)
        })
    
    return weekly_performance