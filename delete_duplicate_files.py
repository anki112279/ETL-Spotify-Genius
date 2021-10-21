import csv
import os
#import boto3
from datetime import datetime
import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
from song_lyrics import SongLyrics
import re


def read_files():
    folder_path = 'Users\Test\PycharmProjects\ETL-Spotify\venv\Data\The Longest Playlist Ever'
    for dirname, _, filename in os.walk(folder_path):
        for file in filename:
            print(file)
            break

if __name__ == '__main__':
    read_files()
