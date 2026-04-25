from flask import Flask, jsonify
import requests
import base64
import os

app = Flask(__name__)

SECRET_KEY = os.getenv("PAYMONGO_SECRET")

def auth():
    return base64.b64encode((SECRET_KEY + ":").encode()).decode()

# CREATE CHECKOUT
@app.route("/create-checkout")
def create_checkout():

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
                "success_url": "https://your-frontend-url/success.html",
                "cancel_url": "https://your-frontend-url/cancel.html"
            }
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic " + auth()
    }

    res = requests.post(url, json=payload, headers=headers).json()

    return jsonify({
        "checkout_url": res["data"]["attributes"]["checkout_url"],
        "checkout_id": res["data"]["id"]
    })

# VERIFY PAYMENT
@app.route("/verify/<checkout_id>")
def verify(checkout_id):

    url = f"https://api.paymongo.com/v1/checkout_sessions/{checkout_id}"

    headers = {
        "Authorization": "Basic " + auth()
    }

    res = requests.get(url, headers=headers).json()

    try:
        status = res["data"]["attributes"]["payment_intent"]["attributes"]["status"]
    except:
        return jsonify({"paid": False})

    if status == "succeeded":
        return jsonify({"paid": True})
    else:
        return jsonify({"paid": False})

# REQUIRED FOR RAILWAY
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)