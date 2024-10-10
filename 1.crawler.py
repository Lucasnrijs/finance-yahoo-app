import requests
from bs4 import BeautifulSoup
import time
from utils import extract_main_text
import pandas as pd

def crawl_yahoo_finance_news():
    url = "https://finance.yahoo.com/news/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        news_items = soup.find_all('a', class_='subtle-link fin-size-small titles noUnderline yf-1e4diqp')
        
        df = pd.DataFrame(columns=["Title", "Link", "Article"])
        for item in news_items:
            title = item.get('title')
            link_tag = item.get('href')
            full_article = extract_main_text(link_tag)
            limited_article = full_article[:100]
            if title is not None:
                print(f"Title: {title}")
            if link_tag is not None:
                print(f"Link: {link_tag}")
                print(f"Article: {limited_article}")
            else:
                print("No link tag found in item.")
            print("---")
            data = {
                "title": [title],
                "link": [link_tag],
                "article": [full_article]
            }
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv("news.csv", index=False)
        time.sleep(1)  # Be respectful to the server

    except requests.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    crawl_yahoo_finance_news()
