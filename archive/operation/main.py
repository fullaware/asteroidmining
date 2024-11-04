from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.templating import Jinja2Templates
from testLuck import diceroll, coin_flip, random_window
import random

app = FastAPI()

# Database connection
client = AsyncIOMotorClient("mongodb://root:Candy123@10.28.28.32:27017")
db = client["game_db"]
game_state_collection = db["game_state"]
game_log_collection = db["game_log"]
players_collection = db["player"]

# Jinja2 Templates setup
templates = Jinja2Templates(directory="templates")

async def initialize_game_state():
    # Check if game state already exists
    game_state = await game_state_collection.find_one({"name": "Player1"})
    if not game_state:
        # Initialize game state
        game_state = {
            "name": "Player1",
            "shield": 100,
            "luck": 7,
            "day": 0,
        }
        await game_state_collection.insert_one(game_state)

@app.on_event("startup")
async def startup_event():
    await initialize_game_state()

async def process_day():
    # Retrieve the current game state
    game_state = await game_state_collection.find_one({"name": "Player1"})
    
    if not game_state:
        game_state = {"name": "Player1", "shield": 100, "luck": 7, "day": 0}
        await game_state_collection.insert_one(game_state)
    
    # Extract values
    shield = game_state["shield"]
    luck = game_state["luck"]
    day = game_state["day"]

    # Only process if shield > 0
    if shield > 0:
        fate = diceroll(20)
        coin = coin_flip()
        alerts = []

        # Dodge and damage logic
        dodge_chance = min(0.3 + (luck * 0.05), 0.85)
        dodged = random.random() < dodge_chance

        if coin == 0:  # Bad outcome
            if dodged:
                alerts.append({"message": "Barely dodged a hit!", "color": "green"})
            else:
                damage = diceroll(4) + 3
                shield -= damage
                alerts.append({"message": f"Direct hit! Shield reduced by {damage}", "color": "red"})
                luck = max(0, luck - 1)
        else:  # Good outcome
            if dodged:
                alerts.append({"message": "Smooth evasion!", "color": "blue"})
            else:
                damage = diceroll(2)
                shield -= damage
                alerts.append({"message": f"Minor impact on shield by {damage}", "color": "yellow"})

        # Update game state
        game_state["shield"] = max(0, shield)
        game_state["luck"] = luck
        game_state["day"] = day + 1

        # Save updated game state
        await game_state_collection.replace_one({"name": "Player1"}, game_state)

        # Log the day's result
        day_log = {
            "day": game_state["day"],
            "fate": fate,
            "luck": game_state["luck"],
            "shield": game_state["shield"],
            "alerts": alerts,
        }
        await game_log_collection.insert_one(day_log)

        # If shield reaches 0, save high score
        if game_state["shield"] <= 0:
            await save_high_score(game_state["day"])

        return day_log

async def save_high_score(days_survived):
    # Prompt player to enter their name (could be adapted to a form)
    player_name = "Player1"  # Simplified for now; this could be input from the player

    high_score_entry = {
        "name": player_name,
        "days_survived": days_survived,
    }
    await db["high_scores"].insert_one(high_score_entry)



    

@app.get("/", response_class=HTMLResponse)
async def game_dashboard(request: Request):
    # Retrieve the current game state
    game_state = await game_state_collection.find_one({"name": "Player1"})
    
    # Check if the game is already over
    if game_state["shield"] <= 0:
        # Fetch high scores to display on game over screen
        high_scores = await db["high_scores"].find().sort("days_survived", -1).to_list(10)
        return templates.TemplateResponse(
            "game_over.html",
            {"request": request, "high_scores": high_scores, "days_survived": game_state["day"]}
        )

    # Otherwise, continue the game and process the day
    day_log = await process_day()

    # Retrieve all logs in descending order to show the most recent at the top
    all_logs = await game_log_collection.find().sort("day", -1).to_list(None)
    
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "game_state": game_state, "all_logs": all_logs}
    )

@app.post("/submit_score", response_class=HTMLResponse)
async def submit_score(request: Request):
    form_data = await request.form()
    player_name = form_data.get("player_name")

    # Retrieve the current game state
    game_state = await game_state_collection.find_one({"name": "Player1"})
    days_survived = game_state["day"]

    # Save high score
    high_score_entry = {
        "name": player_name,
        "days_survived": days_survived,
    }
    await db["high_scores"].insert_one(high_score_entry)

    # Reset the game state for a new game
    reset_state = {"name": "Player1", "shield": 100, "luck": 7, "day": 0}
    await game_state_collection.replace_one({"name": "Player1"}, reset_state)

    # Clear the game log collection
    await game_log_collection.delete_many({})

    # Redirect to the main dashboard to start a new game
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "game_state": reset_state, "all_logs": []}
    )


@app.post("/auto_play", response_class=HTMLResponse)
async def auto_play(request: Request):
    # Retrieve the current game state
    game_state = await game_state_collection.find_one({"name": "Player1"})

    # Auto-play until shield reaches zero
    while game_state["shield"] > 0:
        # Process one day at a time
        await process_day()
        # Retrieve the updated game state after each day
        game_state = await game_state_collection.find_one({"name": "Player1"})

    # Once shield reaches zero, retrieve all daily logs
    all_logs = await game_log_collection.find().sort("day", 1).to_list(None)

    # Check if the player's days survived qualify for the top 10
    high_scores = await db["high_scores"].find().sort("days_survived", -1).limit(10).to_list(10)
    top_10_threshold = high_scores[-1]["days_survived"] if len(high_scores) == 10 else 0
    qualifies_for_high_score = game_state["day"] > top_10_threshold

    # Show the game over screen with logs and high score option if eligible
    return templates.TemplateResponse(
        "game_over.html",
        {
            "request": request,
            "all_logs": all_logs,
            "days_survived": game_state["day"],
            "qualifies_for_high_score": qualifies_for_high_score,
            "high_scores": high_scores,
        }
    )

@app.post("/play_again", response_class=HTMLResponse)
async def play_again(request: Request):
    # Reset the game state for a new game
    reset_state = {"name": "Player1", "shield": 100, "luck": 7, "day": 0}
    await game_state_collection.replace_one({"name": "Player1"}, reset_state)

    # Clear the game log collection
    await game_log_collection.delete_many({})

    # Redirect to the main dashboard to start a new game
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "game_state": reset_state, "all_logs": []}
    )
