import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime

def create_table_visualization(data, title="Data Table", output_path=None):
    if not output_path:
        output_path = f'static/images/table_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('tight')
    ax.axis('off')
    
    table = ax.table(
        cellText=data['values'],
        colLabels=data['columns'],
        cellLoc='center',
        loc='center'
    )
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)
    
    for i in range(len(data['columns'])):
        table[(0, i)].set_facecolor('#6C63FF')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    plt.title(title, fontsize=14, weight='bold')
    plt.savefig(output_path, bbox_inches='tight', dpi=150)
    plt.close()
    
    return output_path

def create_bar_chart(labels, values, title="Performance Chart", output_path=None):
    if not output_path:
        output_path = f'static/images/chart_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='#6C63FF', alpha=0.8)
    plt.xlabel('Categories', fontsize=12)
    plt.ylabel('Values', fontsize=12)
    plt.title(title, fontsize=14, weight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    
    return output_path

def create_pie_chart(labels, values, title="Distribution", output_path=None):
    if not output_path:
        output_path = f'static/images/pie_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    
    plt.figure(figsize=(8, 8))
    colors = ['#6C63FF', '#8A76FF', '#A68EFF', '#C2A6FF', '#DEBEFF']
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title(title, fontsize=14, weight='bold')
    plt.axis('equal')
    plt.savefig(output_path, dpi=150)
    plt.close()
    
    return output_path

def create_line_chart(x_data, y_data, title="Trend Analysis", output_path=None):
    if not output_path:
        output_path = f'static/images/line_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_data, y_data, marker='o', color='#6C63FF', linewidth=2, markersize=8)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.title(title, fontsize=14, weight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    
    return output_path

def analyze_quiz_performance(quiz_results):
    if not quiz_results:
        return None
    
    scores = [r.score for r in quiz_results]
    dates = [r.completed_at.strftime('%m/%d') for r in quiz_results]
    
    chart_path = create_line_chart(dates, scores, "Your Performance Trend")
    
    return {
        'chart': chart_path,
        'avg_score': sum(scores) / len(scores),
        'max_score': max(scores),
        'min_score': min(scores),
        'total_quizzes': len(scores)
    }