import nltk
from nltk.corpus import stopwords

import pandas as pd

# Read the generated questions CSV file
df = pd.read_csv("generated_answers.csv")

# Display the first few rows to verify the data
print(df.head())

# Print some basic information about the dataset
print(df.info())

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Create a boolean mask indicating if the answer is a stop word
mask = df['answer'].apply(lambda x: x.lower() in stop_words)

# Drop the rows where the answer is a stop word
df = df[~mask]

print(df.info())

# Drop duplicate rows based on all columns
df = df.drop_duplicates()

# Print updated information about the dataset after removing duplicates
print("Dataset information after removing duplicates:")
print(df.info())

df['list_of_words'] = df['summary'].apply(lambda x: x.split(f' '))
def check_position_difference(df):
    df['position'] = df.apply(lambda x: x['list_of_words'].index(x['answer']) if x['answer'] in x['list_of_words'] else None, axis=1)
    #df['check'] = df.apply(lambda x: x['position'] == x['position'].shift(-1) + 1 if x['position'] is not None else None, axis=1)
    return df

df = check_position_difference(df)

df = df.dropna()
print(df.head())

print(df.info())
df = df.reset_index().drop("index", axis = 1)
print(df)
to_remove = []
for i in range(len(df)-1, 0, -1):
  #print(i)
  if df.iloc[i,2] == df.iloc[i-1, 2]:
    if df.iloc[i,6] == df.iloc[i-1, 6] - 1:
      df.iloc[i-1,0] = df.iloc[i,0] + " " +  df.iloc[i-1,0]
      to_remove.append(i)

df.drop(to_remove, inplace=True, axis = 0)
print(df.head())

from transformers import T5Tokenizer, AutoModelWithLMHead

tokenizer2 = T5Tokenizer.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap", use_fast=False)

model2 = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")

def get_question(answer, context, max_length=250):
  input_text = "answer: %s  context: %s </s>" % (answer, context)
  features = tokenizer2([input_text], return_tensors='pt')

  output = model2.generate(input_ids=features['input_ids'],
               attention_mask=features['attention_mask'],
               max_length=max_length)

  return_question = tokenizer2.decode(output[0]).split("<pad> question: ")[1].split("</s>")[0]


  return return_question

df['question'] = df.apply(lambda row: get_question(row['answer'], row['summary']), axis=1)

df.to_csv("generated_questions_with_answers.csv", index=False)
