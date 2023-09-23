import requests
import argparse
from http.cookiejar import MozillaCookieJar
import json
from config import cookies_file, instance, status_cw, status_text
from config import token
import time
from helpers import post_to_fedi

parser = argparse.ArgumentParser(description='summarize geo challenges')
parser.add_argument('--cid', type=str, required=True)
parser.add_argument('--cw', type=str, default=status_cw)
args = parser.parse_args()
challenge_id = args.cid
cw = args.cw

cj = MozillaCookieJar(cookies_file)
cj.load()

# antarctica {"token":challenge_id,"lat":-63.39738247529828,"lng":-56.99493795633316,"timedOut":false}

def auto_fill():
    response = requests.post("https://www.geoguessr.com/api/v3/challenges/" + challenge_id, json = {}, cookies = cj) 
    game_id = response.json()["token"]
    guess = {"token":game_id,"lat":-63.39738247529828,"lng":-56.99493795633316,"timedOut":False}
    api_url = "https://www.geoguessr.com/api/v3/games/" + game_id
    print(api_url)
    # + "?client=web"
    for i in range(1, 6):
        response = requests.get(api_url)
        print(response.text)
        print(response.status_code)
        time.sleep(4)
        response = requests.post(api_url, json = guess, cookies = cj)
        print(response.text)
        print(response.status_code)
        time.sleep(4)


challenge = requests.get("https://www.geoguessr.com/api/v3/results/highscores/" + challenge_id + "?friends=false&limit=26&minRounds=5", cookies = cj)
print(challenge.status_code)
if challenge.status_code == 401:
    auto_fill()
    challenge = requests.get("https://www.geoguessr.com/api/v3/results/highscores/" + challenge_id + "?friends=false&limit=26&minRounds=5", cookies = cj)
#print(challenge.text)
challenge_json = json.loads(challenge.text)
i = 1
summary = ""
for item in challenge_json["items"]:
    player_name = item["playerName"]
    player_score = item["totalScore"]
    summary += str(i) + ". " + player_name + " | " + str(player_score) + "\n"
    i += 1

post_to_fedi(instance, summary, token, cw)
