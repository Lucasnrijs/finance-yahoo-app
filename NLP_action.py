from flask import Flask, request, jsonify, render_template
from llama_index.core import Document, VectorStoreIndex
from llama_index.core.node_parser import SimpleNodeParser
import json
import tiktoken
import openai
import os
import requests

app = Flask(__name__)
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Check if the API key is set
if not openai.api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

def get_text_nodes(json_data):
    text_nodes = []
    for key, value in json_data.items():
        if isinstance(value, str):
            text_nodes.append(Document(text=f"{key}: {value}", extra_info={"key": key}))
        elif isinstance(value, (dict, list)):
            text_nodes.append(Document(text=f"{key}: {json.dumps(value, indent=2)}", extra_info={"key": key}))
    return text_nodes

def summarize_text_nodes(text_nodes, max_tokens=8000):
    summarized_nodes = []
    current_tokens = 0
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    for node in text_nodes:
        node_tokens = len(encoding.encode(node.text))
        if current_tokens + node_tokens > max_tokens:
            break
        summarized_nodes.append(node)
        current_tokens += node_tokens

    return summarized_nodes, current_tokens

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stock-analysis-US/<symbol>', methods=['GET'])
def get_stock_analysis(symbol):
    try:
        analysis_url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-analysis"
        params = {
            "symbol": symbol,
            "region": "US"
        }
        
        # Define headers directly in the code
        headers = {
            "X-RapidAPI-Key": "48a2b57d07mshc303b2f74b3c0c0p1996b8jsnfe9e45101fa7",
            "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }
        
        response = requests.get(analysis_url, headers=headers, params=params)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"API request failed with status code {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stock-analysis-US', methods=['POST'])
def stock_analysis():
    data = request.json
    if not data or 'symbol' not in data or 'query' not in data:
        return jsonify({"error": "Missing stock symbol or query"}), 400

    symbol = data['symbol']
    custom_query = data['query']
    
    # Fetch the stock data for the given symbol using the get_stock_analysis function
    stock_data = get_stock_analysis(symbol)
    if isinstance(stock_data, tuple):  # Error occurred
        return stock_data
    
    text_nodes = get_text_nodes(stock_data.json)
    summarized_nodes, total_tokens = summarize_text_nodes(text_nodes)

    # Create a LlamaIndex from the summarized nodes
    parser = SimpleNodeParser()
    nodes = parser.get_nodes_from_documents(text_nodes)
    index = VectorStoreIndex(nodes)
    query_engine = index.as_query_engine(
        similarity_top_k=5
    )

    # Perform analysis using LlamaIndex
    response = query_engine.query(custom_query)

    return jsonify({
        "symbol": symbol,
        "analysis": response.response,
        "total_tokens": total_tokens
    })
import pandas as pd

@app.route('/', methods=['GET'])
def landing_page():
    try:
        # Read the CSV file with generated questions and answers
        df = pd.read_csv("generated_questions_with_answers.csv")
        
        # Convert the DataFrame to a list of dictionaries
        questions = df[['question', 'answer']].to_dict('records')
        
        # Format the questions with a unique id, question, hidden answer, and toggle state
        formatted_questions = [
            {
                "id": idx,
                "question": q['question'],
                "answer": q['answer'],
                "news_title": q['news_title'],
                "show_answer": False
            } for idx, q in enumerate(questions)
        ]
        
        return jsonify({"questions": formatted_questions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/toggle-answer/<int:question_id>', methods=['POST'])
def toggle_answer_question(question_id):
    try:
        # Read the CSV file to get the current state
        df = pd.read_csv("generated_questions_with_answers.csv")
        
        if question_id < 0 or question_id >= len(df):
            return jsonify({"error": "Invalid question id"}), 400
        
        # Toggle the show_answer state
        new_state = not df.at[question_id, 'show_answer'] if 'show_answer' in df.columns else True
        
        # Update the DataFrame
        if 'show_answer' not in df.columns:
            df['show_answer'] = False
        df.at[question_id, 'show_answer'] = new_state
        
        # Save the updated DataFrame back to the CSV
        df.to_csv("generated_questions_with_answers.csv", index=False)
        
        # Get the news_title for the toggled question
        news_title = df.at[question_id, 'news_title']
        
        return jsonify({
            "id": question_id,
            "show_answer": new_state,
            "news_title": news_title
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-news-articles', methods=['GET'])
def get_news_articles():
    try:
        # Read the CSV file with generated questions and answers
        df = pd.read_csv("generated_questions_with_answers.csv")
        
        # Ensure 'show_answer' column exists
        if 'show_answer' not in df.columns:
            df['show_answer'] = False
        
        # Convert the DataFrame to a list of dictionaries
        articles = df.to_dict('records')
        
        # Format the articles with a question, answer, and showAnswer state
        formatted_articles = [
            {
                "id": idx,
                "question": article.get('question', ''),
                "answer": article.get('answer', ''),
                "summary": article.get('summary', ''),
                "showAnswer": bool(article.get('show_answer', False))
            } for idx, article in enumerate(articles)
        ]
        
        if not formatted_articles:
            return jsonify({"error": "No articles found"}), 404
        
        # Debug print to check the content of formatted_articles
        print("Formatted articles:", formatted_articles)
        
        return jsonify({"articles": formatted_articles})
    except Exception as e:
        print(f"Error in get_news_articles: {str(e)}")  # Debug print
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/toggle-answer-article/<int:article_id>', methods=['POST'])
def toggle_answer_article(article_id):
    try:
        data = request.json
        show_answer = data.get('showAnswer', False)

        # Read the CSV file
        df = pd.read_csv("generated_questions_with_answers.csv")
        
        if article_id < 0 or article_id >= len(df):
            return jsonify({"error": "Invalid article id"}), 400
        
        # Update the show_answer state
        if 'show_answer' not in df.columns:
            df['show_answer'] = False
        df.at[article_id, 'show_answer'] = show_answer
        
        # Save the updated DataFrame back to the CSV
        df.to_csv("generated_questions_with_answers.csv", index=False)
        
        # Get the news_title for the toggled article
        summary = df.at[article_id, 'summary']
        
        return jsonify({
            "id": article_id,
            "showAnswer": show_answer,
            "summary": summary
        })
    except Exception as e:
        print(f"Error in toggle_answer_article: {str(e)}")  # Debug print
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True)