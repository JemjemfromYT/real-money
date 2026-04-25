from flask import Flask, jsonify
import requests
import base64
import os

app = Flask(__name__)

SECRET_KEY = os.getenv("PAYMONGO_SECRET")

def auth():
    return base64.b64encode((SECRET_KEY + ":").encode()).decode()

@app.route("/create-checkout")
def checkout():

    url = "https://api.paymongo.com/v1/checkout_sessions"

    payload = {
        "data": {
            "attributes": {
                "line_items": [{
                    "currency": "PHP",
                    "amount": 5000,
                    "name": "Premium Item",
                    "quantity": 1
                }],
                "payment_method_types": ["gcash"],
                "success_url": "https://your-site.github.io/success.html?paid=true",
                "cancel_url": "https://your-site.github.io/cancel.html"
            }
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic " + auth()
    }

    res = requests.post(url, json=payload, headers=headers)

    return jsonify(res.json())

app.run(host="0.0.0.0", port=10000)