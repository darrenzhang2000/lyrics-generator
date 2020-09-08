import configparser
import requests
from bs4 import BeautifulSoup

def getAccessToken():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['Client_Access_Token']['token']

token = getAccessToken()

def searchMusicArtist(name):
    api_url = "http://api.genius.com/search?q={}".format(name)
    headers = {"authorization": token}
    r = requests.get(api_url, headers=headers)
    return r.json()

def getArtistId(name):
    r = searchMusicArtist(name)
    id = r["response"]["hits"][0]["result"]["primary_artist"]["id"]
    return id

def getTopTenSongs(name):
    id = getArtistId(name)
    api_url = "http://api.genius.com/artists/{}/songs".format(id)
    headers = {"authorization": token}
    params = {
        "sort": "popularity",
        "per_page": 10
    }
    r = requests.get(api_url, headers=headers, params=params)
    return r.json()

def getLyricsArray(name):
    r = getTopTenSongs(name)
    songs = r["response"]["songs"]
    lyrics_array = []
    for song in songs:
        lyrics_array.append(song["url"])
    return lyrics_array

def webScrapeLyrics(name):
    arr = getLyricsArray("Kendrick Lamar")
    songs_lyrics = []
    for url in arr:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        lyrics_div = soup.find(class_="lyrics")
        lyrics_links = lyrics_div.find_all('a')
        current_lyrics = []
        for link in lyrics_links:
            if len(link.text) > 0 and link.text[0] != "[":
                # text = link.text.replace("\n", " NEWLINE ")
                text = link.text.replace("\n", " ")
                current_lyrics.append(text)
        songs_lyrics.append(current_lyrics)
    return songs_lyrics


