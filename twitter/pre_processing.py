import re
import string
import nltk
import glob
import pandas as pd
from bs4 import BeautifulSoup
from wordcloud import STOPWORDS
# nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer


def preprocess(text):
    text = str(text)
    stopwords = set(STOPWORDS)
    stopwords.update(["air","airline","united","us","airways","virgin","america","jetblue",
                     "usairway","usairways","flight","americanair","southwestair","southwestairlines",
                     "southwestairway","southwestairways","virginamerica","sunday","monday","tuesday",
                     "wednesday","thursday","friday","saturday", "miami","los angeles","new york",
                     "chicago","dallas","savannah"])

    r = re.compile(r'(?<=\@)(\w+)')
    ra = re.compile(r'(?<=\#)(\w+)')
    ro = re.compile(r'(flt\d*)')

    names = r.findall(text.lower())
    hashtag = ra.findall(text.lower())
    flight = ro.findall(text.lower())
    lmtzr = WordNetLemmatizer()

    def stem_tokens(tokens, lemmatize):
        lemmatized = []
        for item in tokens:
            lemmatized.append(lemmatize.lemmatize(item, 'v'))
        return lemmatized

    def deEmojify(inputString):
        return inputString.encode('ascii', 'ignore').decode('ascii')

    text = deEmojify(text)
    soup = BeautifulSoup(text, features="lxml")
    text = soup.get_text()
    text = ''.join([ch.lower() for ch in text if ch not in string.punctuation])
    tokens = nltk.word_tokenize(text)
    tokens = [ch for ch in tokens if len(ch) >= 3]
    tokens = [ch for ch in tokens if len(ch) <= 15]
    lemm = stem_tokens(tokens, lmtzr)
    lemstop = [i for i in lemm if i not in stopwords]
    lemstopcl = [i for i in lemstop if i not in names]
    lemstopcl = [i for i in lemstopcl if i not in hashtag]
    lemstopcl = [i for i in lemstopcl if i not in flight]
    lemstopcl = [i for i in lemstopcl if not i.isdigit()]
    return lemstopcl


# if __name__ == '__main__':

#     df = pd.concat(map(pd.read_csv, glob.glob('*.csv')))
#     df['tokenize_text'] = df['text'].apply(lambda text: preprocess(text))
#     df.to_csv('data/clean_data.csv')
