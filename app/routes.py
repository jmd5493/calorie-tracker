from flask import Blueprint, render_template

app_routes = Blueprint('app_routes', __name__)

@app_routes.route("/")
def home():
    return render_template("home.html")

@app_routes.route("/profile")
def profile():
    return render_template("profile.html")

@app_routes.route("/tracker")
def tracker():
    return render_template("tracker.html")

@app_routes.route("/goals")
def goals():
    return render_template("goals.html")
