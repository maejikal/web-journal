from flask import Flask, render_template, request, redirect, url_for
from func import get_esv_text, get_random, txttolist
import random
import requests
import datetime
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

d = datetime.date.today()
date = d.strftime("%a, %d %b")

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html', date=date)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username'].strip()
    email = request.form['email'].strip()
    password = request.form['password'].strip()


    db = sqlite3.connect('users.db')
    exist = db.execute("SELECT * from users where email=?", (email,))
    if exist == None:
        db.execute("INSERT INTO users VALUES (?, ?, ?)", (username, email, password))
        db.commit()
        db.close()
        return render_template("user_added.html", msg='registration successful!')
    else:
        return render_template("user_added.html", msg="the email is already associated with an account.")

@app.route('/login', methods=['POST'])
def login():
    return

@app.route('/copyright')
def copyright():
    return render_template("copyright.html")
    
@app.route('/cheer-up')
def sad():
    verses = txttolist("feelz/sad.txt")
    verse = get_esv_text(verses[random.randint(0, len(verses)-1)])
    ref = verse[0]
    content = "\n".join(verse[1])
    return render_template('show.html', verse=content, ref=ref, feel='sad')

@app.route("/be-at-peace")
def worried():
    verses = txttolist("feelz/worried.txt")
    verse = get_esv_text(verses[random.randint(0, len(verses)-1)])
    ref = verse[0]
    content = "\n".join(verse[1])
    return render_template('show.html', verse=content, ref=ref, feel='worried')

@app.route("/have-peace")
def fearful():
    verses = txttolist("feelz/fear.txt")
    verse = get_esv_text(verses[random.randint(0, len(verses)-1)])
    ref = verse[0]
    content = "\n".join(verse[1])
    return render_template('show.html', verse=content, ref=ref, feel='fearful')

@app.route("/take-it-easy")
def stressed():
    verses = txttolist("feelz/stressed.txt")
    verse = get_esv_text(verses[random.randint(0, len(verses)-1)])
    ref = verse[0]
    content = "\n".join(verse[1])
    return render_template('show.html', verse=content, ref=ref, feel='stressed')

@app.route("/calm-down")
def angry():
    verses = txttolist("feelz/angry.txt")
    verse = get_esv_text(verses[random.randint(0, len(verses)-1)])
    ref = verse[0]
    content = "\n".join(verse[1])
    return render_template('show.html', verse=content, ref=ref, feel='angry')

@app.route('/search')
def search():
    feel = request.args['feel']
    verse = get_random(feel)
    if verse == '404':
        return render_template('add_verse.html', search_failed=True)
    ref = verse[0]
    content = verse[1]
    return render_template('show.html', verse=content, ref=ref, feel=feel)

#regenerate verses
@app.route('/redirect/<feel>')
def red(feel):
    main = ['sad', 'worried', 'fearful', 'stressed', 'angry']
    if feel in main:
        return redirect(url_for(feel))
    else:
        return redirect(url_for('search', feel=feel))

@app.route("/save")
def save():
    return render_template("save.html")


app.run(host="0.0.0.0", port=5000)

# curl -L -H 'Authorization: Token 1a07eb6942168a4236f35a488a4da3ca6dfcc72a' 'https://api.esv.org/v3/passage/search/?q=love&page=23'
