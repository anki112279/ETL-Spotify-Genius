import requests
import bs4 as bs
import urllib.request
class SongLyrics():
    def __init__(self, genius_key):
        self.genius_key = genius_key

    def request_song_info(self, track_name, track_artist):
        base_url = 'https://api.genius.com'
        headers = {'Authorization': 'Bearer ' + self.genius_key}
        search_url = base_url + '/search'
        data = {'q': track_name + ' ' + track_artist}
        response = requests.get(search_url, data=data, headers=headers)
        return response

    def get_lyrics(self, track_name, track_artist):
        response = SongLyrics.request_song_info(self, track_name, track_artist)
        try:
            url = response.json()['response']['hits'][0]['result']['url']
            if url == None:
                return
            lyrics = SongLyrics.scrape_lyrics(url)
            if lyrics == None:
                print(f"Track is not in the Genius database.")
            else:
                lyrics = str(lyrics)
                print(f"Retrieved track lyrics!")
        except IndexError:
            return
        return lyrics

    def scrape_lyrics(song_url):
        page = requests.get(song_url)
        html = bs.BeautifulSoup(page.text, 'html.parser')
        lyrics1 = html.find("div", class_="lyrics")
        lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-2 jgQsqn")
        if lyrics1:
            lyrics = lyrics1.get_text()
        elif lyrics2:
            lyrics = lyrics2.get_text()
        elif lyrics1 == lyrics2 == None:
            lyrics = None
        return lyrics