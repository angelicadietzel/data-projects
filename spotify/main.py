import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import pandas as pd


# connect to the API
client_id = '3812e6dedc9440c09c1fd0fdf1ae5151'
client_secret = '4f85dee16915458085f06334e1c08ae7'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def getTrackIDs(user, playlist_id):
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids

ids = getTrackIDs('angelicadietzel', '4R0BZVh27NUJhHGLNitU08') 

def getTrackFeatures(id):
      meta = sp.track(id)
      features = sp.audio_features(id)

      # meta
      name = meta['name']
      album = meta['album']['name']
      artist = meta['album']['artists'][0]['name']
      release_date = meta['album']['release_date']
      length = meta['duration_ms']
      popularity = meta['popularity']

      # features
      acousticness = features[0]['acousticness']
      danceability = features[0]['danceability']
      energy = features[0]['energy']
      instrumentalness = features[0]['instrumentalness']
      liveness = features[0]['liveness']
      loudness = features[0]['loudness']
      speechiness = features[0]['speechiness']
      tempo = features[0]['tempo']
      time_signature = features[0]['time_signature']

      track = [name, album, artist, release_date, length, popularity, danceability, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
      return track

#loop over track ids to create dataset
tracks = []
for i in range(0,len(ids)):
    time.sleep(.5)
    track = getTrackFeatures(ids[i])
    tracks.append(track)

df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])

df.to_csv("spotify.csv", sep = ',')
