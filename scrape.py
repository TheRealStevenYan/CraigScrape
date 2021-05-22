import time
from queue import LifoQueue

import requests
from bs4 import BeautifulSoup

'''
TO DO:
Add persistence to search queries - if the script is ever stopped, it will pick up without notifying about old listings
Make this scrape beyond craigslist vancouver
Add categories: make it so we can scrape from 'electronics' section if specified, etc
Move hashmap to outside of SearchQuery class to make the posts universally only notify once
'''


# Saves HTML content of web page to the file stored at file_path
def save_html(html, file_path):
    with open(file_path, 'wb') as file:
        file.write(html)


# Opens the text stored at file_path
def open_html(file_path):
    with open(file_path, 'rb') as file:
        return file.read()


# Returns a list of strings containing the title, post ID and direct link to new postings.
def search_listings(query):
    url = 'https://vancouver.craigslist.org/search/sss?sort=new&query={query}'.format(query=query)
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.select('.hdrlnk')
    return results


# Parses a new search result into a title, id and link.
def parse_search_results(result):
    title = result.get_text()
    id = result.get('id')[7:]
    link = result.get('href')
    return title, id, link


# Returns formatted string for search result given title, id and link.
def get_formatted_results(title, id, link):
    id = 'Post ID: {}'.format(id)
    link = 'Link: {}'.format(link)
    return '{}\n{}\n{}'.format(title, id, link)


'''
The SearchQuery class keeps track of specific search queries, as its name implies.
A SearchQuery class will periodically ping the website with its given search query,
and update the user iff it detects new posts. 
If it finds an already existing post, does nothing.

Hash table is used to keep track of previous postings to prevent duplicate posts.
Notification backlog represented by LIFO queue represent a backlog of postings to notify the user with.
'''


class SearchQuery:
    def __init__(self, query):
        self.hashtable = dict()
        self.notification_backlog = LifoQueue(400)
        self.query = query
        self.search()
        self.periodic_tasks()

    # Periodic tasks to run. Subject to change later.
    def periodic_tasks(self):
        while True:
            self.search()
            self.notify_user()
            time.sleep(60)

    # Notifies the user about new listings while the notification backlog has stuff.
    def notify_user(self):
        while not self.notification_backlog.empty():
            notification = self.notification_backlog.get()
            print(notification)

    # Runs a search using the given query.
    # Immediately stops the search when it encounters a posting it has seen before.
    # Also run when the program is initialised.
    def search(self):
        results = search_listings(self.query)

        for result in results:
            title, id, link = parse_search_results(result)

            if self.hashtable.get(id):
                break

            self.hashtable.update({id: title})
            self.notification_backlog.put(get_formatted_results(title, id, link))


a = SearchQuery('bike')
