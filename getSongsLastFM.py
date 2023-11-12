import requests
from bs4 import BeautifulSoup
import random
import time

# The Last.fm API Key
API_KEY = "YOUR_API_KEY"

# Get a list of all artists on Last.fm
def get_all_artists():
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "tag.gettopartists",
        "tag": "rock",
        "api_key": API_KEY,
        "format": "json",
    }
    response = requests.get(url, params=params)
    data = response.json()
    artists = [artist["name"] for artist in data["topartists"]["artist"]]
    return artists

# Get a random song from an artist
def get_random_song(artist):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "artist.gettoptracks",
        "artist": artist,
        "api_key": API_KEY,
        "format": "json",
    }
    response = requests.get(url, params=params)
    data = response.json()
    tracks = data["toptracks"]["track"]
    if tracks:
        random_track = random.choice(tracks)
        song = {
            "title": random_track["name"],
            "artist": artist,
            "genre": random_track["genre"],
            "popularity": random_track["listeners"],
        }
        return song
    else:
        return None

# Generate a dataset of 10,000 random songs
def generate_dataset():
    dataset = []
    all_artists = get_all_artists()
    for _ in range(10000):
        random_artist = random.choice(all_artists)
        song = get_random_song(random_artist)
        if song:
            dataset.append(song)
        time.sleep(1) # Be nice to the Last.fm API and wait 1 second between requests
    return dataset

# Write the dataset to a CSV file
def write_dataset_to_csv(dataset):
    with open("lastfm_dataset.csv", "w") as f:
        f.write("title,artist,genre,popularity\n")
        for song in dataset:
            line = ",".join([song[key] for key in song])
            f.write(line + "\n")

if __name__ == "__main__":
    dataset = generate_dataset()
    write_dataset_to_csv(dataset)
    print("Dataset saved to lastfm_dataset.csv")