from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
import urllib.parse
import random
import uuid

app = FastAPI()

# A ".env" file is required to connect to a MongoDB Database
# when running via "uvicorn main:app --host 0.0.0.0 --port 24318 --reload"

######### .env template #########
# DB_SERVER=10.28.28.61
# DB_USER=root
# DB_PW=Candy123
# DB_NAME=asteroidmining

load_dotenv()

if "DB_SERVER" in os.environ and "DB_USER" in os.environ and "DB_PW" in os.environ:
    db_server = os.environ['DB_SERVER']
    db_username = os.environ['DB_USER']
    db_password = urllib.parse.quote_plus(os.environ['DB_PW']) # Fix for passwords with non-alphanumeric symbols
    db_name = os.environ['DB_NAME']

    print(f"Connecting to MongoDB server {db_server} on db {db_name}\n")
else:
    print(f"\nERROR : Missing environment variables:\n")
    print(f"DB_SERVER\nDB_USER\nDB_PW\nDB_NAME\n")
    print(f"Loading .env file...\n")

    db_server = os.getenv['DB_SERVER']
    db_username = os.getenv['DB_USER']
    db_password = urllib.parse.quote_plus(os.getenv['DB_PW']) # Fix for passwords with non-alphanumeric symbols
    db_name = os.getenv['DB_NAME']


app.mount("/static", StaticFiles(directory="static"), name="static")
# add favicon route
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

# Database connection
# client = AsyncIOMotorClient("mongodb://root:Candy123@10.28.28.32:27017")
client = AsyncIOMotorClient(f"mongodb://{db_username}:{db_password}@{db_server}:27017")
db = client[db_name]
game_state_collection = db["game_state"]
game_log_collection = db["game_log"]
high_scores_collection = db["high_scores"]

# Jinja2 Templates setup
templates = Jinja2Templates(directory="templates")

async def initialize_config():
    """Ensure the configuration settings are initialized in MongoDB."""
    config = await db["config"].find_one({"_id": "game_settings"})
    
    # Default configuration values for required fields
    default_config = {
        "_id": "game_settings",
        "asteroid_discovery_chance": 0.1,  # 10% chance each day to find an asteroid
        "ship_capacity": 10000,            # Max kg the ship can carry
        "mining_rate": 500,                # Mining rate in kg per hour
        "travel_days_min": 1,              # Minimum travel time in days
        "travel_days_max": 5,              # Maximum travel time in days
        "asteroid_mass_min": 5000,         # Minimum mass of the asteroid in kg
        "asteroid_mass_max": 50000,        # Maximum mass of the asteroid in kg
        "credits_per_kg": 10               # Credits earned per kg mined
    }
    
    # If no config exists, insert the full default configuration
    if config is None:
        await db["config"].insert_one(default_config)
        return default_config
    
    # If config exists, check for and add any missing fields
    updated = False
    for key, value in default_config.items():
        if key not in config:
            config[key] = value
            updated = True
    
    # Update the config document in MongoDB if any fields were missing
    if updated:
        await db["config"].replace_one({"_id": "game_settings"}, config)

    return config



async def get_config():
    """Retrieve game configuration from MongoDB, initializing if missing."""
    config = await db["config"].find_one({"_id": "game_settings"})
    if config is None:
        config = await initialize_config()  # Initialize with default settings if not found
    return config

# Helper functions
async def initialize_or_get_game_state():
    """Ensure game state is initialized and update any missing fields."""
    game_state = await game_state_collection.find_one({})
    
    # Define the complete initial game state with all required fields
    default_game_state = {
        "shield": 100,
        "luck": 7,
        "day": 0,
        "asteroid_found": False,
        "asteroid_mass": 0,
        "asteroid_travel_days": 0,
        "ship_cargo": 0,
        "base_credits": 0
    }
    
    # Insert missing fields
    if game_state is None:
        await game_state_collection.insert_one(default_game_state)
        return default_game_state
    
    updated = False
    for key, value in default_game_state.items():
        if key not in game_state:
            game_state[key] = value
            updated = True
    
    if updated:
        await game_state_collection.replace_one({}, game_state)

    return game_state


async def get_top_high_scores(limit=5):
    """Retrieve the top high scores with UID, name, days survived, and credits earned."""
    return await high_scores_collection.find(
        {}, {"uid": 1, "name": 1, "days_survived": 1, "credits_earned": 1}
    ).sort("days_survived", -1).limit(limit).to_list(None)

