"""
Contains a dict which stores keywords for different categories under
'for sale' and the equivalent phrase used in the url.
"""

categories_for_sale = {'all': 'sss',
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


# All possible search categories listed out in an array.
all_categories = ['all', 'antiques', 'appliances', 'arts+crafts', 'atvs/utvs/snow', 'auto parts', 'auto wheels & tires',
                  'aviation', 'baby+kids', 'barter', 'beauty+hlth', 'bike parts', 'bikes', 'boat parts', 'boats',
                  'books', 'business', 'cars+trucks', 'cds/dvd/vhs', 'cell phones', 'clothes+acc', 'collectibles',
                  'computer parts', 'computers', 'electronics', 'farm+garden', 'free stuff', 'furniture',
                  'garage sales', 'general', 'heavy equipment', 'household', 'jewelry', 'materials', 'motorcycle parts',
                  'motorcycles', 'music instr', 'photo+video', 'RVs', 'sporting', 'tickets', 'tools', 'toys+games',
                  'trailers', 'video gaming', 'wanted']


# Returns a search url given a search query and a category to search under.
def get_search_url(query, category='all'):
    try:
        category = categories_for_sale[category]
    except KeyError:
        category = categories_for_sale['all']
        print('Unknown category! Defaulting to all categories.')

    return 'https://vancouver.craigslist.org/search/{}?sort=new&query={}'.format(category, query)






"""
Code used to get the info for categories_for_sale. Leaving it here in case it ever needs to be used again.

generic_url = get_search_url("", "all")
html = requests.get(generic_url).content
soup = BeautifulSoup(html, 'html.parser')
results = soup.select('.result-info')
results = soup.find_all('select', {'id': 'subcatAbb'})

for result in soup.find_all('option'):
    print("'{}' : '{}',".format(result.get_text(), result.get('value')))

for result in soup.find_all('option'):
    print("'{}',".format(result.get_text()))
"""
