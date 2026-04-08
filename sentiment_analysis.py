from textblob import TextBlob

def clean_text(text):
    return text.lower()

def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

def apply_sentiment(df):
    df["sentiment"] = df["post"].apply(get_sentiment)
    return df

def sentiment_ratio(df):
    return df["sentiment"].value_counts(normalize=True) * 100
