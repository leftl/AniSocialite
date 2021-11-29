from time import sleep
import requests


GET_ACTIVITES = '''query ($media_ids: [Int]) {
    Page(page: 1, perPage: 20) {
        activities(mediaId_in: $media_ids, type_in: [MANGA_LIST, ANIME_LIST], sort: ID_DESC) {
            ... on ListActivity {
                id
                isLiked
                user {
                    name
                }
            }
        }
    }
}'''

GET_FOLLOWER_ACTIVITES = '''query ($self_uid: Int) {
    Page(page: 1, perPage: 25) {
      pageInfo {
        hasNextPage
      }
      activities(isFollowing: true, userId_not: $self_uid, sort: ID_DESC) {
          ... on ListActivity {
              id
              isLiked
              user {
                  name
              }
          }
          ... on TextActivity {
              id
              isLiked
              user {
                  name
              }
          }
      }
  }
}'''

LIKE_ACTIVITY = '''mutation ($activityId: Int) {
    ToggleLikeV2 (id: $activityId, type: ACTIVITY) {
        ... on ListActivity {
            likes {
                name
            }
        }
    }
}'''

GET_USER_ID = '''mutation {
    UpdateUser {
        id
    }
}'''

def request(url, headers, query, variables = None):
    try:
        resp = requests.post(url = url, headers = headers, json = {'query': query, 'variables': variables})
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        # requested data has been removed or is now private
        if resp.status_code == 404:
            return None
        # rate limited. sleep for 1 minute (AniList cool down) and retry once.
        # assume unrecoverable if request fails again.
        elif resp.status_code == 429:
            print("[ERROR] Rate-limit exceeded. Resting for 1 minute.")
            sleep(60)
            try:
                resp = requests.post(url = url, headers = headers, json = {'query': query, 'variables': variables})
            except Exception as exc:
                print("[ERROR] Exception encountered: ", exc.args)
                raise
        else:
            raise

    # TODO: check header for remaining api calls and time until refresh.
    #       LikeToggleV2 doesn't seem to respect the 'X-RateLimit-Remaining' header, cannot find documentation on this.
    # if int(resp.headers['X-RateLimit-Remaining']) < 5:
    #     print("[WARN] Approaching rate-limit. Sleeping for 5 secons.")
    #     sleep(5)

    return resp.json()
