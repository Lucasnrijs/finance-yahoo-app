from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from utils import get_confident_objects, get_answers
import copy


tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-large-finetuned-conll03-english")

model = AutoModelForTokenClassification.from_pretrained("xlm-roberta-large-finetuned-conll03-english")

import pandas as pd

# Load the news data with summaries
news_data = pd.read_csv("news_with_summaries.csv")

# Display the first few rows to verify the data
print(news_data.head())

# Print some basic information about the dataset
print(news_data.info())

classifier = pipeline("ner", model=model, tokenizer=tokenizer)
def get_df_from_post_titles(list_of_post_titles):
    df = pd.DataFrame(columns = ['answer','summary', 'subject_number'])
    i = 0
    for context in list_of_post_titles:
        #get the different objects from the classifier
        objects_for_question = classifier(context)

        confident_objects = get_confident_objects(objects_for_question)

        answers = get_answers(confident_objects)
        i +=1


        for answer in answers:
            list_to_append = []
            list_to_append.append(answer)
            list_to_append.append(context)
            list_to_append.append(i)
            df.loc[len(df)] = list_to_append

    return df

df = get_df_from_post_titles(news_data['summary'])

# Perform a left join of df with news_data on the 'summary' column
df = df.merge(news_data[['summary', 'title', 'article']], on='summary', how='left')

# Rename columns for clarity
df = df.rename(columns={'title': 'news_title', 'article': 'full_article'})

# Reorder columns for better readability
df = df[['answer', 'summary', 'subject_number', 'news_title', 'full_article']]

# Display the first few rows of the merged DataFrame
print(df.head())

# Print information about the merged DataFrame
print(df.info())

# Write the DataFrame to a CSV file
output_file = "generated_answers.csv"
df.to_csv(output_file, index=False)
print(f"Generated answers have been saved to {output_file}")

import nltk
from nltk.corpus import stopwords