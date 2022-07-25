from tokenize import String
from typing import final
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import tweepy
import json
from textblob import TextBlob
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

app = FastAPI()


origins = [
    "http://localhost:3000",
    "localhost:3000",
    "https://orbitalfrontend.herokuapp.com/"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True
    # allow_methods=["*"],
    # allow_headers=["*"]
)

dic = {"Ticker": "temp"}

# @app.get("/", tags=["root"])
# async def read_root() -> dict:
#     return {"message": "Welcome to your todo list."}


@app.get("/stocksearch", tags=["stocksearch"])
async def get_dic():
    stock = dic["Ticker"]
    return stock


@app.post("/stocksearch", tags=["stocksearch"])
async def change_dic(input: dict):
    variable = input['ticker']
    dic["Ticker"] = variable
    all_tweets = twit(variable)
    final_score = 0
    analyzer = SentimentIntensityAnalyzer()
    for i in all_tweets.values():
        # ts = TextBlob(i).sentiment
        # final_score += ts.polarity
        # print(ts.polarity)
        vs = analyzer.polarity_scores(i)
        final_score += vs["compound"]
    sentiment_score = final_score/len(all_tweets)
    probability_score = predict(variable)
    return json.dumps([sentiment_score, probability_score])


def clean(txt):
    txt = re.sub(r'@[A-Za-z0-9]+', '', txt)  # Removed @mentions
    txt = re.sub(r'#', '', txt)  # Removing the '#' symbol
    txt = re.sub(r'RT[\s]+', '', txt)  # Removing RT
    txt = re.sub(r'https?:\/\/\S+', '', txt)  # Remove the hyper link
    return txt


def twit(stock):
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    result = {}
    api = tweepy.API(auth)

    cursor = tweepy.Cursor(api.search_tweets, q=stock, lang="en", result_type="mixed",
                           tweet_mode="extended").items(100)
    for i, value in enumerate(cursor):
        result[i] = clean(value.full_text)

    return result


def predict(stock):
    ticker = yf.Ticker(stock)
    ticker_hist = ticker.history(period="max")
    data = ticker_hist[["Close"]]
    data = data.rename(columns={'Close': 'Actual Close'})
    data["Target"] = ticker_hist.rolling(2).apply(
        lambda x: x.iloc[1] > x.iloc[0])["Close"]
    ticker_prev = ticker_hist.copy()
    ticker_prev = ticker_prev.shift(1)
    predictors = ["Close", "High", "Low", "Open", "Volume"]
    new = data.join(ticker_prev[predictors]).iloc[1:]
    model = RandomForestClassifier(
        n_estimators=100, min_samples_split=200, random_state=1)
    train = new.iloc[:-100]
    test = new.iloc[-100:]

    # adding extra predictors in order to make more accurate predictions, taking ratio of averages within different timeframes to the closing price and using them to predict the next direction
    weekly_mean = new.rolling(7).mean()
    quarterly_mean = new.rolling(90).mean()
    annual_mean = new.rolling(365).mean()
    weekly_trend = new.shift(1).rolling(7).mean()["Target"]

    new["weekly_mean"] = weekly_mean["Close"] / new["Close"]
    new["quarterly_mean"] = quarterly_mean["Close"] / new["Close"]
    new["annual_mean"] = annual_mean["Close"] / new["Close"]

    new["annual_weekly_mean"] = new["annual_mean"] / new["weekly_mean"]
    new["annual_quarterly_mean"] = new["annual_mean"] / new["quarterly_mean"]
    new["weekly_trend"] = weekly_trend

    new["open_close_ratio"] = new["Open"] / new["Close"]
    new["high_close_ratio"] = new["High"] / new["Close"]
    new["low_close_ratio"] = new["Low"] / new["Close"]
    full_predictors = predictors + ["weekly_mean", "quarterly_mean", "annual_mean", "annual_weekly_mean", "annual_quarterly_mean", "open_close_ratio",
                                    "high_close_ratio", "low_close_ratio"]

    def backtest(new, model, full_predictors, start=1000, step=500):
        predictions = []
        for i in range(start, new.shape[0], step):

            train = new.iloc[0:i].copy()
            test = new.iloc[i:(i+step)].copy()

        # backtesting, not cross validation as doesnt make sense to use future data to
        # predict past data but only using past data to predict future data

            model.fit(train[full_predictors], train["Target"])
            preds = model.predict_proba(test[full_predictors])[:, 1]
            preds = pd.Series(preds, index=test.index)
        # preds[preds > .6] = 1
        # preds[preds<=.6] = 0

            combined = pd.concat(
                {"Target": test["Target"], "Predictions": preds}, axis=1)
            predictions.append(combined)

        predictions = pd.concat(predictions)
        return predictions

    predictions = backtest(new.iloc[365:], model, full_predictors)
    return predictions.iloc[-1]["Predictions"]


api_key = "MDuBpY2HoJjO2pyJ1DtOh6L1Y"
api_key_secret = "eG3vwiyEj9WRa5MozSnYnyHpjtqHME9SydGF06JwBeiBs6qN7t"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAMaAdgEAAAAAULr7gXv1%2BBvh9l3VqbdrblJr%2FuA%3DVMAa4v7EOsE2cJPuDUslpi8iEpAzbDhNrzCTpCsLyRwoKBPc4x"
access_token = "1535555326249799681-gmCTsABAfRRU2BRcg17R1YR1uAiwLz"
access_token_secret = "3J9zH73jvB3FE1SUceZhSd6vLHePDl7wh0uDrYyOuGM31"

# api_key = config.api_key
# api_key_secret = config.api_key_secret

# access_token = config.access_token
# access_token_secret = config.access_token_secret

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
print(dic["Ticker"])

cursor = tweepy.Cursor(api.search_tweets, q=dic["Ticker"], lang="en", result_type="popular",
                       tweet_mode="extended").items(100)
for i in cursor:
    print(i.full_text)
    print("created at", i.created_at)


# # create dataframe
# columns = ['Time', 'User', 'Tweet']
# data = []
# for tweet in public_tweets:
#     data.append([tweet.created_at, tweet.user.screen_name, tweet.text])

# df = pd.DataFrame(data, columns=columns)

# df.to_csv('tweets.csv')
