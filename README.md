# AniSocialite
This bot will automatically like the latest social activity of a set of anime/manga series on [AniList](https://anilist.co). That is, each list update (i.e. watched an episode or read a chapter) for a series being watched will have that activity like by the bot. This is a great way to build a following on the site since the social-network side of the platform is fairly basic.

The objectives of this weekend project were to practice/refamiliarize myself with:
- Python 3
- GraphQL
- OAuth 2.0
- APIs

This project is UNOFFICIAL and not affiliated with the AniList team at all. 
Tested on Python 3.8 and 3.9.

Pull requests welcome!

> Note: due to fairly strict API rate-limiting, ***not all*** activities will be liked, especially if multiple popular series are being monitored. 

## Setup
Create and activate a new virtualenv in the project directory

```
# creates a virtualenv
python3 -m venv venv

# activates the virtualenv
source venv/bin/activate
```

Install needed dependencies

```
pip3 install requests python-dotenv
```

## Configure
Rename `.env.example` to `.env` and follow the comments/links to ensure the correct values are inserted for each environment variable.

Additionally, the variable `media_ids` in `bot.py` needs to be filled with the series ID for each series you wish to monitor. The series ID can be found in the URL of the series page. For example: Cowboy Bebop has the URL [https://anilist.co/anime/**1**/Cowboy-Bebop/](https://anilist.co/anime/1/Cowboy-Bebop/), with the ID **1** found following `/anime/`.

## Run
To run the bot, simply enter the following from a terminal while in the project's top-level directory (the virtualenv must be activated, see above):
```
python bot.py
```

Use the `Ctrl-c` to terminate the bot.

Once completed, close the virtualenv:
```
deactivate
```
