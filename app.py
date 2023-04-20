import sqlite3
from datetime import date
from flask import Flask, render_template, request, url_for, flash, redirect, abort



app = Flask(__name__)

#Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
#Get specific post function

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM FoodFacts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

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

#Edit food item
@app.route('/edit/<id>/', methods=('GET', 'POST'))
def edit(id):
    foods_sel = get_post(id)
    if request.method == 'POST':
        try:
            food = request.form['food']
            calories = request.form['calories']
            carbs = request.form['carbs']
            protein = request.form['protein']
            fat = request.form['fat']
            id_f = request.form['id']
            conn = get_db_connection()
            conn.execute('UPDATE FoodFacts SET food = ?, calories = ?, protein = ?, carbs = ?, fat = ?'
                         ' WHERE id = ?',
                         (food, calories, protein, carbs, fat, id_f))
            conn.commit()
            conn.close()
            flash("Food item was edited successfully.")
            return redirect(url_for('food'))
        except sqlite3.Error as e:
            print(e)
            return "A database error occurred."
    
    return render_template('edit_food.html', foods_sel=foods_sel)

#delete food item from table
@app.route('/delete/<id>/', methods=['GET'])
def delete(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM FoodFacts WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash("Food item was deleted successfully.")
        return redirect(url_for('food'))
    except sqlite3.Error as e:
        print(e)
        return "A database error occurred."

#Add food item to daily food table  
@app.route('/add_food/<id>/', methods=('GET', 'POST'))
def add_food(id):
    foods_sel = get_post(id)
    if request.method == 'POST':
        try:
            qty = int(request.form['quantity'])
            calories = int(request.form['calories']) * qty
            carbs = int(request.form['carbs']) * qty
            protein = int(request.form['protein']) * qty
            fat = int(request.form['fat']) * qty
            datum = date.today()
            conn = get_db_connection()
            conn.execute('INSERT INTO FoodDaily (calories, protein, carbs, fat, datum) VALUES (?, ?, ?, ?, ?)',
                         (calories, protein, carbs, fat, datum))
            conn.commit()
            conn.close()
            flash("Food item was logged successfully.")
            return redirect(url_for('food'))
        except sqlite3.Error as e:
            print(e)
            return "A database error occurred."
    
    return render_template('add_food.html', foods_sel=foods_sel)






if __name__ == "__main__":
    app.run(debug=True)

