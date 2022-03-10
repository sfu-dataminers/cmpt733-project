from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
def sentiment_scores(sentence):
    
    ngram_sentence = generate_n_grams(sentence, 2)
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
 
    # polarity_scores method of SentimentIntensityAnalyzer
    sentiment_dict = sid_obj.polarity_scores(ngram_sentence)
     
    print("Overall sentiment dictionary is : ", sentiment_dict)
    print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
 
    print("Sentence Overall Rated As", end = " ")
 
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        print("Positive")
 
    elif sentiment_dict['compound'] <= - 0.05 :
        print("Negative")
 
    else :
        print("Neutral")

def generate_n_grams(text,ngram = 1):
  words = [word for word in text.split(" ")]  
  temp = zip(*[words[i:] for i in range(0, ngram)])
  ans = [' '.join(ngram) for ngram in temp]
  return ans

if __name__ == "__main__" :
 
    input_tweet = input("Enter the cleaned tweet:")
 
    # function calling
    sentiment_scores(input_tweet)