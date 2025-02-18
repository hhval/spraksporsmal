# :norway: Norwegian Language Q&A Web Scraper

This project demonstrates how to scrape question-and-answer entries from [Språkrådet](https://sprakradet.no/), the Language Council of Norway's website. The section [Språkspørsmål og svar](https://sprakradet.no/spraksporsmal-og-svar/) contains over 1000 language questions and answers for Norwegian, with a mix of Bokmål and Nynorsk.  

The primary goals of this project are:

1. **Collect Norwegian data** for further linguistic or data analysis projects.  
2. **Learn web scraping techniques** using Python’s `requests` and `BeautifulSoup` libraries.  
3. **Normalize and store scraped content** in multiple formats (CSV and JSON).

*Important note: This project and the data collection created by the code is for personal learning and private projects, not commercial use. The data from “Språkspørsmål og svar” is owned by Språkrådet.*  

---

## :open_file_folder: Files Overview

There are two main files in this repository:

### `main.py`
- **Purpose**: Handles the overall scraping workflow. It iterates through multiple Q&A pages, collects question–answer pairs, and writes all extracted data to CSV and JSON files.

### `page.py`
- **Purpose**: Contains helper functions for fetching and parsing each Q&A page, as well as normalizing text.
  - **`fetch_page_questions(page_url)`**:  
    Uses `requests` to get the page content and `BeautifulSoup` to parse the HTML, extracting relevant text and cleaning up unneeded elements.
  - **`normalize_text(text)`**:  
    A function that normalizes the scraped text by removing extra whitespace, adjusting punctuation, and generally standardizing the text before saving.

---

## :bulb: Key Features

1. **Pagination Support**  
   Automatically follows “Next” page links until there are no more pages to scrape.

2. **Text Normalization**  
   Cleans and standardizes extracted text by removing extra spaces and adjusting punctuation (via `normalize_text`).

3. **RegEx-Based Cleanup**  
   Uses regular expressions to remove unwanted spacing and punctuation artifacts.

4. **Multiple Output Formats**  
   Generates both a CSV and a JSON file from the scraped data, making it easy to analyze or integrate into other projects.

5. **Language Detection**  
   Checks if the text contains the word “nynorsk” (case-insensitive). Entries containing “nynorsk” are labeled as “nynorsk,” otherwise “bokmål.” Manual check of the data might be needed before use to check for incorrectly labeled entries.

---

## :coffee: Usage

### Install Dependencies:

```bash
pip install requests beautifulsoup4
```

### Run the Script:

```bash
python main.py
```

This will:

- Begin scraping from the first Q&A page.
- Follow pagination links.
- Collect Q&A entries into an in-memory list.
- Save the results to `spraksporsmal.csv` and `spraksporsmal.json`.

---

## :white_check_mark: Check the Output

- **`spraksporsmal.csv`**: A comma-separated file containing link, title, question, answer, and language type.  
- **`spraksporsmal.json`**: A structured JSON file with the same data fields as the CSV.

---

## :star: Purpose of Data Collection

Gather Norwegian language Q&A data (e.g., questions about grammar, usage, etc.) for further experiments, language projects, or simply as a learning exercise for data scraping, text normalization, and data storage in different formats.