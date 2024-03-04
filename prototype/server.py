from flask import Flask, render_template, request, redirect, url_for, session, flash
from func import *
import random
import datetime
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

d = datetime.date.today()
date = d.strftime("%a, %d %b") #top of html page
format_date = d.strftime("%Y-%m-%d") #storage purposes

app = Flask(__name__)
app.config["SECRET_KEY"] = 'sosecretive'

@app.route('/')
def root():

    return render_template('index.html', date=date)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username'].strip()
    email = request.form['email'].strip()
    password = request.form['password'].strip()
    password_hash = generate_password_hash(password, "pbkdf2:sha256")

    db = sqlite3.connect('database.db')
    exist = db.execute("SELECT * from users where email=?", (email,))
    exist = exist.fetchall()
    if len(exist) == 0:
        db.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password_hash))
        db.commit()
        db.close()
        return render_template("user_added.html", msg='registration successful!')
    else:
        db.close()
        return render_template("user_added.html", msg="this email is already associated with an account.")

@app.route('/login')
def login():
    if 'msg' in request.args:
        msg = request.args['msg']
    else:
        msg = ''
    return render_template("login.html", msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('logged_in', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('root'))

@app.route('/dashboard')
def dashboard():
    if "logged_in" in session:
        return render_template("dashboard.html")
    else:
        return render_template('login.html', msg='please login to access the dashboard!')

@app.route('/verify', methods=['POST'])
def verify():
    db = sqlite3.connect("database.db")
    email = request.form['email'].strip().lower()
    formpassword = request.form['password']
    user = db.execute("SELECT * from users where email=?", (email,))
    user = user.fetchone()
    if user == None:
        return render_template("login.html", msg='user does not exist. please try again.')
    elif check_password_hash(user[3], formpassword):
        session['logged_in'] = True
        session['id'] = user[0]
        session['username'] = user[1]
        session['email'] = user[2]
        return redirect(url_for("root"))
    else:

        return render_template("login.html", msg='wrong password. please try again.')

@app.route('/registerform')
def registerform():
    return render_template("registerform.html")

@app.route('/copyright')
def copyright():
    return render_template("copyright.html")
    
@app.route('/sad')
def sad():
    verses = txttolist("feelz/sad.txt")
    verse = get_esv_text(verses[random.randint(0, len(verses)-1)])
    ref = verse[0]
    content = "\n".join(verse[1])
    return render_template('show.html', verse=content, ref=ref, feel='sad')

@app.route("/worried")
def worried():
    verses = txttolist("feelz/worried.txt")
    verse = get_esv_text(verses[random.randint(0, len(verses)-1)])
    ref = verse[0]
    content = "\n".join(verse[1])
    return render_template('show.html', verse=content, ref=ref, feel='worried')

@app.route("/fearful")
def fearful():
    verses = txttolist("feelz/fear.txt")
    verse = get_esv_text(verses[random.randint(0, len(verses)-1)])
    ref = verse[0]
    content = "\n".join(verse[1])
    return render_template('show.html', verse=content, ref=ref, feel='fearful')

@app.route("/stressed")
def stressed():
    verses = txttolist("feelz/stressed.txt")
    verse = get_esv_text(verses[random.randint(0, len(verses)-1)])
    ref = verse[0]
    content = "\n".join(verse[1])
    return render_template('show.html', verse=content, ref=ref, feel='stressed')

@app.route("/angry")
def angry():
    verses = txttolist("feelz/angry.txt")
    verse = get_esv_text(verses[random.randint(0, len(verses)-1)])
    ref = verse[0]
    content = "\n".join(verse[1])
    return render_template('show.html', verse=content, ref=ref, feel='angry')

@app.route("/bitter")
def bitter():
    verses = txttolist("feelz/bitter.txt")
    verse = get_esv_text(verses[random.randint(0, len(verses)-1)])
    ref = verse[0]
    content = "\n".join(verse[1])
    return render_template('show.html', verse=content, ref=ref, feel='bitter')

@app.route("/weak")
def weak():
    verses = txttolist("feelz/weak.txt")
    verse = get_esv_text(verses[random.randint(0, len(verses)-1)])
    ref = verse[0]
    content = "\n".join(verse[1])
    return render_template('show.html', verse=content, ref=ref, feel='weak')

@app.route("/lost")
def lost():
    verses = txttolist("feelz/lost.txt")
    verse = get_esv_text(verses[random.randint(0, len(verses)-1)])
    ref = verse[0]
    content = "\n".join(verse[1])
    return render_template('show.html', verse=content, ref=ref, feel='lost')

@app.route("/overwhelmed")
def overwhelmed():
    verses = txttolist("feelz/overwhelmed.txt")
    verse = get_esv_text(verses[random.randint(0, len(verses)-1)])
    ref = verse[0]
    content = "\n".join(verse[1])
    return render_template('show.html', verse=content, ref=ref, feel='overwhelmed')

@app.route("/envious")
def envious():
    verses = txttolist("feelz/envious.txt")
    verse = get_esv_text(verses[random.randint(0, len(verses)-1)])
    ref = verse[0]
    content = "\n".join(verse[1])
    return render_template('show.html', verse=content, ref=ref, feel='envious')

@app.route("/grieved")
def grieved():
    verses = txttolist("feelz/grief.txt")
    verse = get_esv_text(verses[random.randint(0, len(verses)-1)])
    ref = verse[0]
    content = "\n".join(verse[1])
    return render_template('show.html', verse=content, ref=ref, feel='grieved')

@app.route('/search')
def search():
    feel = request.args['feel']
    verse = get_random(feel)
    if verse == '404':
        return render_template('error.html', msg='no verse was found. try again.')
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

@app.route("/add_own_verse", methods=['POST'])
def add_verse():
    if 'logged_in' in session:
        ref = request.form['ref'].strip()
        feel = request.form['feel'].strip()
        note = request.form['note'].strip()
        verse = get_esv_text(ref)
        if verse == "404":
            msg = 'unable to find verse, make sure the entered verse reference is of the format \n "book chapter:verse"'
            return render_template('error.html', msg=msg)
        db = sqlite3.connect('database.db')
        db.execute("INSERT INTO saved (user_id, date, verse_ref, verse_cont, feels, note) VALUES (?,?,?,?,?,?)", (session['id'], format_date, ref, "".join(verse[1]), feel, note))
        db.commit()
        db.close()
        return redirect(url_for('save_successful'))
    else:
        return redirect(url_for("login", msg='please login to save this verse!'))

@app.route("/save/<feel>/<ref>", methods=['POST'])
def save(feel, ref):
    if 'logged_in' in session:
        verse = get_esv_text(ref)
        verse = '\n'.join(verse[1])
        note = request.form['note'].strip()
        feel = request.form['feel'].strip()
        db = sqlite3.connect('database.db')
        db.execute("INSERT INTO saved (user_id, date, verse_ref, verse_cont, feels, note) VALUES (?,?,?,?,?,?)", (session['id'], format_date, ref, verse, feel, note))
        db.commit()
        db.close()
        return redirect(url_for('save_successful'))
    else:
        return redirect(url_for("login", msg='please login to save this verse!'))

@app.route('/status')
def save_successful():
    return render_template('saved_info.html')

@app.route('/edit/<post_id>')
def edit(post_id):
    db = sqlite3.connect('database.db')
    post = db.execute('SELECT date, feels, note from saved where saved_id=?', (post_id,))
    post = post.fetchone() 
    print(post)
    db.close()
    return render_template('edit.html', post_id=post_id, date=post[0], feel=post[1], note=post[2])

# @app.route('/edit/form')
# def edit_form():
#     post_id = request.args['post_id']
#     date = request.args['date']
#     feel = request.args['feel']
#     note = request.args['note']
#     return render_template('edit.html', post_id=post_id, date=date, feel=feel, note=note)

@app.route('/edit/<post_id>/save-edit', methods=['POST'])
def save_edit(post_id):
    feel = request.form['feel'].strip()
    note = request.form['note'].strip()
    print(feel, note)
    db = sqlite3.connect('database.db')
    db.execute('UPDATE saved set feels = ?, note = ? where saved_id=?', (feel, note, post_id))
    db.commit()
    db.close()
    return redirect(url_for("journal", msg=" edit saved successfully!"))

@app.route('/delete/<post_id>')
def delete_post(post_id):
    db = sqlite3.connect('database.db')
    db.execute("DELETE from saved where saved_id =?", (post_id,))
    db.commit()
    db.close()
    return redirect(url_for('journal', msg='deleted successfully!'))

@app.route('/delete_user')
def delete_user():
    db = sqlite3.connect('database.db')
    db.execute("DELETE from users where id =?", (session['id'],))
    db.execute("DELETE from saved where user_id =?", (session['id'],)) #delete all posts saved by user
    db.commit()
    db.close()
    return redirect(url_for('logout'))

# change appearance of app
@app.route('/settings')
def settings():
    if session['mode'] == 'dark':
        session['mode'] = 'light'
    else:
        session['mode'] = 'dark'
    return redirect(url_for('root'))

@app.route('/journal')
def journal():
    if 'msg' in request.args:
        msg = request.args['msg']
    else:
        msg = ''
    db = sqlite3.connect('database.db')
    posts = db.execute("SELECT * from saved where user_id = ? order by date desc", (session['id'],))
    posts = posts.fetchall()
    if len(posts) == 0:
        msg = "there is nothing in your journal. generate a random verse to add your first entry."
    db.close()
    return render_template("journal.html", posts=posts, msg=msg)

@app.route('/full-view/<post_id>')
def viewfull(post_id):
    db = sqlite3.connect('database.db')
    post = db.execute("SELECT * from saved where saved_id = ? order by date desc", (post_id,))
    post = post.fetchone()
    db.close()
    return render_template('fullview.html', post=post)

@app.route('/saved')
def saved_verses():
    if 'logged_in' in session:
        db = sqlite3.connect('database.db')
        posts = db.execute("SELECT verse_ref, verse_cont from saved where user_id = ? order by date desc", (session['id'],))
        posts = posts.fetchall()
        if len(posts) == 0:
            msg = 'there is nothing to show. add your first verse or generate a random verse.'
        else:
            msg = ''
        db.close()
        return render_template('saved_verses.html', posts=posts, msg=msg)
    else:
        return redirect(url_for("login", msg='please login to save view your saved verses!'))


app.run(host="0.0.0.0", port=5000, debug=True)

# curl -L -H 'Authorization: Token your_API' 'https://api.esv.org/v3/passage/search/?q=love&page=23'
