# ---- YOUR APP STARTS HERE ----
# -- Import section --

import os
from flask import Flask
from flask import render_template, request, redirect, session, url_for
from flask_pymongo import PyMongo

from bson.objectid import ObjectId

# -- Initialization section --
app = Flask(__name__)

# name of database
app.config['MONGO_DBNAME'] = os.getenv("NAME_DB") 

# URI of database for read/write provileges
app.config['MONGO_URI'] = os.getenv("MONGO_URI")


# This is for the session
#  If using Python 3, use a string
app.secret_key = os.getenv("SESSION")

mongo = PyMongo(app)

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if request.form['password'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('display_main'))
        return render_template('login.html', prompt="Id or password do not match")
    return render_template('signup.html', prompt="There is no account with that name, create new account") 

# SIGN UP
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            users.insert({'name' : request.form['username'], 'password' : request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('display_main'))
        return render_template('signup.html', prompt='That username already exists! Try again.')
    return render_template('signup.html', prompt='You need to sign up for an account')

# INDEX
@app.route('/')
@app.route('/index')
def index():
    collection = mongo.db.music
    songsDB = collection.find({})
    print(songsDB)
    print(collection.count_documents({}))    #how to get count of documents (records)
    return render_template("index.html", records=songsDB)

# GO TO LOGIN
@app.route('/gologin')
def go_to_login():
    return render_template('login.html', prompt="Login here")

# DISPLAY MAINPAGE
@app.route('/mainpage')
def display_main():
    collection = mongo.db.music
    songsDB = collection.find({})
    return render_template("mainpage.html", records=songsDB)


# ADD SONGS
@app.route('/add')
def add():
    # define a variable for the collection you want to connect to
    collection = mongo.db.music
    mylist = [
        { "title": "Amy", "artist": "Coldplay", "comment": ["a", "b", "c"]},
        { "title": "Hannah", "artist": "Mumford and Sons", "comment": ["a", "c"]},
        { "title": "Michael", "artist": "Mumford and Sons", "comment":["a"]},
        { "title": "Sandy", "artist": "Coldplay", "comment": ["b", "c"]},
        { "title": "Betty", "artist": "Blue October", "comment": [ "c"]},
        { "title": "Richard", "artist": "Blue October", "comment": ["a", "b", "c"]},
        { "title": "Susan", "artist": "Coldplay", "comment": [ "b", "c"]},
        { "title": "Vicky", "artist": "Blue October", "comment": []},
        { "title": "Ben", "artist": "Elton John", "comment": []},
        { "title": "William", "artist": "Elton John", "comment": []},
        { "title": "Chuck", "artist": "Mumford and Sons", "comment":[]},
        { "title": "Viola", "artist": "Mumford and Sons", "comment": ["a", "b", "c"]}
        ]
        
    collection.insert_many(mylist)
    # songsDB = collection.find({})
    # print(collection.count_documents({}))    #how to get count of documents (records)
    return redirect(url_for('display_main'))

#remove all
@app.route('/remove')
def emptyDatabase():
    # define a variable for the collection you want to connect to
    songs = mongo.db.music
    songs.remove({})
    # print(songs.count_documents({}))    #how to get count of documents (records)
    return redirect(url_for('display_main'))

# ADVANCED: A FORM TO COLLECT USER-SUBMITTED SONGS
#14. Create a new HTML template that is a form for a user to submit their favorite songs to the list. 
#Make sure there is a way for the user to include the song title, artist, and a description of why they like that song.
@app.route('/song/new', methods=['GET', 'POST'])
def new_event():
    if request.method == "GET":
        #return render_template('new_event.html')
        return "Need to add a page here"
    else:
        song_title = request.form['song_name']
        song_artist = request.form['song_artist']
        comment = request.form['song_comment']
        songs = mongo.db.music
        songs.insert({'title': song_title, 'artist': song_artist, 'comment': comment, 'lister': session['username']})
        return redirect(url_for('display_main'))

#11. Update the route method to show the songs in alphabetical order by the name of the song.
#sort by song title
@app.route('/sort/title')
def sort_title():
    collection = mongo.db.music
    #db.mycol.find({},{"title":1,_id:0}).sort({"title":-1})
    songsDB=collection.find({}).sort('title', 1 )  #1 means ascending, -1 is descending
    return render_template('mainpage.html', records=songsDB)
    #return redirect('/')

#12. Update the route method to show the songs in alphabetical order by the name of the artist.

#13. Update the route method to show just the first three songs when ordered alphabetically by artist.

# DOUBLE-ADVANCED: SHOW ARTIST PAGE
#16. Create a new HTML template and route that will show all songs matching an artist's name: e.g. `/artist/<name>`.
@app.route('/find/artist', methods=['GET', 'POST'])
def find_artist():
    if request.method == "GET":
        #return render_template('new_event.html')
        return "Find Artist: Need to add something here"
    else:
        song_artist = request.form['artist']
        songs = mongo.db.music
        artist = request.form['artist']
        songsList = songs.find({'artist': artist})
        return render_template('artist.html', theArtist = song_artist, records = songsList)

#17. Update the HTML template showing all songs to make each artist's name a hyperlink which 
#shows all songs by that artist.

#18. Create a new HTML template and route that will show a song based on the unique identifier, `_id`, that is assigned by MongoDB: e.g. `/song/<_id>`. 
# Each song-specific page should also show the user-submitted description of the song.

# TRIPLE-ADVANCED: SHOW SONG PAGE
#19. Update the HTML template showing all songs to make each song a hyperlink that shows the song-specific page.
@app.route('/find/<songtitle>')
def find_song(songtitle):
    #print(songtitle)
    collection = mongo.db.music
    song = collection.find_one({'_id': ObjectId(songtitle)})
    #print(song)
    song_title = song['title']
    return render_template('song.html', theTitle= song_title, song =  song)

#Update fields
@app.route('/update/<song_id>', methods=['GET', 'POST'])
def changeSong(song_id):
    if request.method == "GET":
        #return render_template('new_event.html')
        return "Returning to update: Need to add a page here"
    else:
        print(song_id)
        myquery = { "_id": ObjectId(song_id) }
        song_title = request.form['song_title']
        song_artist = request.form['song_artist']
        comment = request.form['song_comment']
        newvalues = { "$set": { "title": song_title, "artist" : song_artist, "comment":comment } }

        songs = mongo.db.music
        songs.update_one(myquery, newvalues)
        return redirect(url_for('display_main'))

#REMOVE a 
@app.route('/remove/<song_id>')
def remove_song(song_id):
    collection = mongo.db.music
    collection.delete_one({'_id': ObjectId(song_id)})
    return redirect(url_for('display_main'))

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# GATED PAGE
@app.route('/profile/<name>')
def listings(name):
    print (name)
    collection = mongo.db.music
    songs = collection.find({'lister' : name})
    print(songs)
    return render_template('listings.html', songs = songs, lister = name)

