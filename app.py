
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, url_for, session, request, redirect, render_template
import jinja2
import json
import time
import pandas as pd
from nametourl import query
from ytaudio import download
import secretkeys
class Song():
    def __init__(self,song) -> None:
        '''
        takes in the name of a song
        '''
        self.song_url = query(song)

    def downloadsong(self):
        download(song_url=self.song_url)

class Playlist():
    def __init__(self,songs) -> None:
        '''
        Takes in a list of name of songs
        '''

        self.song_list = []
        for song in songs:
            self.song_list.append(query(song))

    def downloadsong(self):
        for song_url in self.song_list:
            download(song_url=song_url)


#this can take in Song object AND Playlist object and download them
#showcasing polymorphism
def download_any(obj):
    obj.downloadsong()


# App config
app = Flask(__name__)

app.secret_key = 'Onkkgnbm1029'
app.config['SESSION_COOKIE_NAME'] = 'shashwat cookie'
result_play = dict()
@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect("/getPlaylists")
   

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


@app.route('/getPlaylists')
def get_playlist():
    global result_play
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    iter = 0
    print(sp.current_user())
    print("####################################################################")
    while True:
        offset = iter * 50
        iter += 1
        curGroup = sp.current_user_playlists(limit=50, offset=offset)["items"]
        
        results = []
        result_play = dict()
        for idx, item in enumerate(curGroup):
            uri = item['uri']
       
            print(f"Playlist name: {item['name']}")
            tracksitems = sp.playlist_tracks(uri, fields=None, limit=100, offset=0, market=None, additional_types=('track', ))['items']
           
            for tracks in tracksitems:
                if tracks["track"] :
                    song_name = [(tracks['track']['name']+ " - " +tracks['track']["artists"][0]["name"])]
                    if item['name'] not in result_play:
                        result_play[item['name']] =[]

                    result_play[item['name']].append(song_name)
                    
                    results += song_name
        if (len(curGroup) < 50):
            break

    return redirect(url_for('down'))

@app.route('/download')
def down():
    return render_template("result.html",result = result_play)

@app.route('/download',methods = ['POST'])
def down1():
    
    if request.method == 'POST':
        try:
            song = request.form['submit_button']
            song_obj = Song(song)
            download_any(song_obj)
        except:
            playlist = request.form['playlist_btn']
            playlist_obj = Playlist(result_play[playlist])
            download_any(playlist_obj)


    return render_template("result.html",result = result_play)


 
    
 

# Checks to see if token is valid and gets a new token if not
def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid
    # return "token"

def create_spotify_oauth():
    return SpotifyOAuth(
            spotify_client_id=secretkeys.client_id,
            spotify_client_secret=secretkeys.client_secret,
            redirect_uri=url_for('redirectPage', _external=True),
            scope="user-library-read,playlist-read-private,playlist-read-collaborative")

