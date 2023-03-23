from flask import Flask, jsonify, request

app = Flask(__name__)

# Define asteroid data
asteroids = [
    {
        "id": 1,
        "name": "Asteroid A",
        "resources": {
            "iron": 20,
            "gold": 5,
            "platinum": 3
        }
    },
    {
        "id": 2,
        "name": "Asteroid B",
        "resources": {
            "iron": 30,
            "gold": 2,
            "platinum": 1
        }
    },
    {
        "id": 3,
        "name": "Asteroid C",
        "resources": {
            "iron": 10,
            "gold": 8,
            "platinum": 2
        }
    }
]

# Define cargo data
cargo = {
    "iron": 0,
    "gold": 0,
    "platinum": 0
}

# Define market prices
market = {
    "iron": 2,
    "gold": 10,
    "platinum": 50
}

# Define upgrade costs
upgrade_costs = {
    "mining_laser_level": [10, 50, 100],
    "cargo_hold_size": [10, 50, 100]
}

# Define mining function
def mine_asteroid(asteroid_id, mining_laser_level):
    for asteroid in asteroids:
        if asteroid["id"] == asteroid_id:
            resources = asteroid["resources"]
            mined_resources = {}
            for resource, quantity in resources.items():
                mined_quantity = quantity // (mining_laser_level + 1)
                mined_resources[resource] = mined_quantity
                resources[resource] -= mined_quantity
            return mined_resources
    return None

# Define routes
@app.route("/asteroids", methods=["GET"])
def get_asteroids():
    return jsonify(asteroids)

@app.route("/asteroids/<int:id>", methods=["GET"])
def get_asteroid(id):
    for asteroid in asteroids:
        if asteroid["id"] == id:
            return jsonify(asteroid)
    return jsonify({"message": "Asteroid not found"}), 404

@app.route("/asteroids/<int:id>/mine", methods=["POST"])
def mine_asteroid_route(id):
    mining_laser_level = request.json.get("mining_laser_level")
    mined_resources = mine_asteroid(id, mining_laser_level)
    if mined_resources is None:
        return jsonify({"message": "Asteroid not found"}), 404
    for resource, quantity in mined_resources.items():
        cargo[resource] += quantity
    return jsonify({"resources": mined_resources})

@app.route("/cargo", methods=["GET"])
def get_cargo():
    return jsonify(cargo)

@app.route("/cargo", methods=["POST"])
def store_resources():
    for resource, quantity in request.json.items():
        if resource not in cargo:
            return jsonify({"message": "Invalid resource"}), 400
        if quantity < 0:
            return jsonify({"message": "Quantity must be positive"}), 400
        cargo[resource] += quantity
    return jsonify({"message": "Resources stored"})

@app.route("/market", methods=["GET"])
def get_market_prices():
    return jsonify(market)

@app.route("/market/sell", methods=["POST"])
def sell_resources():
    total_price = 0
    for resource, quantity in request.json.items():
        if resource not in cargo:
            return jsonify

if __name__ == "__main__":
    app.run(debug=True, port=8088)
