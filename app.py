import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort



app = Flask(__name__)

#Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():

    return "Init app!"

#Add food item
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        try:
            food = request.form['food']
            calories = request.form['calories']
            carbs = request.form['carbs']
            protein = request.form['protein']
            fat = request.form['fat']
            conn = get_db_connection()
            conn.execute('INSERT INTO FoodFacts (food, calories, protein, carbs, fat) VALUES (?, ?, ?, ?, ?)',
                         (food, calories, protein, carbs, fat))
            conn.commit()
            conn.close()
            flash("New food item was added successfully.")
            return redirect(url_for('food'))
        except sqlite3.Error as e:
            print(e)
            return "A database error occurred."
    return render_template('create.html')










if __name__ == "__main__":
    app.run(debug=True)

