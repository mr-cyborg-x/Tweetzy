from textblob import TextBlob
import datetime

def analyze_sentiment(tweets):
    positive = 0
    negative = 0
    neutral = 0
    total_polarity = 0
    
    analyzed_tweets = []

    for tweet_data in tweets:
        # Handle both string (legacy) and dict (new) formats
        if isinstance(tweet_data, str):
            text = tweet_data
            metadata = {}
        else:
            text = tweet_data.get('text', '')
            metadata = tweet_data
            
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        total_polarity += polarity
        
        sentiment = "Neutral"
        if polarity > 0:
            sentiment = "Positive"
            positive += 1
        elif polarity < 0:
            sentiment = "Negative"
            negative += 1
        else:
            neutral += 1
            
        result = {
            "text": text,
            "sentiment": sentiment,
            "polarity": polarity,
            "username": metadata.get('username', 'Anonymous'),
            "handle": metadata.get('handle', '@anonymous'),
            "timestamp": metadata.get('timestamp', 'Just now')
        }
        analyzed_tweets.append(result)

    total = len(tweets)
    if total > 0:
        avg_polarity = total_polarity / total
    else:
        avg_polarity = 0

    return {
        "total": total,
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "average_polarity": avg_polarity,
        "tweets": analyzed_tweets,
        "timestamp": datetime.datetime.now().isoformat()
    }
