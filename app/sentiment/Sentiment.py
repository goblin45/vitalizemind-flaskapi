from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
from scipy.special import softmax
import numpy as np


MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)


def roberta_polarity_score(example):
    try:
        encoded_text = tokenizer(example, return_tensors='pt')
        output = model(**encoded_text)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        scores_dict = {
            'neg': scores[0],
            'neu': scores[1],
            'pos': scores[2]
        }
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        scores_dict = {'neg':0,'neu':1,'pos':1}

    return scores_dict