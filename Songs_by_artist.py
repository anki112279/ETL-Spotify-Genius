import csv
import os
#import boto3
from datetime import datetime
import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
from song_lyrics import SongLyrics
import re

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
final_data_dictionary = { 'Id':[], 'Album Name' : [],'Date Released':[],'Artist': [], 'Total Tracks': [],
                        'Popularity':[], 'Song Name':[], 'Song Duration':[] }
genius_key = 'b2q1rosqGNy-UI2Z6vyX8_qywpJHZUnM6pXN9NbTlybXEG4-MRBC4cImVo53OPDb'

def get_playlist_songs(playlist_url):
    '''
    :playlist_url: weblink of the spotify playlist
    :return: return a dictionary with relevant information about the album
    '''
    date = datetime.now()
    (dict_artist_id, playlist_name) = all_artist_in_playlist(playlist_url)
    artist_name_set = set()
    filename = f'{playlist_name}-{date.year}-{date.month}-{date.day}.csv'
    #s3_resource = boto3.resource('s3')
    if os.path.isdir(os.path.join("Data", playlist_name)):
        pass
    else:
        playlist_folder = os.path.join("Data",playlist_name )
        os.mkdir(playlist_folder)
    with open(filename, 'w', encoding='utf-8') as file:
        header = list(final_data_dictionary.keys())
        writer = csv.DictWriter(file, fieldnames= header)
        writer.writeheader()
        num_id = 0
        for artist_name in dict_artist_id.keys():
            if artist_name not in artist_name_set and dict_artist_id.get(artist_name) is not None:
                artist_name_set.add(artist_name)
                artist_id = dict_artist_id.get(artist_name)
                album_obtained = []
                artist_album = spotify.artist_albums(artist_id = artist_id, album_type = 'album')
                for album in artist_album['items']:
                    if 'GB' and 'US' in album['available_markets']:
                        album_data = spotify.album(album['uri'])
                        album_name = album_data['name']
                        release_date = album_data['release_date']
                        popularity = album_data['popularity']
                        album_tracks_num = album_data['total_tracks']
                        key = album_name + artist_name + release_date[:4]
                        if key not in album_obtained:
                            album_obtained.append(key)
                            for song in album_data['tracks']['items']:
                                num_id+=1
                                song_name = song['name']
                                song_duration = song['duration_ms']
                                song_obj = SongLyrics(genius_key)
                                #song_lyrics = song_obj.get_lyrics(song_name, artist_name)
                                writer.writerow({
                                         'Id': num_id,
                                         'Album Name' : album_name,
                                         'Date Released': release_date,
                                         'Artist': artist_name,
                                         'Total Tracks' : album_tracks_num,
                                         'Popularity' : popularity,
                                         'Song Name' : song_name,
                                         'Song Duration': song_duration})
                                # if song_lyrics is not None :
                                #     song_name_corrected = re.sub(r'\W+', ' ', song_name)
                                #     lyrics_filename = f'Data/{playlist_name}/{num_id}_{song_name_corrected}.txt'
                                #     lyrics_file = write_song_lyrics(lyrics_filename, song_name, song_lyrics)
                                    #response = s3_resource.Object(bucket_name='spotify-data-ml-training',
                                                                  #key=lyrics_file).upload_file(lyrics_file)

    #response = s3_resource.Object(bucket_name = 'spotify-data-ml-training', key = filename).upload_file(filename)
    return final_data_dictionary

def write_song_lyrics(lyrics_filename, song_name, song_lyrics):
    with open( lyrics_filename, 'w', encoding='utf-8') as lyrics_file:
        song_writer = csv.DictWriter(lyrics_file, fieldnames={'Song Name': [], 'Song Lyrics': []})
        song_writer.writerow({
                'Song Name': 'Song Name: ' + song_name,
                'Song Lyrics': song_lyrics})
    return lyrics_filename

def all_artist_in_playlist(url):
    artists = {}
    playlist_tracks = spotify.playlist_tracks(playlist_id=url)
    playlist_info = spotify.playlist(playlist_id=url)
    playlist_name = playlist_info['name']
    for song in playlist_tracks['items']:
        if song['track']:
            artists[song['track']['artists'][0]['uri']] = song['track']['artists'][0]['name']
    dict_art_reverse = {k:v for v, k in artists.items()}
    return dict_art_reverse, playlist_name


if __name__ == '__main__':
    data = get_playlist_songs('https://open.spotify.com/playlist/6yPiKpy7evrwvZodByKvM9')





