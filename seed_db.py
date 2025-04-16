from main import db, Goal, FoodEntry, app
from datetime import date

with app.app_context():
    # Create a goal
    goal = Goal(
        user_id=1,
        goal_type="Bulk up",
        target_date="6/30/25",
        target_calories=2000
    )
    db.session.add(goal)

    # Add a few food entries for today
    today = date.today()
    food_items = [
        ("Choc. Almond Milk", 90),
        ("Avocado Toast", 290),
        ("Chicken Rice Bowl", 600),
        ("Coffee", 0)
    ]

    for name, calories in food_items:
        entry = FoodEntry(
            user_id=1,
            food_name=name,
            calories=calories,
            date=today
        )
        db.session.add(entry)

    db.session.commit()
    print("✅ Sample goal and food entries added.")
