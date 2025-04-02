import subprocess
import json
import os
from tqdm import tqdm  # Import tqdm for progress bar

# Search query
query = "Paul Graham Talk"
max_results = 1000  # Number of videos to fetch

# Step 1: Search YouTube using yt-dlp (metadata only, no downloads)
print(f"🔍 Searching YouTube for up to {max_results} videos (metadata only, no downloads)...")
command = f'yt-dlp --flat-playlist "ytsearch{max_results}:{query}" --print-json'  # Fetch metadata only
result = subprocess.run(command, shell=True, capture_output=True, text=True)

# Check if the command executed successfully
if result.returncode != 0:
    print("❌ Error: Failed to execute yt-dlp command.")
    print(result.stderr)
    exit(1)

# Step 2: Parse JSON output
video_ids = []
lines = result.stdout.strip().split("\n")

print(f"📄 Found {len(lines)} results. Extracting video IDs...")
with tqdm(total=len(lines), desc="Processing videos", unit="video") as pbar:
    for line in lines:
        try:
            data = json.loads(line)  # Parse each line as JSON
            video_ids.append(data["id"])  # Extract video ID
        except json.JSONDecodeError:
            print("⚠️ Warning: Failed to parse a line of JSON.")
        pbar.update(1)  # Update progress bar

# Step 3: Save video IDs to a JSON file in the correct directory
# Get the absolute path to the project root
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this script
output_dir = os.path.join(script_dir, "../../data/youtube")  # Target directory
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
output_file = os.path.join(output_dir, "video_ids.json")

with open(output_file, "w") as f:
    json.dump(video_ids, f, indent=4)

print(f"✅ Successfully fetched {len(video_ids)} YouTube video IDs and saved to {output_file}!")