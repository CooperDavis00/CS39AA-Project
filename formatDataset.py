import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up Spotify API credentials
SPOTIPY_CLIENT_ID = 'your_client_id'
SPOTIPY_CLIENT_SECRET = 'your_client_secret'

# Set up Spotify API authentication without redirect URL
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='21c51f8e6f784d7fadc41f84acf80ab5', client_secret='584fc966136e4e6989b01d982d7e8ab5'))

# Load your dataset from CSV using Pandas
df = pd.read_csv('Spotify_Song_Attributes.csv')

# Create a list to store rows
updated_rows = []

# Iterate over rows and fetch genre information
for index, row in df.iterrows():
    track_name = row['trackName']
    artist_names = row['artistName'].split(', ')  # Assuming artistName are separated by a comma and space
    # track_uri = row['Track URI']
    track_id = row['id']

    # Get track details, including artistName, using the Spotify API
    try:
        track_details = sp.track(track_id)
        artistName = track_details['artistName']

        # Extract genres for each artist (assuming only one genre per artist)
        genres = []
        for artist in artistName:
            artist_id = artist['id']
            artist_info = sp.artist(artist_id)
            artist_genres = artist_info['genres'] if artist_info['genres'] else ['N/A']
            genres.extend(artist_genres)

        # Create a dictionary for the current track's information
        track_info = {'trackName': track_name,
                    'artistName': ', '.join(artist_names),
                    'Genre': ', '.join(genres)}

        # Append the track information to the list
        updated_rows.append(track_info)

    except spotipy.SpotifyException as e:
        # If there's an error (e.g., track not found), write 'N/A' for genre
        print(f"Error for track {track_name}: {e}")
        track_info = {'trackName': track_name,
                    'artistName': ', '.join(artist_names),
                    'Genre': 'N/A'}

        # Append the track information to the list
        updated_rows.append(track_info)

# Create the DataFrame from the list of rows
updated_df = pd.DataFrame(updated_rows, columns=['trackName', 'artistName', 'Genre'])

# Save the updated DataFrame to a new CSV file
output_csv_file_path = 'song_dataset.csv'
updated_df.to_csv(output_csv_file_path, index=False, encoding='utf-8')

print(f"Updated dataset written to: {output_csv_file_path}")
