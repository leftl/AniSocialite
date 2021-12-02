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
    # retry all requests up to 10 times.
    for i in range(0, 10):
        try:
            resp = requests.post(url = url, headers = headers, json = {'query': query, 'variables': variables})
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            # HTTP status 429 => rate limited. Sleep for 60 seconds. All other errors sleep for 5 minutes.
            time = 60 if resp.status_code == 429 else 300
            print(f"[ERROR] Rate limited or general HTTP error: {resp.status_code}. Continuing in {time / 60} minutes.")
            sleep(time)

            try:
                resp = requests.post(url = url, headers = headers, json = {'query': query, 'variables': variables})
                resp.raise_for_status()
            except requests.exceptions.HTTPError:
                continue

        return resp.json()

    # all retries failed. return no response.
    return None
