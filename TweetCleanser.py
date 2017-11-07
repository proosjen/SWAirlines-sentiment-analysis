import re
import nltk

stopwords = nltk.corpus.stopwords.words("english")
whitelist = ["n't", "not"]

class TweetCleanser:
    
    def to_ascii(self, text):
        return text.encode('ascii', 'ignore').decode('ascii')
    
    def remove_urls(self, text):
        return re.sub(r"http.?://[^\s]+[\s]?", '', text)
    
    def remove_special_characters(self, text):
        return re.sub("[^0-9A-Za-z']", ' ', text)
    
    def remove_usernames(self, text):
        return re.sub(r"@[^\s]+[\s]?", '', text)
    
    def remove_numbers(self, text):
        return re.sub(r"\s?[0-9]+\.?[0-9]*", '', text)
    
    def remove_stopwords(self, tokens):
        for token in tokens:
            if token in stopwords and token not in whitelist:
                tokens.remove(token)
        return tokens