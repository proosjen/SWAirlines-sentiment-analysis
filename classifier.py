import nltk

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.local

trainData = db.trainData
trainTweets = []
for tweet in trainData.find():
    pair = ()
    pair = pair + (tweet['processed_words'], tweet['category'])
    trainTweets.append(pair)

with open('opinion-lexicon-English/positive-words.txt') as pos_words:
    positive_words = [word.strip('\n') for word in pos_words.readlines()]
with open('opinion-lexicon-English/negative-words.txt') as neg_words:
    negative_words = [word.strip('\n') for word in neg_words.readlines()]

'''
This function returns the number of positive
and the number negative words in a list of 
preprocessed words in a tweet.
'''
def polarity_ratio(tweet_word_list):
    num_pos = 0
    num_neg = 0
    for word in tweet_word_list:
        if str(word) in positive_words:
            num_pos += 1
        if str(word) in negative_words:
            num_neg += 1
    return {'num_pos': num_pos, 'num_neg': num_neg}

'''
This function checks if the polarity ratio
matches the classification returned by our
classifier. If there is a match, a boolean
True value is returned.
'''
def validate_polarity(classification, ratio):
    if classification == 'positive':
        if ratio['num_pos'] > ratio['num_neg']:
            return True
    elif classification == 'negative':
        if ratio['num_neg'] > ratio['num_pos']:
            return True
    elif classification == 'neutral':
        if ratio['num_pos'] == ratio['num_neg']:
            return True
    else:
        return False

'''
The following two helper functions come from a 
blog post by Laurent Luce on Twitter sentiment
analysis using Python and NLTK. 

The blog post can be found here: 
https://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/
'''
def get_words_in_tweets(tweets):
    allWords = []
    for (processed_words, category) in tweets:
        allWords.extend(processed_words)
    return allWords


def get_word_features(wordList):
    wordList = nltk.FreqDist(wordList)
    wordFeatures = wordList.keys()
    return wordFeatures

'''
The list of word features need to be extracted from the tweets. 
word_features is a list with every distinct words ordered by
frequency of appearance.
'''
word_features = get_word_features(get_words_in_tweets(trainTweets))

'''
Before we create our classifier, we need to decide what features
are relevant. This feature extractor returns a dictionary indicating
what words are contained in the tweet (document). 
'''
def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


# We can now apply the features to our classifier using the nltk method apply_features.
training_set = nltk.classify.apply_features(extract_features, trainTweets)


# Train a Naive Bayes classifier with training data
classifier = nltk.NaiveBayesClassifier.train(training_set)

'''
This function uses the classifier we built and classifies
a tweet as positive, negative, or neutral. The sentiment
determined is returned.
'''
def classify(tweet):
    classification = classifier.classify(extract_features(tweet))
    ratio = polarity_ratio(tweet)
    final_sentiment = ""

    # Does the ratio of positive to negative words match the classifier output?
    if validate_polarity(classification, ratio):
        final_sentiment = classification
    # If neutral and polarity was not validated, set final sentiment to sentiment with higher word count
    else:
        if ratio['num_pos'] > ratio['num_neg']:
            final_sentiment = 'positive'
        elif ratio['num_pos'] < ratio['num_neg']:
            final_sentiment = 'negative'
        else:
            final_sentiment = 'neutral'  
    
    return final_sentiment
