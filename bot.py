from time import sleep
from pathlib import Path
from random import randint as rand
from dotenv import dotenv_values, set_key
from auth import authenticate
from queries import request, GET_ACTIVITES, LIKE_ACTIVITY, GET_USER_ID

API_URL = "https://graphql.anilist.co"
ENV_PATH = Path(".env")
SLEEP_TIME = 5
headers = { "Content-Type": "application/json",
            "Accept": "application/json" }
config = None

def init():
    global config
    config = dotenv_values(ENV_PATH)

    if 'access_token' not in config.keys() or config['access_token'] == "":
        authenticate(config, ENV_PATH)
        config = dotenv_values(ENV_PATH)

    headers['Authorization'] = f"Bearer {config['access_token']}"

    if 'user_id' not in config.keys() or config['user_id'] == "":
        resp = request(API_URL, headers, GET_USER_ID)
        set_key("./.env", "user_id", str(resp['data']['UpdateUser']['id']))
        config = dotenv_values(ENV_PATH)

def main():
    init()
    userid = config['user_id'] if config is not None else 0

    # CONFIG: The ID of each series (Anime OR Manga) you wish to monitor the social activities of.
    #   Cowboy Bebop: https://anilist.co/anime/1/Cowboy-Bebop/ => ID: 1
    #   Sailor Moon: https://anilist.co/anime/530/Sailor-Moon/ => ID: 530
    media_ids = [1, 530]

    while True:
        resp = request(API_URL, headers, GET_ACTIVITES, variables={'media_ids' : media_ids, 'self_uid' : userid})

        if resp is None:
            continue

        activities = resp['data']['Page']['activities']

        if activities:
            for act in activities[::-1]:
                if 'isLiked' not in act.keys():
                    continue

                if not act['isLiked']:
                    resp = request(API_URL, headers, LIKE_ACTIVITY, variables = { "activityId" : act['id'] })

                    if resp is None:
                        continue

                    print(f"Liked: activity id {act['id']} by {act['user']['name']}")
                    sleep(SLEEP_TIME)

        sleep(SLEEP_TIME)

main()