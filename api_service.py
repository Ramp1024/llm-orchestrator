import requests
import json


def update_workflow_actions(api_url, payload, token=None):

    headers = {
        "Content-Type": "application/json"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.post(
        api_url,
        headers=headers,
        json=payload
    )

    if response.status_code not in [200, 201]:
        raise Exception(f"API call failed: {response.status_code} {response.text}")

    return response.json()