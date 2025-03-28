# src/dataset_builder.py

import os
import json
import csv
from tqdm import tqdm
from extract_features import extract_features

# --- Config ---

INPUT_DIR = "../data/essays"  # path to the essays directory
OUTPUT_DIR = "../dataset"    # Adjusted output directory to match project structure
CSV_OUTPUT = os.path.join(OUTPUT_DIR, "essays_dataset.csv")
JSON_OUTPUT = os.path.join(OUTPUT_DIR, "essays_dataset.json")

# --- Prepare ---
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Read essays ---
essay_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".txt")]
dataset = []

print(f"Found {len(essay_files)} essays.")

# --- Process essays ---
for fname in tqdm(essay_files, desc="Extracting features"):
    with open(os.path.join(INPUT_DIR, fname), "r", encoding="utf-8") as f:
        text = f.read()

    title = os.path.splitext(fname)[0]
    features = extract_features(text, title=title)
    dataset.append(features)

# --- Save CSV ---
print("Saving CSV...")
with open(CSV_OUTPUT, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=dataset[0].keys())
    writer.writeheader()
    writer.writerows(dataset)

# --- Save JSON ---
print("Saving JSON...")
with open(JSON_OUTPUT, "w", encoding="utf-8") as jsonfile:
    json.dump(dataset, jsonfile, indent=2, ensure_ascii=False)

print(f"\n✅ Dataset ready! Saved to {OUTPUT_DIR}/")
