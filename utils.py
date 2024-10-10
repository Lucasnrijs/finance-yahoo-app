import requests
from bs4 import BeautifulSoup
import copy
# List of URLs to process
urls = [
    "https://finance.yahoo.com/news/ask-advisor-spouse-dies-full-100000535.html",
    "https://finance.yahoo.com/news/1-vanguard-index-fund-could-084400540.html",
    "https://finance.yahoo.com/news/want-millionaire-stop-doing-9-164523481.html",
    "https://finance.yahoo.com/news/unfortunate-truth-claiming-social-security-141500632.html"
]

def extract_main_text(url):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Attempt to find the main content
        # This is a generic example; you may need to adjust the selectors based on the actual HTML structure
        main_content = soup.find('div', class_='caas-body')  # Example class name, adjust as needed

        if main_content:
            # Extract and return the text
            return main_content.get_text(separator='\n', strip=True)
        else:
            return "Main content not found."

    except requests.RequestException as e:
        return f"Error fetching {url}: {e}"

# Process each URL
def get_confident_objects(objects_for_question):
  for object in objects_for_question.copy():
    if object['score'] < 0.99:
      objects_for_question.remove(object)


  return objects_for_question

#this loops over the list in reverse order
def get_answers(objects_for_question):
  copy_of_objects = copy.deepcopy(objects_for_question)

  list_of_final_words = []
  for i in range(len(copy_of_objects)-1, -1, -1):
    if (copy_of_objects[i]['word'].find('▁')) != 0:
      part_to_append = copy_of_objects[i]['word']
      #print(part_to_append)
      copy_of_objects[i-1]['word'] = copy_of_objects[i-1]['word'] + part_to_append
      #print('true')
    else:
      list_of_final_words.append(copy_of_objects[i]['word'].replace('▁', ''))
  return list_of_final_words


