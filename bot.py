from time import sleep
from pathlib import Path
from random import randint as rand
from dotenv import dotenv_values, set_key
from auth import authenticate
from queries import *

API_URL = "https://graphql.anilist.co"
ENV_PATH = Path(".env")
headers = { "Content-Type": "application/json",
            "Accept": "application/json" }

def init():
    config = dotenv_values(ENV_PATH)

    if 'access_token' not in config.keys() or config['access_token'] == "":
        authenticate(config, ENV_PATH)
        config = dotenv_values(ENV_PATH)

    headers['Authorization'] = f"Bearer {config['access_token']}"

    if 'user_id' not in config.keys() or config['user_id'] == "":
        r = request(API_URL, headers, getUserId);
        set_key("./.env", "user_id", str(r['data']['UpdateUser']['id']))

def main():
    init()

    # CONFIG: The ID of each series (Anime OR Manga) you wish to monitor the social activities of.
    #   Cowboy Bebop: https://anilist.co/anime/1/Cowboy-Bebop/ => ID: 1
    #   Sailor Moon: https://anilist.co/anime/530/Sailor-Moon/ => ID: 530
    media_ids = [1, 530]

    while True:
        r = request(API_URL, headers, getActivities, variables={'media_ids' : media_ids});
        activities = r['data']['Page']['activities']

        for a in activities:
            if 'isLiked' not in a.keys():
                continue

            if not a['isLiked']: 
                r = request(API_URL, headers, likeActivity, variables = { "activityId" : a['id'] });
                print(f"Liked: activity id {a['id']} by {a['user']['name']}")
                sleep(4)

        sleep(rand(15,25))

main()
