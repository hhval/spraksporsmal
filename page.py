import requests
from requests.exceptions import RequestException
import re
from bs4 import BeautifulSoup

def normalize_text(text: str) -> str:
    """Normalize text by removing extra whitespace and adjusting punctuation."""
    # Convert multiple spaces, tabs, and line breaks into one space
    text = ' '.join(text.split())
    
    # Remove any extra space before punctuation like , . : ; ? !
    text = re.sub(r'\s+([,.:;?!\)])', r'\1', text)
    
    # Remove extra whitespace after an opening parenthesis '('
    text = re.sub(r'\(\s+', '(', text)
    
    return text

def fetch_page_questions(page_url):
    """
    Fetch questions and answers from a given Språkrådet Q&A page.
    
    :param page_url: URL of the Q&A page
    :return: A tuple (list of questions, URL of next_page)
    """
    try:
        response = requests.get(page_url, timeout=10)
        response.raise_for_status()  # Raises HTTPError if status code is 4xx/5xx
    except RequestException as e:
        print(f"An error occurred while fetching {page_url}: {e}")
        return [], ""  # Return empty results and no next link

    soup = BeautifulSoup(response.text, "html.parser")
    question_dropdowns = soup.find_all("div", class_="question-dropdown")
    results = []
   
    for qd in question_dropdowns:
        # 1) Get link + title
        link_tag = qd.select_one("h2.font-step-1 > a")
        if not link_tag:
            continue    
        link = link_tag.get("href", "")
        title_raw = link_tag.get_text(strip=True)

        # 2) Get question text from <div class="question-content">
        question_div = qd.select_one("div.question-content")
        question_raw = question_div.get_text(separator=" ", strip=True) if question_div else ""

        # 3) Get answer text from <div class="answer-content">
        answer_div = qd.select_one("div.answer-content")
        if answer_div is not None:
            # Remove <h2 class="answer-title">
            heading = answer_div.select_one("h2.answer-title")
            if heading is not None:
                heading.decompose()            
            # Remove <div class="terms-expand">
            terms_expand = answer_div.select_one("div.terms-expand")
            if terms_expand is not None:
                terms_expand.decompose()
            # Extract the text from the pruned <div>
            answer_raw = answer_div.get_text(separator=" ", strip=True)
 
        # 4) Normalize each text field
        title_text = normalize_text(title_raw)
        question_text = normalize_text(question_raw)
        answer_text = normalize_text(answer_raw)

        # 5) Check for 'nynorsk' (case-insensitive) in title, question, or answer
        combined_text = f"{title_text} {question_text} {answer_text}".lower()
        if "nynorsk" in combined_text:
            lang_type = "nno"
        else:
            lang_type = "nob"

        results.append({
            "title": title_text,
            "question": question_text,
            "answer": answer_text,
            "lang_type": lang_type,
            "link": link,
        })
        
    # Get link for next page
    next_li = soup.select_one("li.next.btn a[href]")
    if next_li:
        next_href = next_li.get("href").replace(
            "https://sprakradet.no/?",
            "https://sprakradet.no/spraksporsmal-og-svar/?"
        )
    else:
        next_href = ""

    return results, next_href