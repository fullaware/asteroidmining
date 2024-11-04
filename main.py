from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
# add favicon route
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

# Database connection
client = AsyncIOMotorClient("mongodb://root:Candy123@10.28.28.32:27017")
db = client["game_db"]
game_state_collection = db["game_state"]
game_log_collection = db["game_log"]
high_scores_collection = db["high_scores"]

# Jinja2 Templates setup
templates = Jinja2Templates(directory="templates")

# Helper functions
async def initialize_or_get_game_state():
    """Ensure game state is initialized and return it."""
    game_state = await game_state_collection.find_one({})
    if game_state is None:
        game_state = {"shield": 100, "luck": 7, "day": 0}
        await game_state_collection.insert_one(game_state)
    return game_state

async def get_top_high_scores(limit=5):
    """Retrieve top high scores."""
    return await high_scores_collection.find().sort("days_survived", -1).limit(limit).to_list(None)

async def display_game_over(request, game_state, all_logs):
    """Display the game over screen with high scores and eligibility for submission."""
    high_scores = await get_top_high_scores()
    top_threshold = high_scores[-1]["days_survived"] if len(high_scores) == 5 else 0
    qualifies_for_high_score = game_state["day"] > top_threshold
    return templates.TemplateResponse(
        "game_over.html",
        {
            "request": request,
            "all_logs": all_logs,
            "days_survived": game_state["day"],
            "qualifies_for_high_score": qualifies_for_high_score,
            "high_scores": high_scores
        }
    )

def diceroll(sides=6):
    """Return random number from 1 up to X sides. Default=6."""
    return random.randint(1, sides)

def coin_flip():
    """Simulate a coin flip (0 or 1)."""
    return random.randint(0, 1)

async def process_day():
    """Process a single game day and update game state and logs."""
    game_state = await initialize_or_get_game_state()
    shield, luck, day = game_state["shield"], game_state["luck"], game_state["day"]

    fate, coin = diceroll(20), coin_flip()
    alerts = []

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

    game_state.update({"shield": max(0, shield), "luck": luck, "day": day + 1})
    await game_state_collection.replace_one({}, game_state)

    day_log = {
        "day": game_state["day"],
        "fate": fate,
        "luck": game_state["luck"],
        "shield": game_state["shield"],
        "alerts": alerts,
    }
    await game_log_collection.insert_one(day_log)

    return day_log

# Routes
@app.get("/", response_class=HTMLResponse)
async def game_dashboard(request: Request):
    game_state = await initialize_or_get_game_state()

    if game_state["shield"] > 0:
        await process_day()
        game_state = await game_state_collection.find_one({})
        all_logs = await game_log_collection.find().sort("day", -1).to_list(None)
        high_scores = await get_top_high_scores()
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "game_state": game_state,
                "all_logs": all_logs,
                "high_scores": high_scores
            }
        )

    all_logs = await game_log_collection.find().sort("day", -1).to_list(None)
    return await display_game_over(request, game_state, all_logs)

@app.post("/submit_score", response_class=HTMLResponse)
async def submit_score(request: Request):
    form_data = await request.form()
    player_name = form_data.get("player_name")
    game_state = await game_state_collection.find_one({})
    days_survived = game_state["day"]

    await high_scores_collection.insert_one({"name": player_name, "days_survived": days_survived})

    high_scores = await get_top_high_scores()
    reset_state = {"shield": 100, "luck": 7, "day": 0}
    await game_state_collection.replace_one({}, reset_state)
    await game_log_collection.delete_many({})

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "game_state": reset_state,
            "all_logs": [],
            "high_scores": high_scores
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
    reset_state = {"shield": 100, "luck": 7, "day": 0}
    await game_state_collection.replace_one({}, reset_state)
    await game_log_collection.delete_many({})

    high_scores = await get_top_high_scores()
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "game_state": reset_state,
            "all_logs": [],
            "high_scores": high_scores
        }
    )
