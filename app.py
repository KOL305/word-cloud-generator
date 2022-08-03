from functools import wraps
from bson.objectid import ObjectId
import datetime
from flask import Flask, render_template, jsonify, request, redirect, session, abort, flash
from flask_minify import minify
from flask_pymongo import PyMongo
from flask_session import Session
from passlib.hash import pbkdf2_sha256
import pymongo
from config import Config, db

app = Flask("ATT Hackathon Project")
app.config.from_object(Config)
client = PyMongo(app)
db = client.db
Session(app)

def login_required(something):
    @wraps(something)
    def wrap_login(*args, **kwargs):
        if 'logged_in' in session and session["logged_in"]:
            return something(session['logged_in_id'], *args, **kwargs)
        else:
            flash("Please Sign In First", category="danger")
            return redirect('/')
    return wrap_login

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'GET':     
        if 'logged_in' in session and session["logged_in"]:
            user = db.users.find_one({'_id': ObjectId(session["logged_in_id"])})
            bal = user['balance']
            return render_template('home.html', bal=bal)
        return render_template('home.html')
    elif request.method == 'POST':
        return render_template('home.html')

if __name__ == "__main__":
    app.config['SECRET_KEY'] = '123qwi34iWge9era89F1393h3gwJ0q3'
    app.run(debug=True)