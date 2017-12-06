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

    
def polarity_ratio(tweet_word_list):
    num_pos = 0
    num_neg = 0
    for word in tweet_word_list:
        if str(word) in positive_words:
            num_pos += 1
        if str(word) in negative_words:
            num_neg += 1
    return {'num_pos': num_pos, 'num_neg': num_neg}


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


def get_words_in_tweets(tweets):
    allWords = []
    for (processed_words, category) in tweets:
        allWords.extend(processed_words)
    return allWords


def get_word_features(wordList):
    wordList = nltk.FreqDist(wordList)
    wordFeatures = wordList.keys()
    return wordFeatures


word_features = get_word_features(get_words_in_tweets(trainTweets))


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features



training_set = nltk.classify.apply_features(extract_features, trainTweets)


# Train a Naive Bayes classifier with training data
classifier = nltk.NaiveBayesClassifier.train(training_set)

#print classifier.show_most_informative_features(10)


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