async def display_game_over(request, game_state, all_logs):
    """Display the game over screen with high scores and eligibility for submission."""
    config = await get_config()  # Retrieve config to pass credits conversion, if needed
    high_scores = await get_top_high_scores()
    top_threshold = high_scores[-1]["days_survived"] if len(high_scores) == 10 else 0
    qualifies_for_high_score = game_state["day"] > top_threshold
    
    # Render the game_over template with game state, logs, high scores, and config
    return templates.TemplateResponse(
        "game_over.html",
        {
            "request": request,
            "game_state": game_state,            # Ensure game_state is passed here
            "all_logs": all_logs,
            "days_survived": game_state["day"],
            "base_credits": game_state.get("base_credits", 0),  # Default to 0 if not present
            "qualifies_for_high_score": qualifies_for_high_score,
            "high_scores": high_scores,
            "config": config
        }
    )


def diceroll(sides=6):
    """Return random number from 1 up to X sides. Default=6."""
    return random.randint(1, sides)

def coin_flip():
    """Simulate a coin flip (0 or 1)."""
    return random.randint(0, 1)

async def process_day():
    """Process a single game day with dynamic config from MongoDB."""
    game_state = await initialize_or_get_game_state()
    config = await get_config()

    shield, luck, day, asteroid_found, asteroid_mass, asteroid_travel_days, ship_cargo, base_credits = (
        game_state["shield"],
        game_state["luck"],
        game_state["day"],
        game_state["asteroid_found"],
        game_state["asteroid_mass"],
        game_state["asteroid_travel_days"],
        game_state["ship_cargo"],
        game_state["base_credits"]
    )
    alerts = []

    # Asteroid Discovery
    if not asteroid_found and random.random() < config["asteroid_discovery_chance"]:
        asteroid_found = True
        asteroid_mass = random.randint(config["asteroid_mass_min"], config["asteroid_mass_max"])
        asteroid_travel_days = random.randint(config["travel_days_min"], config["travel_days_max"])
        alerts.append({
            "message": f"Asteroid discovered with mass {asteroid_mass} kg. Travel time: {asteroid_travel_days} days.",
            "color": "blue"
        })

    # Traveling to the Asteroid
    if asteroid_found and asteroid_travel_days > 0:
        asteroid_travel_days -= 1
        alerts.append({"message": f"Traveling to asteroid. {asteroid_travel_days} days remaining.", "color": "yellow"})

    # Mining Process at the Asteroid
    elif asteroid_found and asteroid_travel_days == 0 and asteroid_mass > 0 and ship_cargo < config["ship_capacity"]:
        mining_amount = min(config["mining_rate"], asteroid_mass, config["ship_capacity"] - ship_cargo)
        asteroid_mass -= mining_amount
        ship_cargo += mining_amount
        alerts.append({
            "message": f"Mining asteroid: Mined {mining_amount} kg. Ship cargo: {ship_cargo}/{config['ship_capacity']} kg.",
            "color": "green"
        })

        # Check if asteroid is depleted or ship is full
        if asteroid_mass == 0:
            alerts.append({"message": "Asteroid depleted.", "color": "red"})
            asteroid_found = False
        elif ship_cargo >= config["ship_capacity"]:
            # Return to base, transfer cargo to credits, and repair ship
            earned_credits = ship_cargo * config["credits_per_kg"]
            base_credits += earned_credits
            shield = 100
            ship_cargo = 0
            alerts.append({
                "message": f"Cargo transferred to base. Earned {earned_credits} credits. Shield repaired to 100.",
                "color": "purple"
            })
            asteroid_found = False

    # Regular Game Events (e.g., shield/luck management)
    fate = diceroll(20)
    coin = coin_flip()
    dodge_chance = min(0.3 + (luck * 0.05), 0.85)
    dodged = random.random() < dodge_chance

    if coin == 0 and not dodged:  # Bad outcome, direct hit
        damage = diceroll(4) + 3
        shield -= damage
        luck = max(0, luck - 1)
        alerts.append({"message": f"Direct hit! Shield reduced by {damage}", "color": "red"})
    elif coin == 1 and not dodged:  # Minor impact on good outcome
        damage = diceroll(2)
        shield -= damage
        alerts.append({"message": f"Minor impact on shield by {damage}", "color": "yellow"})
    elif dodged:
        alerts.append({"message": "Successful evasion!", "color": "green"})

    # Update game state with new values
    game_state.update({
        "shield": max(0, shield),
        "luck": luck,
        "day": day + 1,
        "asteroid_found": asteroid_found,
        "asteroid_mass": asteroid_mass,
        "asteroid_travel_days": asteroid_travel_days,
        "ship_cargo": ship_cargo,
        "base_credits": base_credits
    })
    await game_state_collection.replace_one({}, game_state)

    # Log the day's result
    day_log = {
        "day": game_state["day"],
        "fate": fate,
        "luck": game_state["luck"],
        "shield": game_state["shield"],
        "alerts": alerts,
        "asteroid_mass": asteroid_mass,
        "ship_cargo": ship_cargo,
        "base_credits": base_credits
    }
    await game_log_collection.insert_one(day_log)

    return day_log



