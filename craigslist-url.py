from bs4 import BeautifulSoup
from scrape import open_html

"""
Contains a dict which stores keywords for different categories under 'for sale' and the equivalent word used in the url
"""

for_sale_keywords = {'all': 'sss',
                     'antiques': 'ata',
                     'appliances': 'ppa',
                     'arts+crafts': 'ara',
                     'atvs/utvs/snow': 'sna',
                     'auto parts': 'pta',
                     'auto wheels & tires': 'wta',
                     'aviation': 'ava',
                     'baby+kids': 'baa',
                     'barter': 'bar',
                     'beauty+hlth': 'haa',
                     'bike parts': 'bip',
                     'bikes': 'bia',
                     'boat parts': 'bpa',
                     'boats': 'boo',
                     'books': 'bka',
                     'business': 'bfa',
                     'cars+trucks': 'cta',
                     'cds/dvd/vhs': 'ema',
                     'cell phones': 'moa',
                     'clothes+acc': 'cla',
                     'collectibles': 'cba',
                     'computer parts': 'syp',
                     'computers': 'sya',
                     'electronics': 'ela',
                     'farm+garden': 'gra',
                     'free stuff': 'zip',
                     'furniture': 'fua',
                     'garage sales': 'gms',
                     'general': 'foa',
                     'heavy equipment': 'hva',
                     'household': 'hsa',
                     'jewelry': 'jwa',
                     'materials': 'maa',
                     'motorcycle parts': 'mpa',
                     'motorcycles': 'mca',
                     'music instr': 'msa',
                     'photo+video': 'pha',
                     'RVs': 'rva',
                     'sporting': 'sga',
                     'tickets': 'tia',
                     'tools': 'tla',
                     'toys+games': 'taa',
                     'trailers': 'tra',
                     'video gaming': 'vga',
                     'wanted': 'waa'}


"""
Code used to get the above info. Leaving it here in case it ever needs to be used again.

soup = BeautifulSoup(open_html('craigslist_com'), 'html.parser')
results = soup.find_all('select', {'id': 'subcatAbb'})

for result in soup.find_all('option'):
    print("'{}' : '{}',".format(result.get_text(), result.get('value')))
"""
