import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def fetch_transcript(url):
    """Fetch transcript text from a given URL"""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract text (this may need adjustment per website)
        paragraphs = soup.find_all("p")
        transcript = "\n".join([p.get_text() for p in paragraphs])
        return transcript.strip()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# List of URLs with transcripts
urls = [
    "https://conversationswithtyler.com/episodes/paul-graham/",
    "https://www.listennotes.com/podcasts/founders/275-paul-graham-GRaADbYdql1/",
    "https://smashnotes.com/p/econtalk-archives-2009/e/graham-on-start-ups-innovation-and-creativity",
    "https://mixergy.com/interviews/y-combinator-paul-graham/",
    "https://americansuburbx.com/2010/07/interview-paul-graham-with-richard.html",
    "https://www.paulgraham.com/wids.html",
    "https://www.paulgraham.com/frinterview.html",
    "https://joincolossus.com/episode/senra-paul-graham-how-to-do-great-work/",
    "https://www.wondercraft.ai/studio/e/dHyZwCg2",
    "https://pier24.org/pilarafoundation/wp-content/uploads/2015/09/paul_graham_interview.pdf",
    # Additional podcast links
    "https://www.ferrisspodcast.com/paul-graham",
    "https://www.entrepreneur.com/article/411493",
    "https://www.acquired.fm/episodes/paul-graham-founder-of-y-combinator",
    "https://lexfridman.com/paul-graham/",
    "https://mastersofscale.com/paul-graham/",
    "https://www.startupschool.org/episodes/paul-graham-interview",
    "https://www.recode.net/2015/5/5/11647334/paul-graham",
    "https://www.thetimferrissshow.com/podcast/paul-graham",
    "https://www.a16z.com/2017/10/23/paul-graham-ycombinator-qa/",
    "https://www.theknowledgeproject.com/podcast/paul-graham"
]

# Get the absolute path to the project root
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this script
output_dir = os.path.join(script_dir, "../../data/podcasts")  # Target directory
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Directory to save individual transcripts
transcripts_dir = os.path.join(output_dir, "transcripts")
os.makedirs(transcripts_dir, exist_ok=True)

# Fetch and save transcripts
for url in tqdm(urls, desc="Downloading Transcripts", unit="file"):
    transcript = fetch_transcript(url)
    if transcript:
        filename = url.split("/")[-2] + ".txt"
        filepath = os.path.join(transcripts_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(transcript)

# Combine all transcripts into one file
combined_filepath = os.path.join(output_dir, "all_transcripts.txt")
with open(combined_filepath, "w", encoding="utf-8") as outfile:
    for file in os.listdir(transcripts_dir):
        with open(os.path.join(transcripts_dir, file), "r", encoding="utf-8") as infile:
            outfile.write(infile.read() + "\n\n")

print(f"✅ All transcripts saved in {combined_filepath}")
