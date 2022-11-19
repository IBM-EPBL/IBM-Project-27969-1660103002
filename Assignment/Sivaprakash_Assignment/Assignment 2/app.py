from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'a2z@3334'
app.config['MYSQL_DB'] = 'sys'

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/signin',methods=["POST","GET"])
def signin():
   return render_template("signin.html")

@app.route('/addsignin',methods=['POST','GET'])
def addsignin():
    msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('home.html', msg = msg)
		else:
			return render_template("signin.html",msg="Invalid E-Mail or Password")

@app.route('/signup',methods=['POST','GET'])
def signup(): 
    return render_template("signup.html")

@app.route('/addsignup',methods=["POST","GET"])
def addsignup():
    msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (username, password, email,))
			mysql.connection.commit()
			return render_template("home.html",msg="Successfully Registered")
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('signup.html', msg = msg)


if __name__ == '__main__':
    app.run(debug=True)
