import requests

# URL of your webhook
url = "http://localhost:5678/webhook/analyze"

# Payload
payload = {
    "url": "https://www.thehindu.com/news/international/iran-israel-us-war-live-updates-25-may-2026-trump-peace-deal-pakistan/article71019686.ece" # "https://en.wikipedia.org/wiki/Artificial_intelligence" ,
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