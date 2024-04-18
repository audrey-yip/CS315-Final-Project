from lyricsgenius import Genius
# https://pypi.org/project/lyricsgenius/
import time

from api_key import access
genius = Genius(access)
# artist = genius.search_artist("Andy Shauf", max_songs=5, sort="title")
# print(artist.songs)
# time.sleep(5)
# song = artist.song("To You")
# print(song)
# song = genius.search_song("To You", artist.name)
# print(song)

# Using Song URL
url = "https://genius.com/Andy-shauf-begin-again-lyrics"
print(genius.lyrics(song_url=url))

# Using Song ID
# Requires an extra request to get song URL
id = 2885745
print(genius.lyrics(id))