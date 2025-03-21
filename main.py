import json
import csv

from page import fetch_page_questions

def main():
    base_url = "https://sprakradet.no/spraksporsmal-og-svar"
    current_url = f"{base_url}/?page=1&kategori=&sok="
    output_csv = 'spraksporsmal.csv'
    output_json = 'spraksporsmal.json'
    all_results = []

    while True:
        print(f"Fetching: {current_url}")
        page_qa, next_url = fetch_page_questions(current_url)

        if not page_qa:
            print("No Q&A blocks found.")
            break
        all_results.extend(page_qa)
        
        if not next_url:
            print("No 'Next' link found. Finished crawling.")
            break
        current_url = next_url
    
    print(f'Number of Q&A entries scraped: {len(all_results)}')
    nynorsk_count = sum(1 for result in all_results if result["lang_type"] == "nno")
    print(f'Number of entries containing the word "nynorsk": {nynorsk_count}')

    # Write to CSV and JSON
    fieldnames = ["title", "question", "answer", "lang_type", "link"]
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in all_results:
            writer.writerow(row)
        print(f'CSV file created: {output_csv}')
    
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f'JSON file created: {output_json}')

if __name__ == "__main__":
    main()