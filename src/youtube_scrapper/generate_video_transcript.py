import json
import time
import os
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from tqdm import tqdm

# Get the absolute path to the project root
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this script
output_dir = os.path.join(script_dir, "../../data/youtube")  # Target directory
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Load video IDs
video_ids_file = os.path.join(output_dir, "video_ids.json")  # Path to video_ids.json
if not os.path.exists(video_ids_file):
    print(f"❌ Error: video_ids.json not found in {output_dir}. Please ensure the file exists.")
    exit(1)

with open(video_ids_file, "r") as f:
    video_ids = json.load(f)

transcripts = {}

try:
    # Loop through video IDs with progress bar
    for video_id in tqdm(video_ids, desc="Extracting Transcripts"):
        try:
            # Fetch transcript
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
            # Convert to plain text
            transcript_text = "\n".join([entry["text"] for entry in transcript_data])
            # Store transcript
            transcripts[video_id] = transcript_text
        except TranscriptsDisabled:
            print(f"⚠️ Transcripts are disabled for video ID {video_id}. Skipping...")
        except NoTranscriptFound:
            print(f"⚠️ No transcript found for video ID {video_id}. Skipping...")
        except Exception as e:
            print(f"⚠️ Skipping video ID {video_id} due to an unexpected error: {e}")
        # Respect YouTube API limits
        time.sleep(2)
except KeyboardInterrupt:
    print("\n⏹️ Script interrupted. Saving progress...")
finally:
    # Save transcripts to JSON file in the correct directory
    transcripts_file = os.path.join(output_dir, "paul_graham_transcripts.json")
    with open(transcripts_file, "w") as f:
        json.dump(transcripts, f, indent=4)
    print(f"✅ Progress saved! Extracted {len(transcripts)} transcripts so far.")