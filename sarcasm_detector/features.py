from textblob import TextBlob

from preprocessor import preprocess
from tweets import get_tweets_for_feature_extraction

def get_topic_sentiment(topic_keywords):
    topic_polarity_distance = [0]
    topic_subjectivity_distance = [0]
    topic_sarcastic = False

    for topic_keyword in topic_keywords:
        tweets = get_tweets_for_feature_extraction(topic_keyword, 5)

        tweets_polarity = [0]
        tweets_subjectivity = [0]
        tweets_sarcastic = False
        for tweet in tweets:
            processed_tweet = preprocess(tweet["text"])
            processed_text = processed_tweet["text"]

            blob_text = TextBlob(processed_text)
            tweets_polarity.append(blob_text.sentiment.polarity)
            tweets_subjectivity.append(blob_text.sentiment.subjectivity)

            tweets_sarcastic = ("#sarcasm" in processed_tweet["hashtags"]) or tweets_sarcastic

        topic_polarity_distance.append(max(tweets_polarity) - min(tweets_polarity))
        topic_subjectivity_distance.append(max(tweets_polarity) - min(tweets_polarity))
        topic_sarcastic = topic_sarcastic or tweets_sarcastic

    return sum(topic_polarity_distance) / (len(topic_keywords) or 1), sum(topic_subjectivity_distance) / (len(topic_keywords) or 1), int(topic_sarcastic)

def get_features(tweet):

    # is tweet sarcastic
    is_sarcastic = int("#sarcasm" in tweet["text"])

    # preprocess tweet content
    processed_tweet = preprocess(tweet["text"])
    processed_text = processed_tweet["text"]

    blob_text = TextBlob(processed_text)

    # measure sentiment features of tweet
    sentence_polarity = blob_text.sentiment.polarity
    sentence_subjectivity = blob_text.sentiment.subjectivity

    # calculate word based polarity to capture extreme expressions
    polarities = []
    for word in processed_text.split(" "):
        blob_word = TextBlob(word)
        polarities.append(blob_word.sentiment.polarity)

    maximum_word_polarity = max(polarities)
    minimum_word_polarity = min(polarities)

    # measure how extreme the most expressive is with respect to whole sentence
    polarity_distance_max = maximum_word_polarity - sentence_polarity
    polarity_distance_min = abs(minimum_word_polarity - sentence_polarity)

    # extract topic based sentiment values; combined polarity, subjectivity and any sarcasm clue
    topic_keywords = blob_text.noun_phrases + processed_tweet["hashtags"] + processed_tweet["mentions"]
    topic_polarity, topic_subjectivity, topic_sarcasm = get_topic_sentiment(topic_keywords)

    return ["{0:.2f}".format(sentence_polarity),
            "{0:.2f}".format(sentence_subjectivity),
            "{0:.2f}".format(maximum_word_polarity),
            "{0:.2f}".format(polarity_distance_max),
            "{0:.2f}".format(polarity_distance_min),
            "{0:.2f}".format(topic_polarity),
            "{0:.2f}".format(topic_subjectivity),
            topic_sarcasm,
            is_sarcastic]
