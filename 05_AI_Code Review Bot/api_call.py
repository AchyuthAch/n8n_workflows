import json

import requests

# URL of your webhook
url = "http://localhost:5678/webhook/code-review"

# Payload
payload = {
    "code": "def get_user(id):\n  return db.execute(f'SELECT * FROM users WHERE id={id}')",
    "language": "python",
    "context": "User lookup function for REST API",
    "pass_threshold": 9,
}

# Headers
headers = {
    "Content-Type": "application/json"
}

try:
    # Send POST request
    response = requests.post(url, json=payload, headers=headers)

    # Print response
    print("Status Code:", response.status_code)
    try:
        print("Response Body:")
        print(json.dumps(response.json(), indent=2))
    except ValueError:
        print("Response Body:", response.text)

except requests.exceptions.RequestException as e:
    print("Error:", e)
