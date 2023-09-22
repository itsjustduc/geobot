import requests
from http.cookiejar import MozillaCookieJar
import json
from keys import token
import os

# geo options
moving = True
panning = True
zooming = True
time_limit = 180 # seconds
map_url = "https://www.geoguessr.com/maps/62a44b22040f04bd36e8a914"
cookies_file = "cookies-geoguessr-com.txt" # path to cookies file

# fedi options
instance = "https://quack.duc.gay/" # include trailing slash !!!!
status_text = "New GeoGuessr daily challenge!" # text before URL in status
status_cw = "GeoGuessr Daily Fedi Challenge" # text to use as cw for post

# convert map url to just id
map_id = map_url.split("/")[-1]

def generate_challenge():
    cj = MozillaCookieJar(cookies_file)
    cj.load()
    api_url = "https://www.geoguessr.com/api/v3/challenges"
    challenge_options = {"map":map_id,"forbidMoving": not moving,"forbidRotating": not panning,"forbidZooming": not zooming,"timeLimit": time_limit}
    x = requests.post(api_url, json = challenge_options, cookies = cj)
    print(x.text)
    return x.json()

#generate_challenge()

def post_to_fedi(instance, status, token):
    response = requests.post(
    url= instance + "api/v1/statuses",
    headers={"Authorization": "Bearer " + token},
    json={"status": status, "visibility": "public", "spoiler_text": status_cw},
    )
    if response.status_code != 200:
        print(response.text)
    
def run():
    challenge_id = generate_challenge()["token"]
    base_url = "https://www.geoguessr.com/challenge/"
    challenge_url = base_url + challenge_id
    status = status_text + " " + challenge_url
    print(status)
    post_to_fedi(instance, status, token)
    
run()
