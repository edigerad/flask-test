from flask import Flask, render_template, g, redirect
import sqlite3
from flask import request

app = Flask(__name__)


def connect_db():
    sql = sqlite3.connect('./database.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite3_db = connect_db()
    return g.sqlite3_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite3_db.close()


@app.route('/')
def hello_world():
    db = get_db()
    cursor = db.execute('select id, name, age from users')
    users = cursor.fetchall()
    print(users)

    return render_template('users.html', **{'users': users})


@app.route('/create', methods=['GET', 'POST'])
def form_example():
    # handle the POST request
    if request.method == 'POST':
        name, age = request.form.get('name'), request.form.get('age')
        db = get_db()
        db.execute(f'insert into users (name, age) values ("{name}",{age})')
        db.commit()
        return redirect('/')
    return '''
           <form method="POST">
               <div><label>Name: <input type="text" name="name"></label></div>
               <div><label>Age: <input type="text" name="age"></label></div>
               <input type="submit" value="Submit">
           </form>'''


@app.route('/<int:id>/edit', methods=["GET", "POST"])
def edit(id):
    db = get_db()
    if request.method == 'POST':
        name, age = request.form.get('name'), request.form.get('age')
        db.execute(f'update users set name="{name}", age="{age}" where id={id}')
        db.commit()
        return redirect('/')
    cursor = db.execute(f'select id, name, age from users where id={id}')
    user = cursor.fetchall()[0]
    return f'''
           <form method="POST">
               <div><label>Name: <input type="text" name="name" value={user['name']}></label></div>
               <div><label>Age: <input type="text" name="age" value={user['age']}></label></div>
               <input type="submit" value="Submit">
           </form>'''


@app.route('/<int:id>/delete', methods=["GET"])
def delete(id):
    db = get_db()
    db.execute(f'delete from users where id={id}')
    db.commit()
    return redirect('/')


@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
