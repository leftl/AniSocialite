import requests
from dotenv import set_key

# OAuth2.0 via requests reference: https://developer.byu.edu/docs/consume-api/use-api/oauth-20/oauth-20-python-sample-code
def authenticate(config, env_path):
    auth_url = "https://anilist.co/api/v2/oauth/authorize"
    token_url = "https://anilist.co/api/v2/oauth/token"
    headers = { "Accept": "application/json",
                "Content-Type": "application/json" }

    # Get code from user
    print(f"Please visit the folowing site to obtain a code to authenticate: \n\t{auth_url}?client_id={config['client_id']}&redirect_uri={config['client_redirect']}&response_type=code")
    auth_code = input('Copy and paste the code here: ')

    try:
        resp = requests.post(token_url, headers = headers, json = {
            "grant_type": "authorization_code",
            "client_id": config['client_id'],
            "client_secret": config['client_secret'],
            "redirect_uri": config['client_redirect'],
            "code": auth_code
        })
    except Exception as exc:
        print("[ERROR] Exception encountered: ", exc.args)
        raise

    resp = resp.json()
    set_key(env_path, 'access_token', resp['access_token'])
    set_key(env_path, 'code', resp['refresh_token'])
    print(f"[INFO] Authentication for client {config['client_id']} was successful.")
