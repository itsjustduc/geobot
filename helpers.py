import requests

def post_to_fedi(instance, status, token, cw):
    response = requests.post(
    url= instance + "api/v1/statuses",
    headers={"Authorization": "Bearer " + token},
    json={"status": status, "visibility": "public", "spoiler_text": cw},
    )
    if response.status_code != 200:
        print(response.text)
