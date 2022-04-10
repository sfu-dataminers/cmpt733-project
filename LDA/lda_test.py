from gensim import corpora, models
from LDA.preprocess_lda import preprocess

# Fetch twitter topic from tweets using LDA
def get_topic(tweet):
    # Load LDA model and corpora created in train
    lda_model4 = models.LdaModel.load('./LDA/LDA_details/lda_model4.model')
    id2word = corpora.Dictionary.load('./LDA/LDA_details/id2word.dict')

    # Create doc to bag to word and fetch topics using model
    bow_vector = id2word.doc2bow(preprocess(tweet))
    result = lda_model4.get_document_topics(bow_vector)
    resultdict = dict(result)
    orddict = sorted(resultdict, key=resultdict.get, reverse=True)
    
    # Classifying fetched topics into issues
    keymax = 1
    keymax +=orddict[0]

    if keymax == 1:
        return 'Delay Issue'
    elif keymax == 2:
        return 'Reservation Issue'
    elif keymax == 3:
        return 'Baggage Issue'
    elif keymax == 4:
        return 'Customer Service'
    elif keymax == 5:
        return 'Rescedule Issue'
    elif keymax == 6 or keymax == 7:
        return 'Phone or Online Booking Issue'
    else:
        return 'Refund Issues'
