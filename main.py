from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "_SPOTIFY_CLIENT_ID_"  # input your own
CLIENT_SECRET = "_SPOTIFY_CLIENT_SECRET_"  # input your own

# spotipy auth and token generation
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

# user input to activate the time machine ;)
travel_date = input("Which year do you want to travel to? e.g. YYYY-MM-DD \n> ")

year = travel_date.split("-")[0]
track_ids = []

# making soup
billboard_res = requests.get(f"https://www.billboard.com/charts/hot-100/{travel_date}")
billboard_site = billboard_res.text
first_soup = BeautifulSoup(billboard_site, "html.parser")
song_titles = first_soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")

# list of songs
all_songs = [title.getText() for title in song_titles]

# create the playlist
playlist_name = f"{travel_date} Billboard 100"
my_playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)

#  sorts through the soup to fetch the songs on spotify
for song in all_songs:
    spotipy_query = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        # get the id's to make the playlist
        track_ids.append(spotipy_query['tracks']['items'][0]['id'])
    # if they don't have the song print the exception
    except IndexError:
        print(f"{song} doesn't exist.")

# user_playlist_add_tracks might be about to be deprecated at the time of this completion
sp.user_playlist_add_tracks(user=user_id, playlist_id=my_playlist["id"], tracks=track_ids)
