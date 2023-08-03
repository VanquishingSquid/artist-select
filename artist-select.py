import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
from os.path import exists

# authorisation
scope = "user-follow-read"
client_id = "" # Get your client_id and client_secret from https://developer.spotify.com/dashboard
client_secret = ""
redirect_uri = "http://localhost"

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

# get all followed artists
artists_data = []
temp_artists = spotify.current_user_followed_artists(limit=50)["artists"]["items"]
artists_data += temp_artists
i = 1
while len(temp_artists) != 0:
    temp_artists = spotify.current_user_followed_artists(limit=50, after=i*50)["artists"]["items"]
    artists_data += temp_artists
    i += 1

# filter out all the unnecessary information
artists_id = []
for artist_data in artists_data:
    artists_id.append([artist_data["name"], artist_data["id"]])
random.shuffle(artists_id)

# read artists from file
artists_file = []
if exists("artists-spotify.txt"):
    file = open("artists-spotify.txt", "r")
    artist_id_from_file = file.readline()
    while artist_id_from_file != "":
        artists_file.append(artist_id_from_file.strip("\n"))
        artist_id_from_file = file.readline()
    file.close()

# give the user artists
i = 0
complete_loop = True
while True:
    if i < len(artists_id):
        if artists_id[i][1] not in artists_file:
            complete_loop = False
            # if the artist is not in the blacklist, ask the user if they want to add them to the blacklist
            print(artists_id[i][0])
            choiche = input("Add to blacklist? ").strip().lower()
            if choiche in ["y", "yes"]:
                artists_file.append(artists_id[i][1])
            elif choiche in ["x", "exit"]:
                break
        i += 1
    else:
        if complete_loop:
            print("You have blacklisted every artist you follow")
            break

        i = 0
        complete_loop = True

# write to the file
string_to_write = ""
for artist_id in artists_file:
    string_to_write += artist_id + "\n"
file = open("artists-spotify.txt", "w")
file.write(string_to_write)
file.close()
