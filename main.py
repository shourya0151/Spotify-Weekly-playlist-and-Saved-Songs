##First we need to find songs from discover weekly playlists
import json
import requests
from secret import spotify_user_id,discover_weekly_id
from refresh import Refresh
from datetime import date


API_BASE_URL = 'https://api.spotify.com/v1/'



class SaveSongs:
    def __init__(self):
        self.spotify_user_id = spotify_user_id
        self.spotify_token = ''
        self.discover_weekly_id = discover_weekly_id
        self.tracks = []

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.spotify_token}"
        }
    
    def find_songs(self):

        print("Finding songs in discover weekly....")

        ##loop through playlist tracks and add them to the list

        query = API_BASE_URL + "playlists/" + discover_weekly_id + "/tracks"
        
        

        response = requests.get(query,headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        })

        response_json = response.json()
        print(response)

        for i in response_json["items"]:
            songTrack = ""
            songTrack += (i["track"]["uri"])
            self.tracks.append(songTrack)

        print("Songs Found!!\n")

        self.add_to_playlist()
    
    #now that we have got all teh playlists lerts now create a new playlist with all these items

    def create_playlist(self):
        print("Creating discover weekly playlist....")

        query = API_BASE_URL + "users/" + spotify_user_id + "/playlists"
        
        today = date.today()

        todayFormatted = today.strftime("%d/%m/%Y")

        req_body = json.dumps({
            "name": todayFormatted + "Discover Weekly",
            "description": "Discover Weekly saved playlist",
            "public": True
        })

        response = requests.post(query,
                                 data=req_body,
                                 headers={
                                            "Content-Type": "application/json",
                                            "Authorization": "Bearer {}".format(self.spotify_token)
        })
        
        response_json = response.json()
        print(response,response_json["id"],"\n")

        return response_json["id"]

    def add_to_playlist(self):

        print("Adding Songs.....")

        self.new_playlist_id = self.create_playlist()

        query = API_BASE_URL + "playlists/" + self.new_playlist_id + "/tracks"
        
        req_body = json.dumps({
            "uris":self.tracks
        })

        response = requests.post(query,
                                 data=req_body,
                                 headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})
        response_json = response.json()
        print(response_json)
    
    def getSavedPlaylists(self):

        query = 'https://api.spotify.com/v1/me/tracks'

        response = requests.get(query,headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})
        response = response.json()
        for i in response["items"]:
            songTrack = ""
            songTrack += (i["track"]["uri"])
            self.tracks.append(songTrack)
        
        self.add_to_playlist()

    
                

    
    def call_refresh(self):

        print("Refreshing token")

        refreshCaller = Refresh()

        self.spotify_token = refreshCaller.refresh()

        self.find_songs()




a = SaveSongs()
a.call_refresh()
