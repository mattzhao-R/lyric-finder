import time
import os
import csv
import re

import requests
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool

import pandas as pd
import numpy as np

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def make_query(artist,song):
    """
    Makes link to genius lyrics page using artist and song names from Spotify
    
    Input:
        artist (str): artist name
        song (str): song name
    Output:
        Genius.com lyrics link (str)
    """
    base = 'https://genius.com/'
    sfx = '-lyrics'
    art = '-'.join(artist.lower().split(' '))
    sng = '-'.join(song.lower().split(' '))
    link = base + art + '-' + sng + sfx
    return link

def extract_lyrics(artist,song):
    """
    Creates query for genius for a song given the song name
    and artist name and scrapes the lyrics from the website.
    
    Inputs:
        query (str): hyperlink from genius site
    Outputs:
        formatted lyrics (str) from genius
    """
    query = make_query(artist,song)
    req = requests.get(query)
    soup = BeautifulSoup(req.content,'html.parser')
    
    lyric_containers = soup.find_all(name='div',
                                     class_='Lyrics__Container-sc-1ynbvzw-6 YYrds')
    lyrics = ''
    for c in lyric_containers:
        for val in c.contents:
            if isinstance(val,str):
                lyrics = lyrics + val + '\n'
    return lyrics

