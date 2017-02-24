from bs4 import BeautifulSoup
import requests
import sqlite3

# F Movies
base_url = 'https://fmovies.se/search?keyword='
next_url = 'https://fmovies.se'

# SQlite database link, CREATES DB FILE IN SAME LOCATION AS MAIN FILE
sqlite_file = 'scraper_data.db'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# SQL database table
good_table = 'good_links'   # table of good links
good_name = 'good_name'     # name given to good links
good_link = 'good_link'     # good link

bad_table = 'bad_links'     # table of bad links
bad_name = 'bad_name'       # reason link is bad
bad_link = 'bad_link'       # bad link

# Create table for good links
c.execute('''CREATE TABLE IF NOT EXISTS  good_table
    (good_name TEXT , good_link TEXT)''')

# Create table for bad links
c.execute('''CREATE TABLE IF NOT EXISTS  bad_table
    (bad_name TEXT, bad_link TEXT)''')

# Store good links
def store_good(name, url):
    c.execute('''INSERT INTO good_table (good_name, good_link)
    VALUES (?,?) ''',(name,url))

# Store bad links
def store_bad(url, reason):
    c.execute('''INSERT INTO bad_table (bad_name, bad_link)
    VALUES (?,?)''',(url,reason))

# Main menu function
def main_menu():
    option = input("Would you like to: 1. Find new shows 2. Watch old shows ")
    option_guard = ["1", "2"]
    while option not in option_guard:
        print("Sorry, I didn't quite catch that.")
        option = input("Would you like to: 1. Find new shows 2. Watch old shows ")
    if option is "1":
        choose_tv()
    elif option is "2":
        search_db()

# Search db for previously watched shows
def search_db():
    name = input("What show are you looking for?: ")
    query = "SELECT * FROM good_table WHERE good_name=?"
    try:
        c.execute(query, (name,))
        for row in c:
            print(row)
    except:
            print("Sorry, I couldn't find that! Try again.")
            search_db()

# Main function for scraping and storing
def choose_tv():
    show = str(input("Enter the show you want to watch: "))
    show = show.replace(' ', '+')
    r = requests.get(base_url + show)
    soup = BeautifulSoup(r.text, 'lxml')
    season = str(input("Enter the season you want to watch (number): "))
    for link in soup.findAll('a', class_='name'):
        if season in link.getText():
            print(next_url + link.get('href'))
            url = next_url + link.get('href')
            store_link(url)

# Store link as good or bad
def store_link(url):
    response = input("Would you like to store this link for later use? (Y/N)")
    response_guard = ["Y", "y", "N", "n"]
    while response not in response_guard:
        print("Sorry, I didn't quite catch that.")
        response = input("Would you like to store this link for later use? (Y/N)")
    if response is "Y" or "y":
        name = input("What would you like to name it?")
        store_good(name, url)
    else:
        reason = input("Why not?")
        store_bad(url, reason)
    conn.commit()


# main file to start program
def main():
    main_menu()

if __name__ == "__main__":
    main()



