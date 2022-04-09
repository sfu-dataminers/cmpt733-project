from preprocess_lstm import preprocess
import pandas as pd
from ast import literal_eval
import numpy as np

from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from keras.models import load_model

from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def decode_prediction(prediction):
    if prediction == 0:
        return "Negative"
    elif prediction == 1:
        return "Neutral"
    else:
        return "Positive"

def predict_sentiment(text):
    model = load_model("./LSTM_details/model.h5")
    model.load_weights('./LSTM_details/model_weights.h5') 
    model.compile(loss = 'categorical_crossentropy', optimizer='adam', metrics = ['accuracy'])

    f = open("./LSTM_details/X_train_max_length.txt", "r")
    max_length = int(f.read())

    df_vals = pd.read_csv('./LSTM_details/train_text_vals.csv',converters={'text_tokenized': literal_eval})
    tokenizer = Tokenizer(num_words=500, split=' ')
    tokenizer.fit_on_texts(df_vals['text_tokenized'].values)

    text = preprocess(text)
    text = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen = max_length, dtype='float64')

    prediction = model.predict([text])
    result = np.where(prediction[0] == np.amax(prediction[0]))

    return decode_prediction(result[0])
