import re
import nltk
from collections import Counter

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
    """
    Original summarize function (kept for backward compatibility)
    """
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


def summarize_text_with_style(text, style='paragraphs', length='medium'):
    """
    Generate summary with custom style and length
    
    Args:
        text: Input text to summarize
        style: 'bullets', 'paragraphs', 'numbered', 'very_short', 'detailed'
        length: 'short', 'medium', 'long'
    
    Returns:
        Formatted summary string
    """
    if not text or len(text) < 50:
        return text
    
    # Length configuration
    length_config = {
        'short': 3,      # 3 sentences
        'medium': 5,     # 5 sentences
        'long': 8        # 8 sentences
    }
    
    max_sentences = length_config.get(length, 5)
    
    try:
        # Tokenize sentences
        sentences = sent_tokenize(text)
        
        if len(sentences) <= 2:
            return text
        
        # Calculate sentence importance
        stop_words = set(stopwords.words('english'))
        word_freq = Counter()
        
        for sentence in sentences:
            words = word_tokenize(sentence.lower())
            words = [w for w in words if w.isalnum() and w not in stop_words]
            word_freq.update(words)
        
        # Score sentences
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            words = word_tokenize(sentence.lower())
            score = sum(word_freq[w] for w in words if w in word_freq)
            sentence_scores[i] = score
        
        # Get top sentences
        top_sentence_indices = sorted(
            sentence_scores, 
            key=sentence_scores.get, 
            reverse=True
        )[:max_sentences]
        
        # Sort by original order
        top_sentence_indices.sort()
        selected_sentences = [sentences[i] for i in top_sentence_indices]
        
        # Format based on style
        if style == 'bullets':
            # Bullet points format
            formatted = '\n'.join([f"• {s.strip()}" for s in selected_sentences])
            
        elif style == 'numbered':
            # Numbered list format
            formatted = '\n'.join([f"{i+1}. {s.strip()}" for i, s in enumerate(selected_sentences)])
            
        elif style == 'very_short':
            # Ultra concise - only 2 most important sentences
            very_short = [sentences[i] for i in sorted(top_sentence_indices[:2])]
            formatted = ' '.join(very_short)
            
        elif style == 'detailed':
            # Detailed with paragraph breaks
            # Group into paragraphs of 2-3 sentences
            paragraphs = []
            for i in range(0, len(selected_sentences), 3):
                para = ' '.join(selected_sentences[i:i+3])
                paragraphs.append(para)
            formatted = '\n\n'.join(paragraphs)
            
        else:  # paragraphs (default)
            # Standard paragraph format
            formatted = ' '.join(selected_sentences)
        
        return formatted if formatted else ' '.join(selected_sentences)
        
    except Exception as e:
        print(f"⚠️ Summarization with style failed: {e}")
        # Fallback to basic summary
        sentences = text.split('.')
        sentences = [s.strip() for s in sentences if len(s.split()) > 5]
        basic_summary = '. '.join(sentences[:max_sentences])
        
        # Apply basic formatting even in fallback
        if style == 'bullets':
            return '\n'.join([f"• {s.strip()}." for s in sentences[:max_sentences]])
        elif style == 'numbered':
            return '\n'.join([f"{i+1}. {s.strip()}." for i, s in enumerate(sentences[:max_sentences])])
        else:
            return basic_summary + '.'


def extract_keywords(text, num_keywords=10):
    """
    Extract important keywords from text
    """
    try:
        stop_words = set(stopwords.words('english'))
    except:
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 
            'for', 'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 
            'should', 'could', 'may', 'might', 'must', 'can', 'this', 
            'that', 'these', 'those', 'it', 'its', 'as', 'by', 'from'
        }
    
    # Clean and tokenize
    words = text.lower().split()
    words = [w.strip('.,;:!?"\'()[]{}') for w in words if len(w) > 3 and w.isalpha()]
    words = [w for w in words if w not in stop_words]
    
    # Count frequencies
    word_freq = Counter(words)
    keywords = [word for word, freq in word_freq.most_common(num_keywords)]
    
    return keywords if keywords else ['learning', 'knowledge', 'education']