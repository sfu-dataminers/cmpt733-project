import pandas as pd
import re, json
import warnings
import gensim

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
from nltk import word_tokenize,sent_tokenize
from nltk.stem.porter import PorterStemmer
from textblob import TextBlob

from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from bs4 import BeautifulSoup

stopwords_lda = pd.read_csv("./LDA/LDA_details/stopwords_lda.csv")

def preprocess(text):
        stopwords = set(STOPWORDS)

        # Appending new airline related stop-words
        stopwords.update([str(i).lower() for i in stopwords_lda.name]) 
        
         # Replacing similar words
        def replace_similar(text):
            with open('./LDA/LDA_details/sample.json', 'r') as openfile:
                json_object = json.load(openfile)
            for key, value in json_object.items():
                text = text.replace(key, value)
            return text
            
        # Replacing similar words
        text = replace_similar(text)
        
        # Filter for mentions
        mentions_filter = re.compile(r'(?<=\@)(\w+)')
        # Filter for hash-tags
        hashtags_filter = re.compile(r'(?<=\#)(\w+)')
        # Finding all mentions
        all_mentions = mentions_filter.findall(text.lower())
        # Finding all hash-tags
        all_hashtag = hashtags_filter.findall(text.lower())

        word_lemmatize = WordNetLemmatizer()
        # Lemmatizing tokens
        def lemm_tokens(tokens, lemmatize):
            lemmatized = []
            for item in tokens:
                lemmatized.append(lemmatize.lemmatize(item,'v'))
            return lemmatized

        # De-emojify tweets to text
        def deEmojify(inputString):
            return inputString.encode('ascii', 'ignore').decode('ascii')

        text = deEmojify(text)
        soup = BeautifulSoup(text)
        text = soup.get_text()

        # Removing punctuation
        punc_text = [x.lower() for x in text if x not in string.punctuation]
        text = "".join(punc_text)
        
        # Tokenize words
        word_tokens = nltk.word_tokenize(text)
        
        # Keeping the words with length between 4 and 15
        filtered_tokens = [x for x in word_tokens if len(x)>4 and len(x)<15]
        
        # Filter tokens
        tokens = lemm_tokens(filtered_tokens, word_lemmatize)
        
        all_tokens = [i for i in tokens if (i not in stopwords) and (i not in all_mentions) 
                      and (i not in all_hashtag) and (not i.isdigit())]
        return all_tokens
