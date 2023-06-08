#!/usr/bin/env python3
import random
import requests
import time
from dotenv import load_dotenv
import os
import base64

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


def get_token():
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = josen_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


token = get_token()


def start_playlist_playback(songs, token):
    random.shuffle(songs)  # Randomly sort the array of songs

    for song in songs:
        song_id = song['songid']
        duration_ms = song['duration_ms']

        # Send Spotify API request to start playback for the current song
        # Replace 'YOUR_ACCESS_TOKEN' with the actual access token
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
        data = {
            'uris': [f'spotify:track:{song_id}']
        }
        response = requests.put(
            'https://api.spotify.com/v1/me/player/play',
            headers=headers, json=data)

        if response.status_code == 204:
            print(f'Started playback for song {song_id}.')
            time.sleep(duration_ms / 1000)  # Wait for the specified duration
            token = get_token()
        else:
            print(
                f'Error starting playback for song {song_id}. \
                Status code: {response.status_code}.')
