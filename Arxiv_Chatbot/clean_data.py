import pandas as pd

def clean_massive_dataset(input_file, output_file, chunk_size=100000):
    print(f"Starting memory-safe cleaning of {input_file}...")
    chunk_iterator = pd.read_csv(input_file, chunksize=chunk_size)

    first_chunk = True
    total_original = 0
    total_cleaned = 0

    target_pattern = r'(^|\s)cs\.'

    for chunk in chunk_iterator:
        total_original += len(chunk)
        
        cleaned_chunk = chunk[chunk['categories'].str.contains(target_pattern, na=False, regex=True)]
        total_cleaned += len(cleaned_chunk)
        
        if first_chunk:
            cleaned_chunk.to_csv(output_file, index=False, mode='w')
            first_chunk = False
        else:
            cleaned_chunk.to_csv(output_file, index=False, mode='a', header=False)
            
        print(f"Scanned {total_original:,} rows... Kept {total_cleaned:,} valid CS papers.")

    print("\n--- Cleaning Complete ---")
    print(f"Original rows: {total_original:,}")
    print(f"Strict CS rows: {total_cleaned:,}")
    print(f"Removed {total_original - total_cleaned:,} non-CS papers.")
    print(f"Clean dataset saved to {output_file}!")


INPUT = 'all_cs_papers.csv'
OUTPUT = 'all_cs_papers_strict.csv' 

clean_massive_dataset(INPUT, OUTPUT)