from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from datetime import datetime
import os
import sqlite3
import util

app = Flask(__name__, static_folder='static')

config_path = os.path.join(os.path.dirname(__file__), "config.py")
app.config.from_pyfile(config_path)
db = SQLAlchemy(app)

# Postgres/Sql database details.
# evil global variables
# can be placed in a config file
# here is a possible tutorial how you can do this
username='postgres'
password='admin'
host='127.0.0.1'
port='5432'
database='calorie_tracker'

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

@app.route('/save_goal', methods=['POST'])
def save_goal():
    conn = sqlite3.connect('calorie_tracker.db')
    cursor = conn.cursor()

    # Create the data in goal table if not exist
    cursor.execute("Insert into goal (user_id, target_calories, target_date, goal_type) values (1, 2000, '6/30/25', 'Bulk up')")
    conn.commit()

    # Retrieve data from database to display in profile page.
    cursor.execute("Select * FROM goal")
    data = cursor.fetchall()

    conn.close()
    return render_template("profile.html",data=data)

@app.route("/tracker")
def tracker():
    user_id = 1
    data = FoodEntry.query.filter_by(user_id=user_id).order_by(FoodEntry.date).all()
    return render_template("tracker.html", data=data)

@app.route("/add_entry/", methods=['POST'])
def add_entry():
    food = FoodEntry(user_id=1,
                     food_name=request.form.get('food_name'),
                     calories=int(request.form.get('calories')),
                     date=datetime.strptime(request.form.get('date'), '%Y-%m-%d')
                     )

    db.session.add(food)
    db.session.commit()
    return redirect(url_for("tracker"))

@app.route("/update_entry/<int:id>", methods=['POST'])
def update_entry(id):
    food = FoodEntry.query.get(id)
    food.food_name = request.form.get('food_name', food.food_name)
    food.calories = request.form.get('calories', food.calories)
    food.date = datetime.strptime(request.form.get('date', food.date), '%Y-%m-%d')
    db.session.commit()
    return redirect(url_for("tracker"))

@app.route("/delete_entry/<int:id>", methods=['POST'])
def delete_entry(id):
    food = FoodEntry.query.get(id)
    db.session.delete(food)
    db.session.commit()
    return redirect(url_for("tracker"))

@app.route("/test-db")
def test_db():
    entries = FoodEntry.query.all()
    output = "<h2>Food Entries:</h2>"
    for e in entries:
        output += f"<p>{e.food_name} - {e.calories} cal</p>"
    return output

# route is used to map a URL with a Python function
# complete address: ip:port/
# 127.0.0.1:5000/
@app.route('/getSampleData', methods=['GET'])
# this is how you define a function in Python
def getSampleData():
    # this is your index page
    # connect to DB
    cursor, connection = util.connect_to_db(username,password,host,port,database)
    # execute SQL commands
    record = util.run_and_fetch_sql(cursor, "SELECT * from sample;")
    if record == -1:
        # you can replace this part with a 404 page
        print('Something is wrong with the SQL command')
    else:
        # this will return all column names of the select result table
        # ['customer_id','store_id','first_name','last_name','email','address_id','activebool','create_date','last_update','active']
        col_names = [desc[0] for desc in cursor.description]
        # only use the first five rows
        log = record[:5]
        # log=[[1,2],[3,4]]
    # disconnect from database
    util.disconnect_from_db(connection,cursor)
    # using render_template function, Flask will search
    # the file named index.html under templates folder
    return render_template('getSampleData.html', sql_table = log, table_title=col_names)


# default page for 404 error
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404_error.html'), 404

# default page for 500 error
@app.errorhandler(500)
def server_error(e):
	print(e)
	return render_template('500_error.html'), 500



# ---------- ENTRY POINT ----------
if __name__ == '__main__':
    app.run(debug=True)
