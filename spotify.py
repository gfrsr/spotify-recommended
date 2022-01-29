import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()
scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET"), redirect_uri=os.getenv("REDIRECT_URI")))

playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None