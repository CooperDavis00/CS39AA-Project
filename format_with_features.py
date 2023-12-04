import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up Spotify API credentials
SPOTIPY_CLIENT_ID = 'your_client_id'
SPOTIPY_CLIENT_SECRET = 'your_client_secret'

# Set up Spotify API authentication without redirect URL
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='21c51f8e6f784d7fadc41f84acf80ab5', client_secret='584fc966136e4e6989b01d982d7e8ab5'))

# Load your dataset from CSV using Pandas
df = pd.read_csv('liked.csv')

# Create a list to store rows
updated_rows = []

# Iterate over rows and fetch genre information
for index, row in df.iterrows():
    track_name = row['Track Name']
    artist_names = row['Artist Name(s)'].split(', ')  # Assuming artistName are separated by a comma and space
    track_uri = row['Track URI']
    
    # Get track details, including artistName, using the Spotify API
    try:
        track_details = sp.track(track_uri)
        artists = track_details['artists']  # List of artists
        audio_features = sp.audio_features(track_uri)[0]  # Get audio features

        genres = []
        for artist in artists:
            artist_id = artist['id']
            artist_info = sp.artist(artist_id)
            artist_genres = artist_info['genres'] if artist_info['genres'] else ['N/A']
            genres.extend(artist_genres)

        # Create a dictionary for the current track's information
        track_info = {
            'Track URI': track_uri,
            'Track Name': track_name,
            'Artist Name(s)': ', '.join(artist_names),
            'genre': ', '.join(genres),
            'danceability': audio_features['danceability'],
            'energy': audio_features['energy'],
            'key': audio_features['key'],
            'loudness': audio_features['loudness'],
            'mode': audio_features['mode'],
            'speechiness': audio_features['speechiness'],
            'acousticness': audio_features['acousticness'],
            'instrumentalness': audio_features['instrumentalness'],
            'liveness': audio_features['liveness'],
            'valence': audio_features['valence'],
            'tempo': audio_features['tempo']
        }

        # Append the track information to the list
        updated_rows.append(track_info)

    except spotipy.SpotifyException as e:
        # If there's an error (e.g., track not found), write 'N/A' for audio features
        print(f"Error for track {track_name}: {e}")
        track_info = {
            'Track URI': track_uri,
            'Track Name': track_name,
            'Artist Name(s)': ', '.join(artist_names),
            'genre': 'N/A',
            'danceability': 'N/A',
            'energy': 'N/A',
            'key': 'N/A',
            'loudness': 'N/A',
            'mode': 'N/A',
            'speechiness': 'N/A',
            'acousticness': 'N/A',
            'instrumentalness': 'N/A',
            'liveness': 'N/A',
            'valence': 'N/A',
            'tempo': 'N/A'
        }

        # Append the track information to the list
        updated_rows.append(track_info)


    except spotipy.SpotifyException as e:
        # If there's an error (e.g., track not found), write 'N/A' for audio features
        print(f"Error for track {track_name}: {e}")
        track_info = {
            'Track Name': track_name,
            'Artist Name(s)': ', '.join(artist_names),
            'genre': 'N/A',
            'danceability': 'N/A',
            'energy': 'N/A',
            'key': 'N/A',
            'loudness': 'N/A',
            'mode': 'N/A',
            'speechiness': 'N/A',
            'acousticness': 'N/A',
            'instrumentalness': 'N/A',
            'liveness': 'N/A',
            'valence': 'N/A',
            'tempo': 'N/A'
        }

        # Append the track information to the list
        updated_rows.append(track_info)

# Create the DataFrame from the list of rows
updated_df = pd.DataFrame(updated_rows)

# Save the updated DataFrame to a new CSV file
output_csv_file_path = 'liked_w_features.csv'
updated_df.to_csv(output_csv_file_path, index=False, encoding='utf-8')

print(f"Updated dataset written to: {output_csv_file_path}")
