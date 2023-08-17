import requests
from bs4 import BeautifulSoup
import spacy
from collections import Counter

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

def extract_keywords_from_content(content):
    doc = nlp(content)
    keywords = []

    for token in doc:
        if not token.is_stop and not token.is_punct and not token.is_space:
            keywords.append(token.text)

    return keywords

def main():
    while True:
        webpage_url = input("Enter the webpage address: ")
        
        if not webpage_url:
            print("Exiting the program.")
            break
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(webpage_url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.get_text()
            
            keywords = extract_keywords_from_content(content)
            
            keyword_counter = Counter(keywords)
            top_keywords = [keyword for keyword, _ in keyword_counter.most_common(20)]  # Get top 20 keywords
            
            with open('spotted.txt', 'a', encoding='utf-8') as file:
                file.write(f"Keywords extracted from {webpage_url}:\n")
                file.write(", ".join(top_keywords))  # Join keywords with comma
                file.write("\n" + "=" * 40 + "\n")
            
            print(f"Top SEO keywords extracted from {webpage_url} and saved to 'spotted.txt'.")
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)

if __name__ == "__main__":
    main()
