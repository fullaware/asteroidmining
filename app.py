from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Define API URL
API_URL = "http://localhost:8088"

# Define routes
@app.route("/")
def index():
    response = requests.get(f"{API_URL}/asteroids")
    asteroids = response.json()
    return render_template("index.html", asteroids=asteroids)

@app.route("/asteroids")
def asteroids():
    response = requests.get(f"{API_URL}/asteroids")
    asteroids = response.json()
    return render_template("asteroids.html", asteroids=asteroids)

@app.route("/asteroids/<int:id>")
def asteroid(id):
    response = requests.get(f"{API_URL}/asteroids/{id}")
    asteroid = response.json()
    return render_template("asteroid.html", asteroid=asteroid)

@app.route("/asteroids/<int:id>/mine", methods=["POST"])
def mine_asteroid(id):
    mining_laser_level = request.form.get("mining_laser_level")
    payload = {"mining_laser_level": mining_laser_level}
    response = requests.post(f"{API_URL}/asteroids/{id}/mine", json=payload)
    mined_resources = response.json()["resources"]
    return render_template("mine.html", mined_resources=mined_resources)

@app.route("/cargo")
def cargo():
    response = requests.get(f"{API_URL}/cargo")
    cargo = response.json()
    return render_template("cargo.html", cargo=cargo)

@app.route("/market")
def market():
    response = requests.get(f"{API_URL}/market")
    market = response.json()
    return render_template("market.html", market=market)

@app.route("/market/sell", methods=["POST"])
def sell():
    sell_items = {}
    for resource in ["iron", "gold", "platinum"]:
        quantity = request.form.get(f"{resource}_quantity")
        if quantity:
            sell_items[resource] = int(quantity)
    response = requests.post(f"{API_URL}/market/sell", json=sell_items)
    total_price = response.json()["total_price"]
    return render_template("sell.html", sell_items=sell_items, total_price=total_price)

if __name__ == "__main__":
    app.run(debug=True)
