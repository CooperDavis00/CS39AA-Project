import requests
import json

client_id = '21c51f8e6f784d7fadc41f84acf80ab5'
client_secret = '584fc966136e4e6989b01d982d7e8ab5'

# Redirect URI specified in your Spotify Developer Dashboard
redirect_uri = 'http://localhost/callback'

# Step 1: Direct the user to the Spotify authorization page
auth_url = f'https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=user-library-read'
print(f'Visit the following URL to authorize your application:\n{auth_url}')

# Step 2: Get the authorization code from the user
authorization_code = input('Enter the authorization code from the URL: ')

# Step 3 and 4: Exchange the authorization code for an access token
token_url = 'https://accounts.spotify.com/api/token'
token_data = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'redirect_uri': redirect_uri,
}

token_headers = {
    'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode(),
}

token_response = requests.post(token_url, data=token_data, headers=token_headers)
token_data = token_response.json()
access_token = token_data.get('access_token')

# Use the access token to make requests
if access_token:
    # Example: Search for songs
    search_query = ''  # Modify as needed (here, it searches for tracks starting with the letter 'a')
    search_url = 'https://api.spotify.com/v1/search'
    search_params = {'q': search_query, 'type': 'track', 'limit': 5}  # Limit to 5 for demonstration

    search_response = requests.get(search_url, headers={'Authorization': f'Bearer {access_token}'}, params=search_params)

    if search_response.status_code == 200:
        search_results = search_response.json()
        tracks = search_results.get('tracks', {}).get('items', [])

        for track in tracks:
            title = track.get('name', 'N/A')
            artist = ', '.join([a.get('name', 'N/A') for a in track.get('artists', [])])
            print(f'Searched Track - Title: {title}, Artist(s): {artist}')
    else:
        print(f"Failed to retrieve search results: {search_response.status_code} - {search_response.text}")

else:
    print(f"Failed to obtain access token: {token_response.status_code} - {token_response.text}")
