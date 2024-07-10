import os
from datetime import datetime, date, timedelta, timezone

import tweepy
import pandas as pd

from DailyQuakes import fetch_earthquake_data, process_earthquake_data, create_geodataframe, plot_earthquakes, twitter_message

def main():

    today = date.today()
    yesterday = today - timedelta(1)
    starttime = f"{yesterday.year}-{yesterday.month}-{yesterday.day}"

    df = pd.read_csv(f"data/{starttime}.csv")

    # Load Twitter API credentials from environment variables
    API_KEY = os.getenv("API_KEY")
    API_KEY_SECRET = os.getenv("API_KEY_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

    # Authenticate with Twitter using Tweepy
    client = tweepy.Client(
        consumer_key=API_KEY, consumer_secret=API_KEY_SECRET,
        access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET
    )
    auth = tweepy.OAuth1UserHandler(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Upload the earthquake plot image to Twitter
    media = api.media_upload(f"outputs/{starttime}.png")

    # Post a tweet with the uploaded image
    response = client.create_tweet(
        text=twitter_message(df, starttime),
        media_ids=[media.media_id]
    )

if __name__ == "__main__":
    main()