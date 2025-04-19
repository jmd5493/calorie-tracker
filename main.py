from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os
import sqlite3

app = Flask(__name__, static_folder='static')

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

    def __repr__(self):
        return f"ID: {self.id}, User: {self.user_id}, Food: {self.food_name}, Calories: {self.calories}, Date: {self.date}"

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

@app.route('/edit_goal')
def edit_goal():
    return render_template('AddEditGoal.html')

@app.route("/tracker", methods=['GET'])
def tracker():
    conn = sqlite3.connect('calorie_tracker.db')
    cursor = conn.cursor()
    cursor.execute("Select * FROM food_entry")
    data = cursor.fetchall()
    conn.close()
    return render_template("tracker.html", data=data)

@app.route("/test-db")
def test_db():
    entries = FoodEntry.query.all()
    output = "<h2>Food Entries:</h2>"
    for e in entries:
        output += f"<p>{e.food_name} - {e.calories} cal</p>"
    return output

# @app.route("/reset-db")
# def reset_db():
#     # Delete everything from both tables
#     FoodEntry.query.delete()
#     Goal.query.delete()
#     db.session.commit()
#     return "<h3>✅ All data wiped from FoodEntry and Goal tables.</h3>"


# ---------- ENTRY POINT ----------
if __name__ == '__main__':
    app.run(debug=True)
