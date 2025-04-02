import json
import os

# Get the absolute path to the project root
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this script
output_dir = os.path.join(script_dir, "../../data/youtube")  # Target directory
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Load video IDs from the JSON file
video_ids_file = os.path.join(output_dir, "video_ids.json")  # Path to video_ids.json
with open(video_ids_file, "r") as f:
    video_ids = json.load(f)

# Construct YouTube URLs
youtube_urls = [f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids]

# Save the URLs to a file in the same directory
video_urls_file = os.path.join(output_dir, "video_urls.txt")  # Path to video_urls.txt
with open(video_urls_file, "w") as f:
    f.write("\n".join(youtube_urls))

print(f"✅ Generated {len(youtube_urls)} YouTube URLs and saved to '{video_urls_file}'.")