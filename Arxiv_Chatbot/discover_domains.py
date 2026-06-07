import json
from collections import Counter

def analyze_domains(input_filename):
    domains_counts = Counter()
    lines_processed = 0

    print("Scanning dataset to discover domains. This may take a few minutes...")

    with open(input_filename, 'r', encoding = 'utf-8') as file:
        for line in file:
            lines_processed += 1

            paper = json.loads(line)

            categories_string = paper.get('categories', '')
            categories_list = categories_string.split()

            for cat in categories_list:
                major_domain = cat.split('.')[0]
                domains_counts[major_domain] += 1

                if lines_processed % 500000 == 0:
                    print(f"Scanned {lines_processed} lines...")
    
    print("\n--- Domain Discovery Complete ---")
    print(f"Total papers scanned: {lines_processed}\n")
    
    print("Found the following major domains:")
    print("-" * 40)

    for domain, count in domains_counts.most_common():
        print(f"{domain:<15} | {count:,} tags")

INPUT_FILE = 'arxiv-metadata-oai-snapshot.json'
analyze_domains(INPUT_FILE)