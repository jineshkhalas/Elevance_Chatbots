import pandas as pd
import json

def extract_all_cs_papers(input_filename, output_filename, target_domain='cs.'):
    """
    Streams the entire dataset and extracts EVERY paper containing the target domain.
    """
    filtered_papers = []
    lines_processed = 0
    
    print(f"Starting FULL extraction for '{target_domain}' papers. This will take a few minutes...")

    with open(input_filename, 'r', encoding='utf-8') as file:
        for line in file:
            lines_processed += 1
            paper = json.loads(line)
            categories = paper.get('categories', '')
            
            # If 'cs.' is in the categories, save the relevant data
            if target_domain in categories:
                filtered_papers.append({
                    'id': paper.get('id'),
                    'title': paper.get('title'),
                    'abstract': paper.get('abstract'), 
                    'categories': categories
                })
                
                # Print progress every 50,000 papers so we know it hasn't crashed
                if len(filtered_papers) % 50000 == 0:
                    print(f"Extracted {len(filtered_papers):,} CS papers so far...")

    print(f"\nFinished scanning {lines_processed:,} total lines.")
    print(f"Total CS papers found: {len(filtered_papers):,}")
    
    print("Saving to CSV... (This might take a minute due to the massive size)")
    # Save to a new CSV file specifically for the full dataset
    df = pd.DataFrame(filtered_papers)
    df.to_csv(output_filename, index=False)
    print(f"Success! Full dataset saved to {output_filename}")

# --- Execution ---
INPUT_FILE = 'arxiv-metadata-oai-snapshot.json'
OUTPUT_FILE = 'all_cs_papers.csv' # Changed filename so we don't overwrite the small one

extract_all_cs_papers(INPUT_FILE, OUTPUT_FILE)