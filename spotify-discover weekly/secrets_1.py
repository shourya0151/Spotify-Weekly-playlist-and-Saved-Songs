
import requests
import urllib.parse

from datetime import datetime, timedelta
from flask import Flask,redirect,request,jsonify,session


app = Flask(__name__)
app.secret_key = 'gdfdfhfhhfg8h8f7hfhfh7ffg7hhgh7h-hfh4'

CLIENT_ID = 'f2bbb53b070e43b182e6346488e3a27e'
CLIENT_SECRET = 'cd96d67caa2c4aeca9ca4300317ef4e6'
REDIRECT_URI =  'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

@app.route('/')
def index():
    return "Welcome to my Spotify AA <a href='/login'>Loogin with spotify</a>"

## now create login end point

@app.route('/login')
def login():
    scope = 'playlist-modify-public playlist-modify-private playlist-read-collaborative playlist-read-private user-library-read'

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True ##by defauly its is set false
    }

    ##make get request = their api

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    ##url lib to get params

    return redirect(auth_url) ## then redirect to auth url

@app.route('/callback')
def callback():
    if 'error' in request.args :##in query params
        return jsonify({"error": request.args['error']})
    
    ##if user login is successful that is no error
    
    
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret':CLIENT_SECRET
        } 

        response = requests.post(TOKEN_URL,data=req_body)
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

        print("The access token is -> ",session['access_token'])
        print("\n")
        print("The refresh token is ->",session['refresh_token'])

        return session
    
@app.route('/playlists')
def get_playlists():
    ##check if access token exists or not
    if 'access_token' not in session:
        return redirect('/login')
    ##check if access token has expired or not

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')
    
    ##now go and make the api request for the playlisty

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    response = requests.get(API_BASE_URL + 'me/playlists',headers=headers)
    playlists = response.json()

    return jsonify(playlists)

@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')
    

    ##check if token is expired or not

    if datetime.now().timestamp() > session['expires_at']:
        
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL,data=req_body)
        new_token_info = response.json()

        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']



        return redirect('/playlists')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
    