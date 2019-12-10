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
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt2
import matplotlib.pyplot as plt2; plt2.rcdefaults()
import numpy as np

# we talked to professor ericson because we realized when
# we were too far into our project that we were using beautiful
# soup to scrape web data instead of an actual API so she suggested
# we add extra visualizations to make up for the 10 points for not 
# using an API instead of trying to change all of our code
# url and beautiful soup
url = 'https://www.billboard.com/charts/billboard-200'
def getSoupFromURL(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")
    return soup
soup = getSoupFromURL(url)

# create a dictionary of the top 100 billboard chart
# key - song title
# value - artist and rank

def scrape_data(soup):
    billboard = {}
    chart_list = soup.find_all('li',class_ = 'chart-list__element')
    for song in chart_list:
        # song info
        song_info = song.find('span', class_ = 'chart-element__information__song')
        song_title = song_info.text

        # artist info
        artist_info = song.find('span', class_ = 'chart-element__information__artist')
        artist = artist_info.text

        # rank info
        ranking_info = song.find('span', class_ = 'chart-element__rank__number')
        ranking = ranking_info.text

        # # duration info
        # duration_info = song.find_all('div', class_ = 'chart-element__metas')
        # duration_info_rank = duration_info.find_all('div', class_ = 'chart-element__meta')
        # duration = duration_info_rank.text

        # add to billboard dictionary 
        billboard[song_title.strip()] = [artist.strip(), ranking.strip()]

    return billboard

# scrape data from api 
billboard_obj = scrape_data(soup)

# write cache to file
f = open('billboard_data_cache.json','w')
f.write(json.dumps(billboard_obj))
f.close()

# make sqlite database
def make_database(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    statement='''DROP TABLE IF EXISTS 'Billboard';'''
    statement2='''DROP TABLE IF EXISTS 'Ranks';'''
    cur.execute(statement)
    cur.execute(statement2)
    conn.commit()
    statement= '''CREATE TABLE Billboard (song TEXT, artist TEXT)'''
    statement2= '''CREATE TABLE Ranks (song TEXT, artist TEXT, ranking INTEGER)'''
    cur.execute(statement)
    cur.execute(statement2)
    conn.commit()
    conn.close()

def populate_database(db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()

    for song in billboard_obj.keys():
        song_title = song
        artist_name = billboard_obj[song_title][0]
        cur.execute('''INSERT INTO 'Billboard' (song, artist) VALUES (?,?)''', (song_title,artist_name))
    conn.commit()

    for song in billboard_obj.keys():
        song_title = song
        artist_name = billboard_obj[song_title][0]
        rankings = int(billboard_obj[song_title][1])
        cur.execute('''INSERT INTO 'Ranks' (song, artist, ranking) VALUES (?,?,?)''', (song_title,artist_name,rankings))
    conn.commit()

# write to file as text
db = os.path.dirname(os.path.realpath(__file__)) + '/' + 'data.db'
make_database(db)

populate_database(db)
conn=sqlite3.connect(db)
cur=conn.cursor()

postmalone = []
for song in cur.execute("SELECT song FROM Billboard WHERE artist = 'Post Malone'"):
    postmalone.append(song)
print(len(postmalone))

billieeilish = []
for song in cur.execute("SELECT song FROM Billboard WHERE artist = 'Billie Eilish'"):
    billieeilish.append(song)
print(len(billieeilish))

jasonaldean = []
for song in cur.execute("SELECT song FROM Billboard WHERE artist = 'Jason Aldean'"):
    jasonaldean.append(song)
print(len(jasonaldean))

taylorswift = []
for song in cur.execute("SELECT song FROM Billboard WHERE artist = 'Taylor Swift'"):
    taylorswift.append(song)
print(len(taylorswift))

lizzo = []
for song in cur.execute("SELECT song FROM Billboard WHERE artist = 'Lizzo'"):
    lizzo.append(song)
print(len(lizzo))

lukecombs = []
for song in cur.execute("SELECT song FROM Billboard WHERE artist = 'Luke Combs'"):
    lukecombs.append(song)
print(len(lukecombs))

dababy = []
for song in cur.execute("SELECT song FROM Billboard WHERE artist = 'DaBaby'"):
    dababy.append(song)
print(len(dababy))

trippieredd = []
for song in cur.execute("SELECT song FROM Billboard WHERE artist = 'Trippie Redd'"):
    trippieredd.append(song)
print(len(trippieredd))

coldplay = []
for song in cur.execute("SELECT song FROM Billboard WHERE artist = 'Coldplay'"):
    coldplay.append(song)
print(len(coldplay))

khalid = []
for song in cur.execute("SELECT song FROM Billboard WHERE artist = 'Khalid'"):
    khalid.append(song)
print(len(khalid))

a = 'Post Malone'
b = 'Billie Eilish'
c = 'Jason Aldean'
d = 'Taylor Swift'
e = 'Lizzo'
f = 'Luke Combs'
g = 'DaBaby'
h = 'Trippie Redd'
i = 'Coldplay'
j = 'Khalid'

dic = {}
dic[a] = postmalone
dic[b] = billieeilish
dic[c] = jasonaldean
dic[d] = taylorswift
dic[e] = lizzo
dic[f] = lukecombs
dic[g] = dababy
dic[h] = trippieredd
dic[i] = coldplay
dic[j] = khalid

z = open('top_10_artists.json','w')
z.write(json.dumps(dic))

# make bar chart

objects = ('Post Malone', 'Billie Eilish', 'Jason Aldean', 'Taylor Swift', 'Lizzo', 'Luke Combs', 'DaBaby', 'Trippie Redd', 'Coldplay', 'Khalid')
y_pos = np.arange(len(objects))
performance = [len(dic[a]) for a in objects]

plt.barh(y_pos, performance, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('Number of Songs in Top 200')
plt.title('Top 10 Artists in the Billboard Top 200')
plt.show()

# make scattergram
# Create data
x = [1,2,3,4,5,6,7,8,9,10]
y = [6,1,2,2,9,1,2,3,7,2]
colors = '#34eb8f'
area = np.pi*20

# Plot
plt2.scatter(x, y, s=area, c=colors, alpha=0.5, marker="D")
plt2.title('Length of Song Title Compared to Rank in Billboard Top 200')
plt2.xlabel('Rank')
plt2.ylabel('Length of Song Title')
plt2.show()


