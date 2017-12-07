import re
import nltk

stopwords = nltk.corpus.stopwords.words("english")
'''
Words like "not" and "n't" can have a great influence on sentiment.
We will "whitelist" these two words when removing stopwords from
the tweet.
'''
whitelist = ["n't", "not"]

'''
The purpose of this class is to cleanse the tweet.

This tweet cleanser was influenced by a tweet cleansing method
defined in this blog post: 
http://zablo.net/blog/post/twitter-sentiment-analysis-python-scikit-word2vec-nltk-xgboost
'''
class TweetCleanser:
    
    # Convert tweet to ascii character set
    def to_ascii(self, text):
        return text.encode('ascii', 'ignore').decode('ascii')
    
    # Remove any urls from tweet
    def remove_urls(self, text):
        return re.sub(r"http.?://[^\s]+[\s]?", '', text)
    
    # Remove special characters from tweet
    def remove_special_characters(self, text):
        return re.sub("[^0-9A-Za-z']", ' ', text)
    
    # Remove any usernames from tweet
    def remove_usernames(self, text):
        return re.sub(r"@[^\s]+[\s]?", '', text)
    
    # Remove any numbers from tweet
    def remove_numbers(self, text):
        return re.sub(r"\s?[0-9]+\.?[0-9]*", '', text)
    
    # Remove nltk stopwords from tweet, except words from white list
    def remove_stopwords(self, tokens):
        for token in tokens:
            if token in stopwords and token not in whitelist:
                tokens.remove(token)
        return tokens