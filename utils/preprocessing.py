import re

def preprocess_text(text):
    """تنظيف النص الأساسي"""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9.,!? ]', '', text)
    return text.strip()