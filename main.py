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
    try:
        # Connect to the database
        cursor, connection = util.connect_to_db(username, password, host, port, database)
        print("entered profile page")

        # Fetch all records from the Profile table
        query = "SELECT name, Age, Weight, Goal, Target_date FROM Profile"
        print("Prepared query:", query)

        cursor.execute(query)
        profile = cursor.fetchone()

        target_date = profile[4]  # The Target_date column from the database (as a string)
        current_date = datetime.now().date()

        # Calculate the difference in days
        days_remaining = (target_date - current_date).days
        profile = profile + (days_remaining,)

        print("Profiles fetched from the database:", profile)

    except Exception as e:
        print("Error while fetching profiles:", str(e))
        profiles = None  # Set profiles to empty in case of error

    finally:
        # Disconnect from the database
        util.disconnect_from_db(connection, cursor)

    # Pass the fetched profile to the template
    return render_template('profile.html', profile=profile)


@app.route('/edit_goal')
def edit_goal():
    return render_template('AddEditGoal.html')

@app.route('/api/save_goal', methods=['POST'])
def save_goal():
    # this is your save goal page

    # Get form data
    name = request.form.get('name', '').strip()  # Strip whitespace

    age = int(request.form.get('age', 0))  # Default to 0 if not provided
    weight = int(request.form.get('weight', 0))

    goal = request.form.get('goal-type', '').strip()

    try:
        target_date = datetime.strptime(request.form.get('target_date', ''), '%m/%d/%Y').strftime('%Y-%m-%d')
    except ValueError:
        target_date = None

    # connect to DB
    cursor, connection = util.connect_to_db(username, password, host, port, database)

    # chck if the record exist

    # Retrieve data from database to display in profile page.
    # execute SQL commands
    record = util.run_and_fetch_sql(cursor, "SELECT * from profile;")
    print(record)

    print('There is no record in the database - creating a new record')
    try:
        query = """
        INSERT INTO Profile (user_id, name, age, goal, weight, target_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (1, name, age, goal, weight, target_date)

        print("Prepared query:", query)
        print("With values:", values)

        cursor.execute(query, values)
        connection.commit()

        # util.run_and_fetch_sql(cursor, query, values)
    except Exception as e:
        print("Error while inserting data:", str(e))

    # if record == -1:
    #     # if rec does NOT exist then create a new record
    #     print('There is no record in the database - creating a new record')
    #     util.run_and_fetch_sql(cursor, "INSERT INTO Profile(name, Age, Weight, Goal, Target_date) VALUES('"+name+"', "+age+", "+weight+", "+goal+", "+target_date+");")
    #     # ("INSERT INTO Profile(name, Age, Weight, Goal, Target_date) VALUES('Alice', 25, 65, 'TrimDown', '2025-06-01');")
    # else:
    #     # Rec do exist update the values
    #     # if rec exist then update the existing record with values
    #     print('There isexisting profile/goal record in the database, Updating the values')
    #     util.run_and_fetch_sql(cursor,
    #                        "UPDATE Profile SET name = '" + name +
    #                        "', Age = " + age +
    #                        ", Weight = " + weight +
    #                        ", Goal = '" + goal +
    #                        "', Target_date = '" + target_date +
    #                        "' WHERE User_Id = " + 1 + ";"
    #                        )

    # Retrieve data from database to display in profile page.
    # execute SQL commands
    record = util.run_and_fetch_sql(cursor, "SELECT * from profile;")
    print(record)

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
    util.disconnect_from_db(connection, cursor)
    # using render_template function, Flask will search
    # the file named index.html under templates folder
    return render_template('profile.html', data=record)

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

@app.route("/update_entry/<int:id>", methods=['PUT'])
def update_entry(id):
    food = FoodEntry.query.get(id)
    food.food_name = request.form.get('food_name', food.food_name)
    food.calories = request.form.get('calories', food.calories)
    food.date = datetime.strptime(request.form.get('date', food.date), '%Y-%m-%d')
    db.session.commit()
    return redirect(url_for("tracker"))

@app.route("/delete_entry/<int:id>", methods=['DELETE'])
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
