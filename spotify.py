import spotipy
import os
import random
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()
scope = "playlist-modify-private playlist-modify-public user-top-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET"), redirect_uri=os.getenv("REDIRECT_URI")))

artist_list = []
track_list = []

#get playlist
playlists = sp.current_user_playlists()
playlist = None
for i, item in enumerate(playlists['items']):
    if item['name'] == "Recommended Daily":
        playlist = item

if playlist == None:
    print("Error: Playlist does not exist")
    exit()

#if playlist has tracks, delete them
playlist_tracks = sp.playlist_tracks(playlist_id = playlist["id"])
old_tracks = []
if playlist_tracks["items"]:
    for i, item in enumerate(playlist_tracks['items']):
        old_tracks.append(item["track"]["id"])   
    sp.playlist_remove_all_occurrences_of_items(playlist_id = playlist["id"], items = old_tracks)

artists = sp.current_user_top_artists(time_range="short_term", limit=20)
for i, item in enumerate(artists['items']):
    artist_list.append(item['id'])

tracks = sp.current_user_top_tracks(time_range="short_term", limit=20)
for i, item in enumerate(tracks['items']):
    track_list.append(item['id'])


recommendations = sp.recommendations(seed_artists = random.choices(artist_list, k=2), seed_tracks = random.choices(track_list, k=3))
rec_track_list = []
for track in recommendations['tracks']:
    rec_track_list.append(track['id'])

test = sp.playlist_add_items(playlist_id=playlist["id"], items = rec_track_list)