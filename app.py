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

#Get specific exercise from table
def get_exercise(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM ExerciseLogs1 WHERE weekid = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

#Home dashboard
@app.route("/")
def home():
    try:
        datum = date.today()
        today = datum.strftime('%Y-%m-%d')
        conn = get_db_connection()
        todo_sql = "SELECT * FROM Todo"
        shopping_sql = "SELECT * FROM Shopping"
        group_sql = "SELECT SUM(calories) FROM FoodDaily GROUP BY datum ORDER BY datum DESC"
        cal_sql = "SELECT SUM(calories) FROM FoodDaily WHERE datum=?"
        pro_sql = "SELECT SUM(protein) FROM FoodDaily WHERE datum=?"
        carb_sql = "SELECT SUM(carbs) FROM FoodDaily WHERE datum=?"
        fat_sql = "SELECT SUM(fat) FROM FoodDaily WHERE datum=?"

        todo = conn.execute(todo_sql).fetchall()
        shopping = conn.execute(shopping_sql).fetchall()
        fats = conn.execute(fat_sql, (today,)).fetchall()
        carbs = conn.execute(carb_sql, (today,)).fetchall()
        pros = conn.execute(pro_sql, (today,)).fetchall()
        cals = conn.execute(cal_sql, (today,)).fetchall()
        grupa = conn.execute(group_sql).fetchall()
        conn.close()
        return render_template('index.html', cals=cals, grupa=grupa, pros=pros, carbs=carbs, fats=fats, shopping=shopping, todo=todo)
    except sqlite3.Error as e:
        print(e)
        return "A database error occurred."


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

#Delete item from daily food table
@app.route('/delete_daily/<id>/', methods=['GET'])
def delete_daily(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM FoodDaily WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash("Food item was deleted successfully.")
        return redirect(url_for('food'))
    except sqlite3.Error as e:
        print(e)
        return "A database error occurred."

#Exercise views for CRUD operations
@app.route("/exercise")
def exercise():
    try:
        conn = get_db_connection()
        exercises = conn.execute('SELECT * FROM ExerciseLogs1').fetchall()
        conn.close()
        return render_template('exercise.html', exercises=exercises)
    except sqlite3.Error as e:
        print(e)
        return "A database error occurred."

#Add Exercise to db
@app.route('/add_exercise', methods=('GET', 'POST'))
def add_exercise():
    if request.method == 'POST':
        try:
            weekid = request.form['weekid']
            dan = request.form['dan']
            exercise_ta = request.form['exercise']
            conn = get_db_connection()
            if dan=="dan1":
                conn.execute('INSERT INTO ExerciseLogs1(weekid, dan1) VALUES (?, ?)',
                            (weekid, exercise_ta))
            elif dan=="dan2":
                conn.execute('INSERT INTO ExerciseLogs1(weekid, dan2) VALUES (?, ?)',
                            (weekid, exercise_ta))
            elif dan=="dan3":
                conn.execute('INSERT INTO ExerciseLogs1(weekid, dan3) VALUES (?, ?)',
                            (weekid, exercise_ta))
            elif dan=="dan4":
                conn.execute('INSERT INTO ExerciseLogs1(weekid, dan4) VALUES (?, ?)',
                            (weekid, exercise_ta))
            else:
                conn.execute('INSERT INTO ExerciseLogs1(weekid, dan5) VALUES (?, ?)',
                            (weekid, exercise_ta))
            conn.commit()
            conn.close()
            flash("New exercise was added successfully.")
            return redirect(url_for('exercise'))
        except sqlite3.Error as e:
            print(e)
            return "A database error occurred."
    return render_template('add_exercise.html')

#Edit exercise 
@app.route('/edit_exercise/<id>/', methods=('GET', 'POST'))
def edit_exercise(id):
    exercise_sel = get_exercise(id)
    if request.method == 'POST':
        try:
            exercise_te = request.form['exercise']
            dan = request.form['dan']
            id_f = request.form['weekid']
            conn = get_db_connection()
            if dan=="dan1":
                conn.execute('UPDATE ExerciseLogs1 SET dan1 = ?'
                            ' WHERE weekid = ?',
                            (exercise_te,  id_f))
            elif dan=="dan2":
                conn.execute('UPDATE ExerciseLogs1 SET dan2 = ?'
                            ' WHERE weekid = ?',
                            (exercise_te,  id_f))
            elif dan=="dan3":
                conn.execute('UPDATE ExerciseLogs1 SET dan3 = ?'
                            ' WHERE weekid = ?',
                            (exercise_te,  id_f))
            elif dan=="dan4":
                conn.execute('UPDATE ExerciseLogs1 SET dan4 = ?'
                            ' WHERE weekid = ?',
                            (exercise_te,  id_f))
            else:
                conn.execute('UPDATE ExerciseLogs1 SET dan5 = ?'
                            ' WHERE weekid = ?',
                            (exercise_te,  id_f))
            conn.commit()
            conn.close()
            flash("Exercise was edited successfully.")
            return redirect(url_for('exercise'))
        except sqlite3.Error as e:
            print(e)
            return "A database error occurred."
    
    return render_template('edit_exercise.html', exercise_sel=exercise_sel)

#Delete exercise
@app.route('/delete_exercise/<id>/', methods=['GET'])
def delete_exercise(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM ExerciseLogs1 WHERE weekid = ?', (id,))
        conn.commit()
        conn.close()
        flash("Exercise was deleted successfully.")
        return redirect(url_for('exercise'))
    except sqlite3.Error as e:
        print(e)
        return "A database error occurred."

#List views and CRUD operations

@app.route('/add_to_shopping', methods=('GET', 'POST'))
def add_to_shopping():
    if request.method == 'POST':
        try:
            shopping = request.form['shopping']
            conn = get_db_connection()
            conn.execute('INSERT INTO Shopping (shopping) VALUES (?)',
                         (shopping,))
            conn.commit()
            conn.close()
            flash("New shopping list item was added successfully.")
            return redirect(url_for('home'))
        except sqlite3.Error as e:
            print(e)
            return "A database error occurred."
    return render_template('add_to_shopping.html')

#Adding item to todo list(Debug note:pass argument to conn.execute as tuple with single element :D)
@app.route('/add_to_todo', methods=('GET', 'POST'))
def add_to_todo():
    if request.method == 'POST':
        try:
            todo = request.form['todo']
            conn = get_db_connection()
            conn.execute('INSERT INTO Todo (todo) VALUES (?)',
                         (todo,))
            conn.commit()
            conn.close()
            flash("New Todo item was added successfully.")
            return redirect(url_for('home'))
        except sqlite3.Error as e:
            print(e)
            return "A database error occurred."
    return render_template('add_to_todo.html')

#Deleting from list
#Shopping
@app.route('/delete_shop_item/<id>/', methods=['GET'])
def delete_shop_item(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM Shopping WHERE shopping = ?', (id,))
        conn.commit()
        conn.close()
        flash("List item was deleted successfully.")
        return redirect(url_for('home'))
    except sqlite3.Error as e:
        print(e)
        return "A database error occurred."

#Todo
@app.route('/delete_todo_item/<id>/', methods=['GET'])
def delete_todo_item(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM Todo WHERE todo = ?', (id,))
        conn.commit()
        conn.close()
        flash("List item was deleted successfully.")
        return redirect(url_for('home'))
    except sqlite3.Error as e:
        print(e)
        return "A database error occurred."

if __name__ == "__main__":
    app.run(debug=True)

