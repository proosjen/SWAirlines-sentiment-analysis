import nltk

'''
The purpose of this class is to stem and tokenize the tweet.

This tweet stemmer/ tokenizer was influenced by a method
defined in this blog post: 
http://zablo.net/blog/post/twitter-sentiment-analysis-python-scikit-word2vec-nltk-xgboost
'''
class TweetStemToken:
    
    # Use the nltk Porter Stemmer to stem the tweet
    def stem(self, text):
        stemmer = nltk.PorterStemmer() 
        return stemmer.stem(text.lower())
    
    # Use the nltk word_tokenize method to tokenize the tweet into a list of words
    def tokenize(self, text):
        tokenizer = nltk.word_tokenize
        tokens = [] + tokenizer(text)
        return tokens