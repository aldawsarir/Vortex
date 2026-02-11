import random
import re

def generate_quiz(text, num_questions=10):
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.split()) > 5]
    
    if len(sentences) < num_questions:
        num_questions = len(sentences)
    
    if num_questions == 0:
        return []
    
    selected_sentences = random.sample(sentences, min(num_questions, len(sentences)))
    
    question_types = ['mcq', 'true_false', 'fill_blank', 'matching', 'mcq',
                      'true_false', 'fill_blank', 'mcq', 'matching', 'true_false']
    
    quiz = []
    for i, sentence in enumerate(selected_sentences):
        q_type = question_types[i % len(question_types)]
        
        if q_type == 'mcq':
            question = generate_mcq(sentence)
        elif q_type == 'true_false':
            question = generate_true_false(sentence)
        elif q_type == 'matching':
            question = generate_matching(
                selected_sentences[i:i+4]
                if i+4 <= len(selected_sentences)
                else selected_sentences[-4:]
            )
        else:
            question = generate_fill_blank(sentence)
        
        if question:
            quiz.append(question)
        else:
            fallback = generate_fill_blank(sentence)
            if fallback:
                quiz.append(fallback)
    
    return quiz

def generate_mcq(sentence):
    words = sentence.split()
    
    important_words = [w.strip('.,;:!?"\'') for w in words if len(w) > 3 and w.isalpha()]
    
    if not important_words:
        return None
    
    correct_word = random.choice(important_words)
    question_text = sentence.replace(correct_word, "______", 1)
    
    wrong_options = []
    
    similar_words = [
        'learning', 'studying', 'knowledge', 'education', 'information',
        'science', 'technology', 'research', 'analysis', 'development'
    ]
    wrong_options.append(
        random.choice([w for w in similar_words if w != correct_word.lower()])
    )
    
    if len(correct_word) > 5:
        wrong_options.append(correct_word[:4] + 'ing')
    else:
        wrong_options.append(correct_word + 'ed')
    
    random_words = ['process', 'system', 'method', 'theory', 'concept', 'practice']
    wrong_options.append(
        random.choice([w for w in random_words if w != correct_word.lower()])
    )
    
    options = [correct_word] + wrong_options[:3]
    random.shuffle(options)
    
    return {
        'type': 'mcq',
        'q': question_text,
        'a': correct_word,
        'options': options
    }

def generate_true_false(sentence):
    is_true = random.choice([True, False])
    
    if is_true:
        question_text = sentence
        answer = 'true'
    else:
        words = sentence.split()
        if len(words) > 5:
            important_idx = [
                i for i, w in enumerate(words)
                if len(w) > 4 and w.isalpha()
            ]
            if important_idx:
                idx = random.choice(important_idx)
                replacement_words = ['never', 'always', 'sometimes', 'rarely', 'often']
                words[idx] = random.choice(replacement_words)
            question_text = " ".join(words)
            answer = 'false'
        else:
            question_text = sentence
            answer = 'true'
    
    return {
        'type': 'true_false',
        'q': question_text,
        'a': answer
    }

def generate_fill_blank(sentence):
    words = sentence.split()
    
    important_words = [
        (i, w.strip('.,;:!?"\''))
        for i, w in enumerate(words)
        if len(w) > 4 and w.isalpha()
    ]
    
    if not important_words:
        return None
    
    idx, word = random.choice(important_words)
    words[idx] = "______"
    
    return {
        'type': 'fill_blank',
        'q': " ".join(words),
        'a': word
    }

def generate_matching(sentences):
    if len(sentences) < 2:
        return None
    
    sentences = sentences[:4]
    
    list_a = []
    list_b = []
    
    for i, sentence in enumerate(sentences):
        words = sentence.split()
        important_words = [w.strip('.,;:!?"\'') for w in words if len(w) > 4 and w.isalpha()]
        
        if not important_words:
            continue
        
        list_a.append(f"{i+1}. {' '.join(words[:5])}...")
        list_b.append(random.choice(important_words))
    
    if len(list_a) < 2:
        return None
    
    correct_mapping = {i: list_b[i] for i in range(len(list_b))}
    random.shuffle(list_b)
    
    return {
        'type': 'matching',
        'q': 'Match items from List A with List B:',
        'list_a': list_a,
        'list_b': list_b,
        'a': correct_mapping
    }