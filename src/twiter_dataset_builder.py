import os
import re
import json
import csv
from textblob import TextBlob
from collections import Counter
import nltk
from tqdm import tqdm  # Import tqdm for progress bar

nltk.download('punkt')

def extract_tweet_features(tweet, hashtags=[], keywords=[]):
    # --- Preprocessing ---
    words = nltk.word_tokenize(tweet)
    word_count = len(words)
    sentences = nltk.sent_tokenize(tweet)
    sentence_count = len(sentences)

    # Feature 1: Length of Tweet (words, characters)
    tweet_length = {
        "word_count": word_count,
        "char_count": len(tweet)
    }

    # Feature 2: Sentiment Analysis
    sentiment = TextBlob(tweet).sentiment
    sentiment_score = sentiment.polarity  # Positive or negative score

    # Feature 3: Question Ratio
    question_count = sum(1 for s in sentences if '?' in s)
    question_ratio = question_count / (sentence_count or 1)

    # Feature 4: First Person Pronouns Ratio
    first_person_pronouns = ['i', 'we']
    first_person_count = sum(1 for word in words if word.lower() in first_person_pronouns)
    first_person_ratio = first_person_count / (word_count or 1)

    # Feature 5: Complex Word Ratio
    complex_words = [word for word in words if len(word) > 10]  # Words longer than 10 characters
    complex_word_ratio = len(complex_words) / (word_count or 1)

    # Feature 6: Connector Words Count
    connectors = ["so", "therefore", "however", "but", "thus"]
    connector_count = sum(1 for word in words if word.lower() in connectors)

    # Feature 7: Metaphor Count
    metaphor_triggers = ["like", "as if", "as though", "similar to", "imagine"]
    metaphor_count = sum(1 for trigger in metaphor_triggers if trigger in tweet.lower())

    # Feature 8: Analogy Count
    analogy_triggers = ["like", "as if", "similar to"]
    analogy_count = sum(1 for trigger in analogy_triggers if trigger in tweet.lower())

    # Feature 9: Hashtag Count
    hashtag_count = len(re.findall(r"#\w+", tweet))

    # Feature 10: Keywords Count (e.g., Paul Graham's topics)
    keywords_count = sum(1 for word in words if word.lower() in keywords)

    # Feature 11: Tone (simple classification: e.g., philosophical, reflective, assertive)
    tone = "neutral"  # Simple tone detection, could use NLP techniques to classify more accurately
    if "philosophy" in tweet.lower():
        tone = "philosophical"
    elif "action" in tweet.lower() or "should" in tweet.lower():
        tone = "assertive"
    elif "think" in tweet.lower():
        tone = "reflective"

    return {
        "tweet_text": tweet,
        "tweet_length_word_count": tweet_length["word_count"],
        "tweet_length_char_count": tweet_length["char_count"],
        "sentiment_score": sentiment_score,
        "question_ratio": question_ratio,
        "first_person_ratio": first_person_ratio,
        "complex_word_ratio": complex_word_ratio,
        "connector_count": connector_count,
        "metaphor_count": metaphor_count,
        "analogy_count": analogy_count,
        "hashtag_count": hashtag_count,
        "keywords_count": keywords_count,
        "tone": tone
    }

# --- Dataset Preparation ---
def prepare_tweet_dataset(tweet_data, output_dir="../dataset"):
    dataset = []
    paul_keywords = ["startup", "investor", "venture", "growth", "philosophy", "thinking"]  # Define keywords

    # Use tqdm to show progress
    with tqdm(total=len(tweet_data), desc="Processing tweets", unit="tweet") as pbar:
        for tweet in tweet_data:
            features = extract_tweet_features(tweet['content'], keywords=paul_keywords)
            dataset.append(features)
            pbar.update(1)  # Update progress bar

    # Save the dataset as JSON
    os.makedirs(output_dir, exist_ok=True)
    json_file_path = os.path.join(output_dir, "tweets_dataset.json")
    with open(json_file_path, "w", encoding="utf-8") as jsonfile:
        json.dump(dataset, jsonfile, indent=2, ensure_ascii=False)
    print(f"✅ Dataset saved as JSON at {json_file_path}")

    # Save the dataset as CSV
    csv_file_path = os.path.join(output_dir, "tweets_dataset.csv")
    with open(csv_file_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=dataset[0].keys())
        writer.writeheader()
        writer.writerows(dataset)
    print(f"✅ Dataset saved as CSV at {csv_file_path}")

# Example usage
if __name__ == "__main__":
    # Load tweet data from a JSON file (replace with your actual tweet data file)
    with open("../data/tweets/twitter.json", "r", encoding="utf-8") as f:
        tweet_data = json.load(f)

    # Prepare the dataset
    prepare_tweet_dataset(tweet_data)