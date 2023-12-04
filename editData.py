import pandas as pd
import os

print(os.getcwd())

df = pd.read_csv('dataset.csv')

new_df = df.drop(['track_id', 'album_name', 'duration_ms', 'explicit', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature' ], axis=1)

new_df.to_csv('songsDataset4600.csv', index=False)