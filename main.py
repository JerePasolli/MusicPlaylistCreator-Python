from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

date = input("Wich year of music would you like to travel to? Type the date in the format: YYYY-MM-DD:\n")
year = date.split("-")[0]
url = f"https://www.billboard.com/charts/hot-100/{date}/"
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
songs = [song.getText().strip() for song in soup.select("li ul li h3")]

spoty = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="Jere Pasolli",
    )
)
user_id = spoty.current_user()["id"]
spotify_URIs = []
print("Creating list of spotify songs")
for song in songs:
    result = spoty.search(q=f"track:{song} year:{year}", type="track")
    try:
        spotify_URIs.append(result["tracks"]["items"][0]["uri"])
    except IndexError:
        print(f"{song} is not available on Spotify. Skipped")

print("Creating Playlist")
playlist = spoty.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print("Adding songs to playlist")
spoty.playlist_add_items(playlist_id=playlist["id"], items=spotify_URIs)

