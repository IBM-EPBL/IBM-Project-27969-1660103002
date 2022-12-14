from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='flask_db',
                            user='postgres',
                            password='a2z@3334')
    return conn


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logout")
def logout():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route('/check',methods=['GET','POST'])
def check():
	email=request.form['email']
	password=request.form['password']
	conn=get_db_connection()
	cur=conn.cursor()
	cur.execute('select * from users')
	users=cur.fetchall()
	flag=False
	for i in users:
		if(i[1]==email and i[2]==password):
			flag=True
	if(flag):
		return redirect("/home")
	else:
		return render_template("index.html",msg="Below Entered Email ID/Password Incorrect")

@app.route('/reg', methods=['GET', 'POST'])
def reg():
	print("Before")
	name = request.form['name']
	email = request.form['email']
	password = request.form['pass']
	print(name,email,password)
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute('select * from users')
	users=cur.fetchall()
	for i in users:
		if(email==i[1]):
			return render_template("register.html",msg="Email id Already Registerd.Please Login")
	cur.execute('insert into users (name,email,passwords) values(%s,%s,%s)',(name,email,password))
	conn.commit()
	cur.close()
	conn.close()
	return render_template("index.html",msg="Succesfully Registered Please Login To Continue")
    

if __name__ == "__main__":
	app.run(debug = True)
