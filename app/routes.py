from flask import Blueprint, render_template
from datetime import date
from .models import Goal, FoodEntry
from app.extensions import db

app_routes = Blueprint('app_routes', __name__)

@app_routes.route("/")
def home():
    user_id = 1  # Placeholder user until login is wired up

    # Get the user's goal
    goal = Goal.query.filter_by(user_id=user_id).first()

    # Get today's food entries
    today = date.today()
    food_entries = FoodEntry.query.filter_by(user_id=user_id, date=today).all()

    # Calculate total calories consumed today
    total_consumed = sum(entry.calories for entry in food_entries)

    # Build a food log list
    food_log = [f"{entry.food_name} - {entry.calories} cal" for entry in food_entries]

    # Mock calorie history for chart (replace later with real data)
    calorie_history = {
        "labels": ["2/20", "2/27", "3/6", "3/13", "3/20"],
        "values": [1200, 1400, 2000, 1800, 1900]
    }

    return render_template("home.html",
        goal=goal,
        total_consumed=total_consumed,
        food_log=food_log,
        calorie_history=calorie_history
    )

@app_routes.route("/profile")
def profile():
    return render_template("profile.html")

@app_routes.route("/tracker")
def tracker():
    return render_template("tracker.html")

@app_routes.route("/goals")
def goals():
    return render_template("goals.html")
