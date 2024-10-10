import pandas as pd

def load_news():
    try:
        df = pd.read_csv("news.csv")
        return df
    except FileNotFoundError:
        print("Error: news.csv file not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: news.csv file is empty.")
        return None
    except Exception as e:
        print(f"An error occurred while loading news.csv: {e}")
        return None

# Load the news data
news_data = load_news()

if news_data is not None:
    print(f"Successfully loaded {len(news_data)} news articles.")
else:
    print("Failed to load news data.")

from dotenv import load_dotenv
import os
import openai

load_dotenv()

def summarize_text(text):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize the following text in 75 words, be concise:\n\n{text}"}
            ],
            max_tokens=150,
            temperature=0.5
        )
        summary = response.choices[0].message['content'].strip()

        return summary
    except Exception as e:
        print(f"An error occurred while summarizing text: {e}")
        return None

# Check if news_data is not None before processing
if news_data is not None:
    # Apply the summarize_text function to the 'article' column and create a new 'summary' column
    news_data['summary'] = news_data['article'].apply(summarize_text)
    
    # Print the first few rows to verify the new column
    print(news_data[['title', 'summary']].head())
    
    # Optionally, save the updated DataFrame back to a CSV file
    news_data.to_csv("news_with_summaries.csv", index=False)
    print("Updated news data with summaries saved to 'news_with_summaries.csv'")
else:
    print("Cannot create summaries: news data is not available.")



