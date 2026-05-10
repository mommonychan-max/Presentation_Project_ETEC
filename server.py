from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "cinema_secret_123"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ================= DATABASE =================
def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='cinema_db'
    )


# ================= LOGIN REQUIRED CHECK =================
def login_required():
    return session.get('user') is not None


# ================= HOME =================
@app.route('/')
def index():

    # 🔐 FORCE LOGIN FIRST
    if not session.get('user'):
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM movies ORDER BY id DESC')
    movies = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('index.html', movies=movies)


# ================= MOVIE DETAIL =================
@app.route('/movie/<int:id>')
def movie_detail(id):

    if not session.get('user'):
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM movies WHERE id=%s', (id,))
    movie = cursor.fetchone()
    cursor.close()
    db.close()

    return render_template('movie_detail.html', movie=movie)


# ================= ADD MOVIE (ADMIN ONLY) =================
@app.route('/add', methods=['GET', 'POST'])
def add_movie():

    if session.get('role') != 'admin':
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        movie_year = request.form['movie_year']
        description = request.form['description']

        filename = ''
        file = request.files.get('image')

        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO movies (title, genre, movie_year, description, image) VALUES (%s,%s,%s,%s,%s)',
            (title, genre, movie_year, description, filename)
        )
        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for('index'))

    return render_template('add_movie.html')


# ================= DELETE MOVIE (ADMIN ONLY) =================
@app.route('/delete/<int:id>')
def delete_movie(id):

    if session.get('role') != 'admin':
        return redirect(url_for('index'))

    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM movies WHERE id=%s", (id,))
    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for('index'))


# ================= EDIT MOVIE (ADMIN ONLY) =================
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_movie(id):

    if session.get('role') != 'admin':
        return redirect(url_for('index'))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute('SELECT * FROM movies WHERE id=%s', (id,))
    movie = cursor.fetchone()

    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        movie_year = request.form['movie_year']
        description = request.form['description']

        filename = movie['image'] if movie else ''

        file = request.files.get('image')
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cursor2 = db.cursor()
        cursor2.execute(
            'UPDATE movies SET title=%s, genre=%s, movie_year=%s, description=%s, image=%s WHERE id=%s',
            (title, genre, movie_year, description, filename, id)
        )

        db.commit()
        cursor2.close()
        cursor.close()
        db.close()

        return redirect(url_for('index'))

    cursor.close()
    db.close()

    return render_template('edit_movie.html', movie=movie)


# ================= REGISTER =================
@app.route('/register', methods=['GET', 'POST'])
def register():

    if session.get('user'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s,%s,'user')",
            (username, password)
        )

        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for('login'))

    return render_template('register.html')


# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():

    error = None

    if session.get('user'):
        return redirect(url_for('index'))

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:
            session.clear()
            session['user'] = user['username']
            session['role'] = user['role']

            return redirect(url_for('index'))
        else:
            error = "❌ Wrong username or password"

    return render_template('login.html', error=error)

# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ================= CART =================
@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):

    if not session.get('user'):
        return redirect(url_for('login'))

    if 'cart' not in session:
        session['cart'] = []

    cart = session['cart']

    if id not in cart:
        cart.append(id)
        session['cart'] = cart

    return redirect(url_for('index'))


@app.route('/cart')
def cart():

    if not session.get('user'):
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cart_items = session.get('cart', [])

    if cart_items:
        format_strings = ','.join(['%s'] * len(cart_items))
        cursor.execute(f"SELECT * FROM movies WHERE id IN ({format_strings})", tuple(cart_items))
        movies = cursor.fetchall()
    else:
        movies = []

    cursor.close()
    db.close()

    return render_template('cart.html', movies=movies)

@app.route('/checkout')
def checkout():

    if not session.get('user'):
        return redirect(url_for('login'))

    cart_items = session.get('cart', [])

    if not cart_items:
        return redirect(url_for('cart'))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    format_strings = ','.join(['%s'] * len(cart_items))
    cursor.execute(f"SELECT * FROM movies WHERE id IN ({format_strings})", tuple(cart_items))
    movies = cursor.fetchall()

    cursor.close()
    db.close()

    total = len(movies) * 5  # 💰 simple ticket price example

    receipt = {
        "user": session['user'],
        "movies": movies,
        "total": total
    }

    # clear cart after buy
    session['cart'] = []

    return render_template('receipt.html', receipt=receipt)




# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)