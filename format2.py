import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from concurrent.futures import ThreadPoolExecutor

# Set up Spotify API credentials
SPOTIPY_CLIENT_ID = '21c51f8e6f784d7fadc41f84acf80ab5'
SPOTIPY_CLIENT_SECRET = '584fc966136e4e6989b01d982d7e8ab5'

# Set up Spotify API authentication without redirect URL
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='21c51f8e6f784d7fadc41f84acf80ab5', client_secret='584fc966136e4e6989b01d982d7e8ab5'))

# Load your dataset from CSV using Pandas
df = pd.read_csv('Spotify_Song_Attributes.csv')

# Function to fetch genre information for a track
def fetch_genre(track_id):
    try:
        track_details = sp.track(track_id)
        artists = track_details['artists']

        # Extract genres for each artist (assuming only one genre per artist)
        genres = []
        for artist in artists:
            artist_id = artist['id']
            artist_info = sp.artist(artist_id)
            artist_genres = artist_info['genres'] if artist_info['genres'] else ['N/A']
            genres.extend(artist_genres)

        return genres

    except spotipy.SpotifyException as e:
        print(f"Error for track {track_id}: {e}")
        return ['N/A']

# Use ThreadPoolExecutor for parallel processing
with ThreadPoolExecutor() as executor:
    # Fetch genres in parallel
    genres_list = list(executor.map(fetch_genre, df['track_id']))

# Create a list of dictionaries for DataFrame construction
updated_rows = [{'track_name': row['track_name'],
                'artists': row['artists'],
                'Genre': ', '.join(genres)} for row, genres in zip(df.itertuples(index=False), genres_list)]

# Create the DataFrame from the list of rows
updated_df = pd.DataFrame(updated_rows, columns=['track_name', 'artists', 'Genre'])

# Save the updated DataFrame to a new CSV file
output_csv_file_path = 'song_dataset_with_genres.csv'
updated_df.to_csv(output_csv_file_path, index=False, encoding='utf-8')

print(f"Updated dataset written to: {output_csv_file_path}")
