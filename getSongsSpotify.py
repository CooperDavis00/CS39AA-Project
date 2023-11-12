import requests
import json
import base64
import time
import csv

def get_access_token(client_id, client_secret):
    token_url = 'https://accounts.spotify.com/api/token'
    token_data = {'grant_type': 'client_credentials'}
    token_headers = {'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}

    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    token_data = token_response.json()
    access_token = token_data.get('access_token')

    return access_token

def get_genre_tracks(access_token, genre, limit=50):
    recommendations_url = 'https://api.spotify.com/v1/recommendations'
    recommendations_params = {'seed_genres': genre, 'limit': limit}

    retry_count = 0
    max_retries = 3  # You can adjust the number of retries as needed

    while retry_count < max_retries:
        recommendations_response = requests.get(recommendations_url, headers={'Authorization': f'Bearer {access_token}'}, params=recommendations_params)

        if recommendations_response.status_code == 200:
            recommendations_data = recommendations_response.json()
            tracks = recommendations_data.get('tracks', [])

            if not tracks:
                print(f"No tracks found for the genre: {genre}")
                return []

            return tracks
        elif recommendations_response.status_code == 429:
            # If rate limited, wait with exponential backoff
            retry_count += 1
            wait_time = 2**retry_count  # Exponential backoff
            print(f"Rate limited. Retrying in {wait_time} seconds... (Attempt {retry_count}/{max_retries})")
            time.sleep(wait_time)
        else:
            print(f"Failed to retrieve recommendations: {recommendations_response.status_code} - {recommendations_response.text}")
            return []

    print("Exceeded maximum retries. Consider adjusting the script.")
    return []

def save_to_csv(data):
    with open('spotify_tracks.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['artist', 'song_title', 'popularity', 'genre'])

        for track in data:
            artists = [artist['name'] for artist in track['artists']]
            artist = ', '.join(artists)
            song_title = track['name']
            popularity = track['popularity']
            genre = track['genre']

            csv_writer.writerow([artist, song_title, popularity, genre])

if __name__ == '__main__':
    # ... (same as before)

    while offset < total_tracks:
        genre_tracks = get_genre_tracks(access_token, genre, limit_per_search)
        if not genre_tracks:
            break

        tracks.extend(genre_tracks)
        offset += limit_per_search

    save_to_csv(tracks)