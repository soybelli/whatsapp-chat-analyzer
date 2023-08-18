import vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sentiment= SentimentIntensityAnalyzer()

def fetch_sentiment(df):
    df['positive']=[sentiment.polarity_scores(i)['pos'] for i in df['message']]
    df['negative']=[sentiment.polarity_scores(i)['neg'] for i in df['message']]
    df['neutral']=[sentiment.polarity_scores(i)['neu'] for i in df['message']]
    return df

def sentiment_value(df):
    x=sum(df['positive'])
    y=sum(df['negative'])
    z=sum(df['neutral'])

    if (x>y) and (x>z):
        a="positive"
    elif (y>z) and (y>x):
        a="negative"
    else:
        a="neutral"
    dict1={
        'positive': x,
        'negative': y,
        'neutral' : z
    }
    return a,dict1