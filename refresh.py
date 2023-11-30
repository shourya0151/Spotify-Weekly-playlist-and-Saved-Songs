import requests
import json
from secret import refresh_token, base_64,client_id

class Refresh:
    def __init__(self):
        self.refresh_token = refresh_token
        self.base_64 = base_64
        self.client_id = client_id

    def refresh(self):
        
        query = 'https://accounts.spotify.com/api/token'

        req_data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }

        headers = {
            'Authorization': 'Basic ' + base_64
        }

        response = requests.post(query,
                                 data = req_data,
                                 headers = headers
                                 )
        response_json = response.json()
        return response_json['access_token']

