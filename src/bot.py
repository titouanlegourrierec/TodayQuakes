# Copyright (c) 2025 Titouan Le Gourrierec
"""Automate daily Twitter posts."""

import datetime
import os
from datetime import timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import tweepy
from dotenv import load_dotenv

from config_logging import configure_logging, log_execution_time
from daily_quakes import twitter_message


logging = configure_logging()

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

MAX_MEMORY_SIZE = 30


@log_execution_time(message="Authenticating with Twitter API.")
def authenticate_twitter() -> tuple[tweepy.Client, tweepy.API]:
    """
    Authenticate with the Twitter API using Tweepy.

    This function retrieves API keys and access tokens from environment variables and uses them to authenticate with
    the Twitter API.
    It returns a Tweepy Client object for the Twitter API v2 and a Tweepy API object for the Twitter API v1.1.

    Returns:
        tuple: A tuple containing:
            - client (tweepy.Client): A client object for Twitter API v2.
            - api (tweepy.API): An API object for Twitter API v1.1.

    Raises:
        OSError: If any of the required API keys or tokens are missing from environment variables.

    """
    # log if any of the keys are missing
    if not all([API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
        logging.error("One or more Twitter API keys or tokens are missing in environment variables.")
        msg = "Missing Twitter API keys or tokens."
        raise OSError(msg)

    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_KEY_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )
    auth = tweepy.OAuth1UserHandler(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    return client, api


@log_execution_time(message="Posting tweet.")
def post_tweet(client: tweepy.Client, api: tweepy.API, message: str, image_path: str) -> tweepy.Response:
    """
    Post a tweet with an image using the Twitter API.

    This function takes a Tweepy Client object for Twitter API v2, a Tweepy API object for Twitter API v1.1, a message,
    and an image path.
    It uploads the image using the v1.1 API and posts a tweet with the provided message and the uploaded image's media
    ID using the v2 API.

    Args:
        client (tweepy.Client): The client object for Twitter API v2.
        api (tweepy.API): The API object for Twitter API v1.1.
        message (str): The text of the tweet.
        image_path (str): The file path of the image to be uploaded.

    Returns:
        - tweepy.Response: The response from the Twitter API after posting the tweet.

    """
    media = api.media_upload(image_path)
    response = client.create_tweet(text=message, media_ids=[media.media_id])

    msg = f"Tweet posted at 'https://x.com/TodayQuakes/status/{response.data['id']}'."
    logging.info(msg)

    return response


@log_execution_time(message="Managing memory.")
def manage_memory(memory: list[list[str]], api: tweepy.API) -> None:
    """
    Manage the memory of posted tweets to avoid exceeding a maximum size.

    This function checks if the memory list exceeds a predefined maximum size (MAX_MEMORY_SIZE). If it does,
    the function removes the oldest entry from the memory and deletes the corresponding media file from the filesystem
    as well as the tweet from Twitter.

    Args:
        memory (list): A list of tuples, where each tuple contains the path to a media file and the tweet ID.
        api (tweepy.API): The API object for Twitter API v1.1, used to delete tweets.

    Note:
        This function modifies the memory list in place and does not return any value.

    """
    while len(memory) > MAX_MEMORY_SIZE:
        media_path, csv_path, tweet_id = memory.pop(0)
        msg = f"Removing media file: {media_path}, csv file: {csv_path} and tweet with ID: {tweet_id}"
        logging.info(msg)
        Path(media_path).unlink()
        Path(csv_path).unlink()
        api.destroy_status(tweet_id)


def main() -> None:
    """Automate daily Twitter posts."""
    today = datetime.datetime.now(tz=datetime.UTC).date()
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