# Routes
async def get_top_high_scores(limit=5):
    """Retrieve the top high scores with name, days survived, and credits earned."""
    return await high_scores_collection.find().sort("days_survived", -1).limit(limit).to_list(None)

# Example usage in routes
@app.get("/", response_class=HTMLResponse)
async def game_dashboard(request: Request):
    # Retrieve current game state and configuration
    game_state = await initialize_or_get_game_state()
    config = await get_config()
    
    # Progress the game by one day if shield is greater than zero
    if game_state["shield"] > 0:
        await process_day()  # Process a new day
        game_state = await game_state_collection.find_one({})  # Re-fetch updated game state
        all_logs = await game_log_collection.find().sort("day", -1).to_list(None)  # Get all logs
        high_scores = await get_top_high_scores()  # Retrieve top high scores

        # Render the dashboard with updated game state, logs, high scores, and config
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "game_state": game_state,
                "all_logs": all_logs,
                "high_scores": high_scores,
                "config": config
            }
        )

    # If shield is zero or below, display the game over screen
    all_logs = await game_log_collection.find().sort("day", 1).to_list(None)
    return await display_game_over(request, game_state, all_logs)




@app.post("/submit_score", response_class=HTMLResponse)
async def submit_score(request: Request):
    form_data = await request.form()
    player_name = form_data.get("player_name")
    game_state = await game_state_collection.find_one({})
    config = await get_config()
    high_scores = await get_top_high_scores()

    # Generate a unique UID for the player
    player_uid = str(uuid.uuid4())

    # Insert score in the database with UID, name, days survived, and credits
    high_score_entry = {
        "uid": player_uid,
        "name": player_name,
        "days_survived": game_state["day"],
        "credits_earned": game_state.get("base_credits", 0)
    }
    await high_scores_collection.insert_one(high_score_entry)

    # Define reset_state properly as a dictionary
    reset_state = {
        "shield": 100,
        "luck": 7,
        "day": 0,
        "asteroid_found": False,
        "asteroid_mass": 0,
        "asteroid_travel_days": 0,
        "ship_cargo": 0,
        "base_credits": 0
    }

    # Reset the game state and clear the logs
    await game_state_collection.replace_one({}, reset_state)
    await game_log_collection.delete_many({})

    # Render the dashboard with the reset game state, high scores, and config
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "game_state": reset_state,
            "high_scores": high_scores,
            "config": config
        }
    )




@app.post("/auto_play", response_class=HTMLResponse)
async def auto_play(request: Request):
    game_state = await initialize_or_get_game_state()
    while game_state["shield"] > 0:
        await process_day()
        game_state = await game_state_collection.find_one({})

    all_logs = await game_log_collection.find().sort("day", -1).to_list(None)
    return await display_game_over(request, game_state, all_logs)

@app.post("/play_again", response_class=HTMLResponse)
async def play_again(request: Request):
    # Define the reset game state
    reset_state = {
        "shield": 100,
        "luck": 7,
        "day": 0,
        "asteroid_found": False,
        "asteroid_mass": 0,
        "asteroid_travel_days": 0,
        "ship_cargo": 0,
        "base_credits": 0
    }

    # Reset the game state in the database
    await game_state_collection.replace_one({}, reset_state)
    await game_log_collection.delete_many({})  # Clear game logs

    # Retrieve config and high scores for rendering the dashboard
    config = await get_config()
    high_scores = await get_top_high_scores()

    # Render the dashboard with the reset game state, high scores, and config
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "game_state": reset_state,
            "high_scores": high_scores,
            "config": config  # Ensure config is passed here
        }
    )

from fastapi.responses import RedirectResponse

@app.get("/player_logs/{uid}", response_class=HTMLResponse)
async def player_logs(request: Request, uid: str):
    # Retrieve player logs by UID
    player_data = await db["player_logs"].find_one({"uid": uid})
    high_scores = await get_top_high_scores()

    if not player_data:
        # Redirect to an error page or the dashboard if the player is not found
        return RedirectResponse(url="/")

    # Render the logs in the player_logs template
    return templates.TemplateResponse(
        "player_logs.html",
        {
            "request": request,
            "player_name": player_data["name"],
            "days_survived": player_data["days_survived"],
            "credits_earned": player_data["credits_earned"],
            "logs": player_data["logs"],
            "high_scores": high_scores
        }
    )






@app.get("/resetbutton")
async def reset_high_scores(request: Request):
    # Delete all documents in the high scores collection
    await high_scores_collection.delete_many({})

    # Optional: return to dashboard or provide a success message
    return "High scores have been reset successfully."
