import subprocess
import json
import os
from tqdm import tqdm
import time

# Get the absolute path to the project root
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this script
output_dir = os.path.join(script_dir, "../../data/youtube")  # Target directory
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Path to cookies file
cookies_file = os.path.join(script_dir, "cookies.txt")  # Ensure cookies.txt is in the same directory as the script
if not os.path.exists(cookies_file):
    print(f"❌ Cookies file not found at {cookies_file}. Please export your YouTube cookies.")
    exit(1)

# Load video IDs from the JSON file
video_ids_file = os.path.join(output_dir, "video_ids.json")  # Path to video_ids.json
with open(video_ids_file, "r") as f:
    video_ids = json.load(f)

# Fetch metadata for each video
metadata = []
print("🔍 Fetching metadata for videos...")
with tqdm(total=len(video_ids), desc="Processing videos", unit="video") as pbar:
    for video_id in video_ids:
        retries = 3  # Number of retries for each video
        for attempt in range(retries):
            command = f'yt-dlp --skip-download --cookies "{cookies_file}" --print-json "https://www.youtube.com/watch?v={video_id}"'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                try:
                    data = json.loads(result.stdout)
                    metadata.append({
                        "id": video_id,
                        "title": data.get("title"),
                        "description": data.get("description"),
                        "uploader": data.get("uploader"),
                        "url": f"https://www.youtube.com/watch?v={video_id}"
                    })
                    break  # Exit retry loop on success
                except json.JSONDecodeError:
                    print(f"⚠️ Warning: Failed to parse metadata for video ID {video_id}.")
            else:
                print(f"❌ Error fetching metadata for video ID {video_id} (Attempt {attempt + 1}/{retries}).")
                print(f"Error: {result.stderr.strip()}")  # Log the error message
                if attempt < retries - 1:
                    time.sleep(2)  # Wait before retrying
        else:
            print(f"❌ Failed to fetch metadata for video ID {video_id} after {retries} attempts.")
        pbar.update(1)

# Save metadata to a JSON file in the same directory
metadata_file = os.path.join(output_dir, "video_metadata.json")  # Path to video_metadata.json
with open(metadata_file, "w") as f:
    json.dump(metadata, f, indent=4)

print(f"✅ Fetched metadata for {len(metadata)} videos and saved to '{metadata_file}'.")