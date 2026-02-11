import re
import nltk
from collections import Counter

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

def summarize_text(text, max_sentences=5, use_nlp=True):
    if not text or len(text) < 100:
        return text
    
    if use_nlp:
        sentences = sent_tokenize(text)
        
        if len(sentences) <= max_sentences:
            return text
        
        stop_words = set(stopwords.words('english'))
        word_freq = Counter()
        
        for sentence in sentences:
            words = word_tokenize(sentence.lower())
            words = [w for w in words if w.isalnum() and w not in stop_words]
            word_freq.update(words)
        
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            words = word_tokenize(sentence.lower())
            score = sum(word_freq[w] for w in words if w in word_freq)
            sentence_scores[i] = score
        
        top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:max_sentences]
        top_sentences.sort()
        
        summary = ' '.join([sentences[i] for i in top_sentences])
        return summary
    
    else:
        sentences = text.split('.')
        sentences = [s.strip() for s in sentences if len(s.split()) > 6]
        return '. '.join(sentences[:max_sentences]) + '.'

def extract_keywords(text, num_keywords=10):
    try:
        stop_words = set(stopwords.words('english'))
    except:
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'are', 'was', 'were'}
    
    words = text.lower().split()
    words = [w.strip('.,;:!?"\'') for w in words if len(w) > 3 and w.isalpha()]
    words = [w for w in words if w not in stop_words]
    
    word_freq = Counter(words)
    keywords = [word for word, freq in word_freq.most_common(num_keywords)]
    
    return keywords if keywords else ['sample', 'keyword']