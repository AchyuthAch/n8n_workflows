import requests

# URL of your webhook
url = "http://localhost:5678/webhook/sentiment"

# Payload
payload = {
    "text": "The movie is really bad", "context": "Entertainment", #"I absolutely love this product, it changed my life!", "context": "product review",
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
    print("Response Body:", response.text)

except requests.exceptions.RequestException as e:
    print("Error:", e)