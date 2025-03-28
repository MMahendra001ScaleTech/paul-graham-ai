# src/extract_features.py

import re
import json
from collections import Counter
import nltk
from textstat import flesch_reading_ease, text_standard
from textblob import TextBlob

nltk.download('punkt')

def extract_features(text, title=""):
    # --- Preprocessing ---
    sentences = nltk.sent_tokenize(text)
    words = nltk.word_tokenize(text)
    word_count = len(words)
    sentence_count = len(sentences)
    words_lower = [w.lower() for w in words]

    # ✅ Feature 1: Essay Title
    essay_title = title

    # ✅ Feature 2: Section Headings Count
    section_headings_count = len(re.findall(r'\n\s*[A-Z][^\n]+\n', text))

    # ✅ Feature 3: Number of Sentences
    num_sentences = sentence_count

    # ✅ Feature 4: Average Sentence Length
    avg_sentence_length = word_count / (sentence_count or 1)

    # ✅ Feature 5: First-Person Ratio
    first_person_count = sum(1 for w in words_lower if w in ["i", "we"])
    first_person_ratio = first_person_count / (word_count or 1)

    # ✅ Feature 6: Anecdote Count
    anecdote_count = sum(1 for s in sentences if "when I " in s or "we once" in s)

    # ✅ Feature 7: Question Count
    question_count = sum(1 for s in sentences if '?' in s)

    # ✅ Feature 8: Quote Count
    quote_count = text.count('"') + text.count('“') + text.count('”')

    # ✅ Feature 9: Metaphor Count
    metaphor_triggers = ["like", "as if", "as though", "it's like", "imagine", "picture"]
    metaphor_count = sum(1 for trigger in metaphor_triggers if trigger in text.lower())

    # ✅ Feature 10: Argument Flow Indicator
    problem_words = ["problem", "difficult", "issue", "hard"]
    solution_words = ["solution", "solve", "way", "method"]
    argument_ratio = sum(1 for w in words_lower if w in problem_words + solution_words) / (word_count or 1)

    # ✅ Feature 11: Rhetorical Question Usage
    rhetorical_questions = sum(1 for s in sentences if "?" in s and "you" in s.lower())

    # ✅ Feature 12: Dialogue Usage
    dialogue_count = text.count('"') // 2  # assumes paired quotes

    # ✅ Feature 13: Vocabulary Richness (Type-Token Ratio)
    unique_word_count = len(set(words_lower))
    type_token_ratio = unique_word_count / (word_count or 1)

    # ✅ Feature 14: Startup-related Keywords Frequency
    startup_vocab = ["startup", "founder", "investor", "hacker", "vc", "venture", "funding"]
    startup_keywords_count = sum(1 for w in words_lower if w in startup_vocab)

    # ✅ Feature 15: Philosophy Keywords Frequency
    philosophy_vocab = ["philosophy", "truth", "meaning", "life", "thought", "mind"]
    philosophy_keywords_count = sum(1 for w in words_lower if w in philosophy_vocab)

    # ✅ Feature 16: Personal Pronouns Ratio
    personal_pronouns = ["i", "we", "my", "our", "us", "me"]
    personal_pronoun_ratio = sum(1 for w in words_lower if w in personal_pronouns) / (word_count or 1)

    # ✅ Feature 17 & 18: Sentiment & Balance
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    sentiment_subjectivity = blob.sentiment.subjectivity

    # ✅ Feature 19: Storytelling Sentences (simplified)
    storytelling_sentences = sum(1 for s in sentences if any(phrase in s.lower() for phrase in ["when i ", "we once", "back then"]))

    # ✅ Feature 20: Passive vs Active Voice Ratio (approx)
    passive_sentences = sum(1 for s in sentences if "was" in s or "were" in s)
    passive_ratio = passive_sentences / (sentence_count or 1)

    # ✅ Feature 21: Direct Advice Sentences
    direct_advice = sum(1 for s in sentences if s.strip().lower().startswith(("you should", "you need to", "if you")))

    # ✅ Feature 22: Sentence Starters Variety
    starters = [s.split()[0].lower() for s in sentences if s.split()]
    starter_variety = len(set(starters)) / (len(starters) or 1)

    # ✅ Feature 23: Parenthesis Usage
    parenthesis_count = text.count('(')

    # ✅ Feature 24: Colon & Semicolon Usage
    colon_semicolon_count = text.count(':') + text.count(';')

    # ✅ Feature 25: List Usage
    list_usage_count = len(re.findall(r'(\n-|\n\d+\.)', text))

    # ✅ Feature 26: Frequency of Connectors
    connectors = ["so", "thus", "however", "therefore", "but", "hence"]
    connector_count = sum(1 for w in words_lower if w in connectors)

    # ✅ Feature 27: Use of Analogies
    analogy_triggers = ["like", "as if", "as though", "similar to"]
    analogy_count = sum(1 for trigger in analogy_triggers if trigger in text.lower())

    # ✅ Feature 28: Uncommon Word Usage (simple)
    uncommon_word_count = sum(1 for w in words_lower if len(w) > 10)

    # ✅ Feature 29: Essay Length in Words
    essay_length = word_count

    # ✅ Feature 30: Ending Pattern
    ending_sentence = sentences[-1] if sentences else ""
    ending_type = "question" if "?" in ending_sentence else "reflection" if "I think" in ending_sentence else "neutral"

    return {
        "essay_title": essay_title,
        "section_headings_count": section_headings_count,
        "num_sentences": num_sentences,
        "avg_sentence_length": avg_sentence_length,
        "first_person_ratio": first_person_ratio,
        "anecdote_count": anecdote_count,
        "question_count": question_count,
        "quote_count": quote_count,
        "metaphor_count": metaphor_count,
        "argument_ratio": argument_ratio,
        "rhetorical_questions": rhetorical_questions,
        "dialogue_count": dialogue_count,
        "type_token_ratio": type_token_ratio,
        "startup_keywords_count": startup_keywords_count,
        "philosophy_keywords_count": philosophy_keywords_count,
        "personal_pronoun_ratio": personal_pronoun_ratio,
        "sentiment_score": sentiment_score,
        "sentiment_subjectivity": sentiment_subjectivity,
        "storytelling_sentences": storytelling_sentences,
        "passive_ratio": passive_ratio,
        "direct_advice": direct_advice,
        "starter_variety": starter_variety,
        "parenthesis_count": parenthesis_count,
        "colon_semicolon_count": colon_semicolon_count,
        "list_usage_count": list_usage_count,
        "connector_count": connector_count,
        "analogy_count": analogy_count,
        "uncommon_word_count": uncommon_word_count,
        "essay_length": essay_length,
        "ending_type": ending_type
    }