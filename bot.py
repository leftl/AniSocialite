from time import sleep
from pathlib import Path
from random import randint as rand
from dotenv import dotenv_values, set_key
from auth import authenticate
from queries import request, GET_ACTIVITES, LIKE_ACTIVITY, GET_USER_ID

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
        resp = request(API_URL, headers, GET_USER_ID)
        set_key("./.env", "user_id", str(resp['data']['UpdateUser']['id']))

def main():
    init()

    # CONFIG: The ID of each series (Anime OR Manga) you wish to monitor the social activities of.
    #   Cowboy Bebop: https://anilist.co/anime/1/Cowboy-Bebop/ => ID: 1
    #   Sailor Moon: https://anilist.co/anime/530/Sailor-Moon/ => ID: 530
    media_ids = [1, 530]

    while True:
        resp = request(API_URL, headers, GET_ACTIVITES, variables={'media_ids' : media_ids})
        activities = resp['data']['Page']['activities']

        for act in activities:
            if 'isLiked' not in act.keys():
                continue

            if not act['isLiked']:
                resp = request(API_URL, headers, LIKE_ACTIVITY, variables = { "activityId" : act['id'] })

                if resp is None:
                    continue

                print(f"Liked: activity id {act['id']} by {act['user']['name']}")
                sleep(4)

        sleep(rand(15,25))

main()
