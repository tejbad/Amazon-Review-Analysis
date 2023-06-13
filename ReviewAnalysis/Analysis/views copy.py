from django.shortcuts import render
import nltk
import re


NON_ALPHANUM = re.compile(r'[\W]')
NON_ASCII = re.compile(r'[^a-z0-1\s]')

def normalize_data(texts):
    normalized_text = []
    for text in texts:
        lower_text = text.lower()
        no_punctuation = NON_ALPHANUM.sub(r'', lower_text)
        no_non_ascii = NON_ASCII.sub(r'',no_punctuation)
        normalized_text.append(no_non_ascii)
    return normalized_text

def get_texts(data):
    texts = []
    for i in range(len(data)):
        texts.append(data[i].get('body').lower())
    return texts

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def analysis(data):
    texts = get_texts(data)
    texts = normalize_data(texts)
    cv = CountVectorizer(binary=True)
    cv.fit(texts)
    X = cv.transform(texts)
    X_test = cv.transform(texts)
    print(X_test)
    # 
    X_train , X_val , y_train , y_val = train_test_split(X,texts,train_size = 0.75)
    for c in [0.01,0.05,0.25,0.5,1]:
        lr = LogisticRegression(C=c)
        lr.fit(X_train,y_train)
        print("Accuracy for C=%s: %s" %(c, accuracy_score(y_val, lr.predict(X_val))))