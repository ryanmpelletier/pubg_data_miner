import requests
import json

PLATFORM = "steam"
PLAYER_NAMES = "YOUR_PUBG_USERNAME"
API_KEY = "YOUR_API_KEY"
PLAYER_REQUEST_URL = "https://api.pubg.com/shards/" + PLATFORM + "/players?filter[playerNames]=" + PLAYER_NAMES
API_REQUEST_HEADERS = {
    "Authorization": ("Bearer " + API_KEY),
    "Accept": "application/vnd.api+json"
}

MATCHES_FILE = "matches.txt"
TELEMETRY_URLS_FILE = "telemetries.txt"
TELEMETRY_DIR = "telemetries"

def main():
    player_response = requests.get(PLAYER_REQUEST_URL, headers=API_REQUEST_HEADERS).json()["data"]

    # extract all match ids that are potentially new
    potentially_new_match_ids = set()
    for player in player_response:
        for match in player["relationships"]['matches']["data"]:
            potentially_new_match_ids.add(match["id"])

    #load all the match ids I already have telemetry for
    previous_match_file = open(MATCHES_FILE, "a+")
    previous_match_ids = set(previous_match_file.read().splitlines())

    #here are the ones we don't have data for
    potentially_new_match_ids.difference_update(previous_match_ids)

    #let's get all the telemetry urls
    telemetry_asset_ids = set()
    telemetry_objects = list()
    for match_id in potentially_new_match_ids:
        match_request_url="https://api.pubg.com/shards/" + PLATFORM + "/matches/" + match_id
        match_response = requests.get(match_request_url, headers=API_REQUEST_HEADERS).json()
        for asset in match_response["data"]["relationships"]["assets"]["data"]:
            telemetry_asset_ids.add(asset["id"])

        for item in match_response["included"]:
            if item["id"] in telemetry_asset_ids:
                telemetry_objects.append(item)

    #now I can go grab data for the new_match_ids using my telemetry URLs
    for telemetry_object in telemetry_objects:
        telemetry = requests.get(telemetry_object["attributes"]["URL"]).json()
        telemetry_file = open(telemetry_object["id"], 'w')
        telemetry_file.write(json.dumps(telemetry, ensure_ascii=False))

    #then I can write those matches I grabbed data for to a file
    for match_id in potentially_new_match_ids:
        previous_match_file.write(match_id + "\n")


if __name__ == "__main__": main()