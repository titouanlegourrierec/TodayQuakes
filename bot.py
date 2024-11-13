import os
from datetime import date, timedelta

import tweepy
import pandas as pd
import numpy as np

from DailyQuakes import twitter_message
from config_logging import configure_logging, log_execution_time

logging = configure_logging()


@log_execution_time(message="Authenticating with Twitter API.")
def authenticate_twitter() -> tuple[tweepy.Client, tweepy.API]:
    """
    Authenticates a user with the Twitter API using Tweepy.

    This function retrieves API keys and access tokens from environment variables and uses them to authenticate with the Twitter API.
    It returns a Tweepy Client object for the Twitter API v2 and a Tweepy API object for the Twitter API v1.1.

    Returns:
        tuple: A tuple containing:
            - client (tweepy.Client): A client object for Twitter API v2.
            - api (tweepy.API): An API object for Twitter API v1.1.
    """

    API_KEY = os.getenv("API_KEY")
    API_KEY_SECRET = os.getenv("API_KEY_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

    client = tweepy.Client(
        consumer_key=API_KEY, consumer_secret=API_KEY_SECRET,
        access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET
    )
    auth = tweepy.OAuth1UserHandler(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    return client, api


@log_execution_time(message="Posting tweet.")
def post_tweet(client: tweepy.Client, api: tweepy.API, message: str, image_path: str) -> tweepy.Response:
    """
    Posts a tweet with an image using the Twitter API.

    This function takes a Tweepy Client object for Twitter API v2, a Tweepy API object for Twitter API v1.1, a message, and an image path.
    It uploads the image using the v1.1 API and posts a tweet with the provided message and the uploaded image's media ID using the v2 API.

    Parameters:
        - client (tweepy.Client): The client object for Twitter API v2.
        - api (tweepy.API): The API object for Twitter API v1.1.
        - message (str): The text of the tweet.
        - image_path (str): The file path of the image to be uploaded.

    Returns:
        - tweepy.Response: The response from the Twitter API after posting the tweet.
    """

    media = api.media_upload(image_path)
    response = client.create_tweet(text=message, media_ids=[media.media_id])

    logging.info(f"Tweet posted at 'https://x.com/TodayQuakes/status/{response.data['id']}'.")

    return response


@log_execution_time(message="Managing memory.")
def manage_memory(memory: list[list[str]], api: tweepy.API) -> None:
    """
    Manages the memory of posted tweets to avoid exceeding a maximum size.

    This function checks if the memory list exceeds a predefined maximum size (MAX_MEMORY_SIZE). If it does, the function
    removes the oldest entry from the memory and deletes the corresponding media file from the filesystem as well as the tweet from Twitter.

    Parameters:
        - memory (list): A list of tuples, where each tuple contains the path to a media file and the tweet ID.
        - api (tweepy.API): The API object for Twitter API v1.1, used to delete tweets.

    Note:
        This function modifies the memory list in place and does not return any value.
    """

    MAX_MEMORY_SIZE = 30
    while len(memory) > MAX_MEMORY_SIZE:
        media_path, csv_path, tweet_id = memory.pop(0)
        logging.info(f"Removing media file: {media_path}, csv file: {csv_path} and tweet with ID: {tweet_id}")
        os.remove(media_path)
        os.remove(csv_path)
        api.destroy_status(tweet_id)


def main() -> None:
    """
    Main function to automate daily Twitter posts.
    """

    today = date.today()
    yesterday = today - timedelta(1)
    starttime = f"{yesterday.year}-{yesterday.month}-{yesterday.day}"

    df = pd.read_csv(f"data/{starttime}.csv")

    client, api = authenticate_twitter()

    response = post_tweet(client, api, twitter_message(df, starttime), f"outputs/{starttime}.png")

    memory = np.load("data/memory.npy").tolist()
    memory.append([f"outputs/{starttime}.png", f"data/{starttime}.csv", response.data["id"]])
    manage_memory(memory, api)
    np.save("data/memory.npy", memory)

    logging.info("bot.py executed successfully.\n\n --- \n\n")


if __name__ == "__main__":
    main()
