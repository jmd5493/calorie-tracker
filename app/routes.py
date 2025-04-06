from flask import Blueprint, render_template

# Define a Blueprint for the routes
app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def index():
    return render_template('index.html')

@app_routes.route('/profile')
def profile():
    return render_template('profile.html')

@app_routes.route('/tracker')
def tracker():
    return render_template('tracker.html')

@app_routes.route('/goals')
def goals():
    return render_template('goals.html')