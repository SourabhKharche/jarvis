import requests

response = requests.post(
    "http://127.0.0.1:5000/ai-process",
    json={"command": "Make a note that I need to buy ice cream!"}
)

print("Status Code:", response.status_code)
print("Response Body:", response.text)
