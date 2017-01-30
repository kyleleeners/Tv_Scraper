from bs4 import BeautifulSoup
import requests

username = 'yyyyyy'
password = 'xxxxxx'

base_url = 'https://fmovies.se/search?keyword='
next_url = 'https://fmovies.se'

show = raw_input("Enter the show you want to watch: ")
str(show)
show = show.replace(' ','+')
r = requests.get(base_url+show)
soup = BeautifulSoup(r.text, 'lxml')
season = raw_input("Enter the season you want to watch (number): ")
season = str(season)

for link in soup.findAll('a',class_='name'):
    if season in link.getText():
        print(next_url+link.get('href'))





