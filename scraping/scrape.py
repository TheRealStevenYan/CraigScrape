from queue import LifoQueue

import requests
from bs4 import BeautifulSoup

from scraping.craigslist_urls import get_search_url


# Saves the given post ID to 'previous_post_ids'
def log_post_id(post_id):
    with open('scraping\previous_post_ids', 'a') as file:
        file.write('{}\n'.format(post_id))


# Opens the text stored at file_path
def get_post_ids():
    with open('scraping\previous_post_ids', 'r') as file:
        post_ids = [line.rstrip() for line in file]

    return post_ids


# Returns a list of strings containing the title, post ID and direct link to new postings, given a query and category.
def search_listings(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.select('.result-info')
    return results


# Parses a new search result into a title, id, price and link.
def parse_search_results(result):
    try:
        price = result.select_one('.result-price').get_text()
    except AttributeError:
        price = 'Unspecified'

    result_link = result.select_one('.hdrlnk')

    title = result_link.get_text()
    id = result_link.get('id')[7:]
    link = result_link.get('href')

    time = get_posting_time(link)

    return title, id, price, time, link


# Returns the time since a given listing was first posted to Craigslist, given a url to the posting.
def get_posting_time(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    time = soup.select_one('.timeago').get_text().strip()
    return time


# Returns formatted string for search result given title, id, price and link.
def get_formatted_results(title, id, price, time, link):
    id = 'Post ID: {}'.format(id)
    link = 'Link: {}'.format(link)
    price = 'Price: {}'.format(price)
    time = 'Posted: {}'.format(time)
    return '---\n{}\n{}\n{}\n{}\n{}\n---'.format(title, id, price, time, link)


class SearchQuery:
    """
    The SearchQuery class keeps track of specific search queries, as its name implies.
    A SearchQuery class will periodically ping the website with its given search query,
    and update the user iff it detects new posts.
    If it finds an already existing post, does nothing.
    """
    # Use a list to keep track of previously searched ID's.
    previous_ids = get_post_ids()

    def __init__(self, query, category='all'):
        # Instance variables keeping track of search details.
        self.query = query
        self.category = category
        self.url = get_search_url(query, category)

        # Notification backlog represented by LIFO queue represent a backlog of postings to notify the user with.
        # Last item is the first thing to be notified, hence LIFO.
        self.notification_backlog = LifoQueue(400)

    # Periodic tasks to run. Runs a search and returns a notification backlog for the bot to manage.
    async def run_search(self):
        await self.search()
        backlog = self.notification_backlog
        self.notification_backlog = LifoQueue(400)
        return backlog

    # Returns keyword for search query.
    def get_keyword(self):
        return self.query

    # Runs a search using the given query.
    # Immediately stops the search when it encounters a posting it has seen before.
    # Also run when the program is initialised.
    async def search(self):
        results = search_listings(self.url)

        for result in results:
            title, id, price, time, link = parse_search_results(result)

            if id in SearchQuery.previous_ids:
                print('Detected a previously searched post, ID {}'.format(id))
                return

            SearchQuery.previous_ids.append(id)
            log_post_id(id)
            self.notification_backlog.put(get_formatted_results(title, id, price, time, link))
