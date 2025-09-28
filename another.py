from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'skibidi'  # More secure secret key

# MySQL DB connection
db = mysql.connector.connect(
    host="localhost",
    user="flaskuser",
    passwd="flaskpass123",
    database="users_db"
)

# Use dictionary cursor for easier access
cursor = db.cursor(dictionary=True)

# Routes

@app.route('/')
def home():
    return render_template('mainpage.html')

@app.route('/Products')
def products():
    if not session.get('loggedin'):
        return redirect(url_for('signup'))
    return render_template('products.html')

@app.route('/Pricing')
def pricing():
    if not session.get('loggedin'):
        return redirect(url_for('signup'))
    return render_template('pricing.html')

@app.route('/Websites')
def websites():
    if not session.get('loggedin'):
        return redirect(url_for('signup'))
    return render_template('websites.html')

@app.route('/Aboutus')
def aboutus():
    if not session.get('loggedin'):
        return redirect(url_for('signup'))
    return render_template('aboutus.html')

@app.route('/FAQ')
def faq():
    if not session.get('loggedin'):
        return redirect(url_for('signup'))
    return render_template('faq.html')

@app.route('/Scripts')
def scripts():
    if not session.get('loggedin'):
        return redirect(url_for('signup'))
    return render_template('scripts.html')

@app.route('/signup', methods=['GET', 'POST'])#methods to get the input
def signup():
    if request.method == 'POST':#if the methd id post 
        username = request.form.get('username')#gets username
        email = request.form.get('email')#gets email
        password = request.form.get('password')#gets password

        if not username or not email or not password:#if they didnt fill it in
            flash("Please fill out all fields.")#flashes message
        else:#else
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))#select everything from users where email is the input
            account = cursor.fetchone()#gets it only one at a time
            if account:#if the account is true or it is ther
                flash("An account with that email already exists.")#flash another message
            else:#else
                hashed = generate_password_hash(password)#turns the password into a hash 
                cursor.execute(
                    "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    (username, email, hashed)
                )
                db.commit()#commits the sql
                flash("You have successfully registered! Please login.")#flashes another message
                return redirect(url_for('login'))#redirects the url

    return render_template('signup.html')#renders html

@app.route('/login', methods=['GET', 'POST'])#another route
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("Please fill out both fields.")
        else:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user and check_password_hash(user['password'], password):
                session.clear()
                session['loggedin'] = True
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect email or password.")

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    session['loggedin'] = False
    flash("You have been logged out.")

    return redirect(url_for('home'))
print(app.secret_key)
# Run the app
if __name__ == '__main__':
    app.run(debug=True)#im sorry
    


