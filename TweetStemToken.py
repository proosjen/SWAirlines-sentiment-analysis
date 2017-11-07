class TweetStemToken:
    def stem(self, text):
        stemmer = nltk.PorterStemmer() 
        return stemmer.stem(text.lower())
    
    def tokenize(self, text):
        tokenizer = nltk.word_tokenize
        tokens = [] + tokenizer(text)
        return tokens