from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os

app = Flask(__name__)
config_path = os.path.join(os.path.dirname(__file__), "config.py")
app.config.from_pyfile(config_path)
db = SQLAlchemy(app)

# ---------- MODELS ----------
class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    target_calories = db.Column(db.Integer)
    target_date = db.Column(db.String(20))
    goal_type = db.Column(db.String(20))

class FoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    food_name = db.Column(db.String(100))
    calories = db.Column(db.Integer)
    date = db.Column(db.Date)

# ---------- ROUTES ----------
@app.route("/")
def home():
    user_id = 1
    goal = Goal.query.filter_by(user_id=user_id).first()
    today = date.today()
    entries = FoodEntry.query.filter_by(user_id=user_id, date=today).all()
    total = sum(e.calories for e in entries)
    food_log = [f"{e.food_name} - {e.calories} cal" for e in entries]

    calorie_history = {
        "labels": ["2/20", "2/27", "3/6", "3/13", "3/20"],
        "values": [1200, 1400, 2000, 1800, 1900]
    }

    return render_template("home.html", goal=goal, total_consumed=total, food_log=food_log, calorie_history=calorie_history)

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/tracker")
def tracker():
    return render_template("tracker.html")

# ---------- ENTRY POINT ----------
if __name__ == '__main__':
    app.run(debug=True)
