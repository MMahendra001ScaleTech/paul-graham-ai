import os
import requests
import json
import time
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the Bearer Token from the environment variable
BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

# Ensure the token is found
if BEARER_TOKEN is None:
    raise ValueError("Bearer token not found. Please set it in the .env file.")

# User information and limits
USERNAME = "paulg"  # Replace with the username you're interested in
TWEET_LIMIT = 99  # Number of tweets you want to scrape

# API URL for getting user tweets
BASE_URL = "https://api.twitter.com/2"

# Set headers
headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "User-Agent": "v2UserTweetsPython"
}

# Output directory and file
DATA_DIR = "../data/tweets"
OUTPUT_FILE = os.path.join(DATA_DIR, f"{USERNAME}_tweets.json")

def get_user_id(username):
    """Function to get user ID from the username with retry logic"""
    url = f"{BASE_URL}/users/by/username/{username}"
    retries = 5  # Number of retries
    delay = 15  # Delay in seconds between retries

    for attempt in range(retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            return user_data['data']['id']
        elif response.status_code == 429:
            print(f"❌ Rate limit reached. Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
            time.sleep(delay)
        else:
            print(f"❌ Error retrieving user ID: {response.status_code} - {response.text}")
            break

    print("❌ Failed to retrieve user ID after multiple attempts.")
    return None

def fetch_tweets(user_id, tweet_limit):
    """Function to fetch tweets of a user by user ID"""
    tweets_list = []
    url = f"{BASE_URL}/users/{user_id}/tweets"
    params = {
        "max_results": 100,  # Twitter API allows a max of 100 tweets per request
        "tweet.fields": "created_at,public_metrics",  # Fields to fetch for each tweet
    }

    try:
        while len(tweets_list) < tweet_limit:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                tweets = data.get("data", [])
                tweets_list.extend(tweets)

                # Check if there's a next_token for pagination
                meta = data.get("meta", {})
                if "next_token" in meta:
                    params["pagination_token"] = meta["next_token"]
                else:
                    break  # No more tweets to fetch
            elif response.status_code == 429:
                print("❌ Rate limit reached. Retrying after 15 seconds...")
                time.sleep(15)  # Wait before retrying
            else:
                print(f"❌ Error fetching tweets: {response.status_code} - {response.text}")
                break

        # Save tweets to a JSON file
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(tweets_list, f, indent=4)

        print(f"✅ Successfully fetched {len(tweets_list)} tweets and saved to {OUTPUT_FILE}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print(f"🚀 Fetching tweets for user: {USERNAME}")
    user_id = get_user_id(USERNAME)
    if user_id:
        fetch_tweets(user_id, TWEET_LIMIT)