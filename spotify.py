from urllib.request import Request
from urllib.request import urlopen
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import os
import re
import requests
import ssl
import json
import sqlite3
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import chart_studio
import numpy as np
import sqlite3
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

# we talked to professor ericson because we realized when
# we were too far into our project that we were using beautiful
# soup to scrape web data instead of an actual API so she suggested
# we add extra visualizations to make up for the 10 points for not 
# using an API instead of trying to change all of our code
# url and beautiful soup
url = 'https://spotifycharts.com/regional'
def getSoupFromURL(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")
    return soup
soup = getSoupFromURL(url)

# create dictionary of top 200 songs from API
# key - song title
# value - artists, rank, streams

spotify = {}
songs = []
strip_dict = {}
chart_list = soup.find('table', class_ = 'chart-table')
song_list = chart_list.find_all('tr')
artists = {}
artists_list = []
artist_index = 0

for song in song_list[1:]:
    # get song info
    song_info = song.find('td', class_ = 'chart-table-track')
    song_title = song_info.strong.text

    # get artist info
    artist_info = song.find('td', class_ = 'chart-table-track')
    artist = artist_info.span.text.strip('by ')
    if artist not in artists:
        artists[artist.strip()] = artist_index
        artists_list.append({
            "artist": artist.strip(),
            "index": artist_index
        })
        artist_index += 1

    # get rank info
    position_info = song.find('td', class_ = 'chart-table-position')
    position = position_info.text

    # get stream info
    stream_info = song.find('td', class_ = 'chart-table-streams')
    stream = stream_info.text

    songs.append({
        "song": song_title.strip(),
        "artist": artists[artist.strip()],
        "rank": position.strip(),
        "streams": stream.strip()
    })

    spotify[song_title.strip()] = (artist.strip(), position.strip(), stream.strip())
    strip_dict[position.strip()] = stream.strip()

# write songs to database
full_path = os.path.dirname(os.path.realpath(__file__)) + '/' + 'data.db'
conn = sqlite3.connect(full_path)
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS artists (id INTEGER PRIMARY KEY, name text)")
cur.execute("CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY, name text, artist_id text, rank int, streams int)")
conn.commit()

query = "SELECT * FROM songs"
cur.execute(query)
results = cur.fetchall()

if len(results) == 20:

    # insert data 20 items at a time
    cur.executemany("INSERT INTO artists (id, name) VALUES (:index, :artist);", artists_list)
    cur.executemany("INSERT INTO songs (name, artist_id, rank, streams) VALUES (:song, :artist, :rank, :streams);", songs)
    conn.commit()

# initializes top 10 artists
edsheeran = 0
percent_ed = 0
postmalone = 0
percent_post = 0
camilacabello = 0
percent_camila = 0
jbalvin = 0
percent_j = 0
khalid = 0
percent_khalid = 0
arianagrande = 0
percent_ariana = 0
justinbieber = 0
percent_justin = 0
billieeilish = 0
percent_billie = 0
maroon5 = 0
percent_maroon = 0
shawnmendes = 0
percent_shawn = 0
total_streams = 0

for song in cur.execute("SELECT streams FROM songs").fetchall():
    count = song[0]
    streams = count.replace(',', '')
    total_streams += int(streams)

for song in cur.execute("SELECT streams FROM songs, artists WHERE songs.artist_id = artists.id AND artists.name = 'Ed Sheeran'"):
    streams = song[0].replace(',', '')
    edsheeran += int(streams)
    percent_ed = (edsheeran/total_streams)*100

for song in cur.execute("SELECT streams FROM songs, artists WHERE songs.artist_id = artists.id AND artists.name = 'Post Malone'"):
    streams = song[0].replace(',', '')
    postmalone += int(streams)
    percent_post = (postmalone/total_streams)*100

for song in cur.execute("SELECT streams FROM songs, artists WHERE songs.artist_id = artists.id AND artists.name = 'Camila Cabello'"):
    streams = song[0].replace(',', '')
    camilacabello += int(streams)
    percent_camila = (camilacabello/total_streams)*100

for song in cur.execute("SELECT streams FROM songs, artists WHERE songs.artist_id = artists.id AND artists.name = 'J Balvin'"):
    streams = song[0].replace(',', '')
    jbalvin += int(streams)
    percent_j = (jbalvin/total_streams)*100

for song in cur.execute("SELECT streams FROM songs, artists WHERE songs.artist_id = artists.id AND artists.name = 'Khalid'"):
    streams = song[0].replace(',', '')
    khalid += int(streams)
    percent_khalid = (khalid/total_streams)*100

for song in cur.execute("SELECT streams FROM songs, artists WHERE songs.artist_id = artists.id AND artists.name = 'Ariana Grande'"):
    streams = song[0].replace(',', '')
    arianagrande += int(streams)
    percent_ariana = (arianagrande/total_streams)*100

for song in cur.execute("SELECT streams FROM songs, artists WHERE songs.artist_id = artists.id AND artists.name = 'Justin Bieber'"):
    streams = song[0].replace(',', '')
    justinbieber += int(streams)
    percent_justin = (justinbieber/total_streams)*100

for song in cur.execute("SELECT streams FROM songs, artists WHERE songs.artist_id = artists.id AND artists.name = 'Billie Eilish'"):
    streams = song[0].replace(',', '')
    billieeilish += int(streams)
    percent_billie = (billieeilish/total_streams)*100

for song in cur.execute("SELECT streams FROM songs, artists WHERE songs.artist_id = artists.id AND artists.name = 'Maroon 5'"):
    streams = song[0].replace(',', '')
    maroon5 += int(streams)
    percent_maroon = (maroon5/total_streams)*100

for song in cur.execute("SELECT streams FROM songs, artists WHERE songs.artist_id = artists.id AND artists.name = 'Shawn Mendes'"):
    streams = song[0].replace(',', '')
    shawnmendes += int(streams)
    percent_shawn = (shawnmendes/total_streams)*100

dict_pie_chart = {}
dict_pie_chart['Ed Sheeran'] = [edsheeran, percent_ed]
dict_pie_chart['Post Malone'] = [postmalone, percent_post]
dict_pie_chart['Camila Cabello'] = [camilacabello, percent_camila]
dict_pie_chart['J Balvin'] = [jbalvin, percent_j]
dict_pie_chart['Khalid'] = [khalid, percent_khalid]
dict_pie_chart['Ariana Grande'] = [arianagrande, percent_ariana]
dict_pie_chart['Justin Bieber'] = [justinbieber, percent_justin]
dict_pie_chart['Billie Eilish'] = [billieeilish, percent_billie]
dict_pie_chart['Maroon 5'] = [maroon5, percent_maroon]
dict_pie_chart['Shawn Mendes'] = [shawnmendes, percent_shawn]

plotly.tools.set_credentials_file(username="minacohen", api_key="vHi4HgiCvLkgYkiwV1dr")

from IPython.display import IFrame
IFrame(src= "https://dash-simple-apps.plotly.host/dash-figurelabelsplot/", width="100%", height="850px", frameBorder="0")

# write to file as text
full_path = os.path.dirname(os.path.realpath(__file__)) + '/' + 'spotify_data.json'
with open(full_path, 'w') as fp:
    fp.write(json.dumps(dict_pie_chart))

# make pie chart
labels = ['Ed Sheeran', 'Post Malone', 'Camila Cabello', 'J Balvin', 'Khalid', 'Ariana Grande', 'Justin Bieber', 'Billie Eilish', 'Maroon 5', 'Shawn Mendes']
values = [edsheeran, postmalone, camilacabello, jbalvin, khalid, arianagrande, justinbieber, billieeilish, maroon5, shawnmendes]
colors = ['#dea2eb', '#eba9a2', '#ceeba2', '#f0ed95', 'white', '#eba2c0', '#19fc00', '#a2b3eb', '#a2ebd0', '#95dff0']

trace = go.Pie(labels=labels, values=values, title="Song Streams of Top 10 Artists in Spotify's Global Top 200",
               hoverinfo='label', textinfo='value+percent', 
               textfont=dict(size=9),
               marker=dict(colors=colors, 
               line=dict(color='#000000', width=1)))

py.iplot([trace], filename='styled_pie_chart', auto_open=True)

# make scattergram
# Create data
x = [1,2,3,4,5,6,7,8,9,10]
y = [6371150,4242225,4077010,3751385,3647985,3584054,3309744,3164740,3129922,2959965]
colors = '#6126eb'
area = np.pi*20

# Plot
plt.scatter(x, y, s=area, c=colors, alpha=0.5, marker="*")
plt.title('Streams Compared to Rank of Top 10 Songs in Spotify Global Top 200')
plt.xlabel('Rank')
plt.ylabel('Streams')
plt.show()