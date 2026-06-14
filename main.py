from flask import Flask, render_template,request,redirect, url_for,session,flash
from tkinter import messagebox
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL

app=Flask(__name__)

app.secret_key="GamingTournament##$@@9765645"
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:Sarthak9321@localhost/gaminghub'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)



class matches(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(50), nullable=False)
    Tournament_name = db.Column(db.String(100))
    status = db.Column(db.String(20), nullable=False, default='Upcoming')
    prize_pull = db.Column(db.Integer, nullable=False, default=0)

class user(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    Join_date = db.Column(db.DateTime, nullable=False,default=db.func.current_timestamp())

@app.route('/')
def home():
    match=matches.query.all()
    return render_template('home.html', matches=match)

@app.route('/tournament')
def tournament():
    match=matches.query.all()
    return render_template('tournament.html',matches=match)

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/teams')
def teams():
    return render_template('teams.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        User=user.query.filter_by(email=email , password=password).first()
        if User:
            session["loggedin"]=True
            session["firstname"]=User.firstname
            session["lastname"]=User.lastname
            session["email"]=User.email
            return redirect(url_for('home'))
        else:
            flash("Account Don`t Exist Create Account To Continue")
            return redirect(url_for('join'))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session["loggedin"]=None
    session["firstname"]=None
    session["lastname"]=None
    return redirect(url_for("home"))
@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method =='POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        
        User=user.query.filter_by(email=email).first()
        if User:
            flash("The Email Address Allredy Registerd With Another Account")
            return redirect(url_for('join'))
        else:
            new_user = user(firstname=firstname, lastname=lastname, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))


    return render_template('join.html')

if __name__=='__main__':
    app.run(debug=True)
