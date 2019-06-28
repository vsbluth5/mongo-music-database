import os
from app import app
from flask import render_template, request, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# name of database
app.config['MONGO_DBNAME'] = 'firstMusic' 

# URI of database for read/write provileges
app.config['MONGO_URI'] = 'mongodb+srv://person1:pVoEoiSZnPw0omb8@cluster0-vmzkd.mongodb.net/firstMusic?retryWrites=true&w=majority' 

# URI of database for read-only provileges
#app.config['MONGO_URI'] = 'mongodb+srv://person_read:vRR3w93lXlbJqMh2@cluster0-vmzkd.mongodb.net/firstMusic?retryWrites=true&w=majority' 

mongo = PyMongo(app)


# INDEX
@app.route('/')
@app.route('/index')
def index():
    collection = mongo.db.music
    songsDB = collection.find({})
    print(collection.count_documents({}))    #how to get count of documents (records)
    return render_template("index.html", records=songsDB)

# ADD SONGS
@app.route('/add')
def add():
    # define a variable for the collection you want to connect to
    collection = mongo.db.music
    #collection.insert({"song":"Row, Row, Row Your Boat"})mydb = myclient["mydatabase"]
    mylist = [
        { "title": "Amy", "artist": "Coldplay", "comment": "provilegesretty"},
        { "title": "Hannah", "artist": "Mumford and Sons", "comment": "soothing"},
        { "title": "Michael", "artist": "Mumford and Sons", "comment": "happy"},
        { "title": "Sandy", "artist": "Coldplay", "comment": "mellow"},
        { "title": "Betty", "artist": "Blue October", "comment": "pretty"},
        { "title": "Richard", "artist": "Blue October", "comment": "happy"},
        { "title": "Susan", "artist": "Coldplay", "comment": "happy"},
        { "title": "Vicky", "artist": "Blue October", "comment": "soothing"},
        { "title": "Ben", "artist": "Elton John", "comment": "fave"},
        { "title": "William", "artist": "Elton John", "comment": "happy"},
        { "title": "Chuck", "artist": "Mumford and Sons", "comment": "pretty"},
        { "title": "Viola", "artist": "Mumford and Sons", "comment": "mellow"}
        ]
        
    #x = songs.insert_many(mylist)
    collection.insert_many(mylist)
    #songsDB = collection.find({})
    print(collection.count_documents({}))    #how to get count of documents (records)
    return redirect('/')

#remove all
@app.route('/remove')
def emptyDatabase():
    # define a variable for the collection you want to connect to
    songs = mongo.db.music
    songs.remove({})
    #songsDB = songs.find({})
    print(songs.count_documents({}))    #how to get count of documents (records)
    return redirect('/')

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
        songs.insert({'title': song_title, 'artist': song_artist, 'comment': comment})
        return redirect('/')

#11. Update the route method to show the songs in alphabetical order by the name of the song.
#sort by song title
@app.route('/sort/title')
def sort_title():
    collection = mongo.db.music
    #db.mycol.find({},{"title":1,_id:0}).sort({"title":-1})
    songsDB=collection.find({}).sort('title', 1 )  #1 means ascending, -1 is descending
    return render_template('index.html', records=songsDB)
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
        return redirect('/')

#REMOVE a 
@app.route('/remove/<song_id>')
def remove_song(song_id):
    collection = mongo.db.music
    collection.delete_one({'_id': ObjectId(song_id)})
    return redirect('/')





