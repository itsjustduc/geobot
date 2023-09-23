import requests
from http.cookiejar import MozillaCookieJar
import json
from config import token
#from config import cookies_file, instance, status_cw, status_text
#from config import moving_conf, panning_conf, zooming_conf, time_limit, map_url
import config
import argparse
import subprocess
import os
from helpers import post_to_fedi

parser = argparse.ArgumentParser(description='geo challenge generator')
parser.add_argument('-m', '--moving', type=int, default=config.moving)
parser.add_argument('-p', '--panning', type=int, default=config.panning)
parser.add_argument('-z', '--zooming', type=int, default=config.zooming)
parser.add_argument('-t', '--time', type=int, default=config.time_limit)
parser.add_argument('--map', type=str, default=config.map_url)
parser.add_argument('--status', type=str, default=config.status_text)
parser.add_argument('--cw', type=str, default=config.status_cw)


args = parser.parse_args()
moving = bool(args.moving)
panning = args.panning
zooming = args.zooming
time_limit = args.time
map_url = args.map
status_text = args.status
status_cw = args.cw



# convert map url to just id
map_id = map_url.split("/")[-1]

def generate_challenge():
    cj = MozillaCookieJar(config.cookies_file)
    cj.load()
    api_url = "https://www.geoguessr.com/api/v3/challenges"
    challenge_options = {"map":map_id,"forbidMoving": not moving,"forbidRotating": not panning,"forbidZooming": not zooming,"timeLimit": time_limit}
    x = requests.post(api_url, json = challenge_options, cookies = cj)
    print(x.text)
    return x.json()

    
def run():
    challenge_id = generate_challenge()["token"]
    base_url = "https://www.geoguessr.com/challenge/"
    challenge_url = base_url + challenge_id
    status = status_text + " " + challenge_url
    print(status)
    post_to_fedi(config.instance, status, token, status_cw)
    
    summary_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "summary.py")
    command = 'echo \'cd ' + os.path.dirname(os.path.abspath(__file__)) + ' && python3 '+ summary_file + ' --cid="' + challenge_id + '" --cw="' + status_cw + ' (summary)" >> logs 2>&1\' | at ' + config.at_cmd
    subprocess.Popen(command, shell=True)
    
run()
