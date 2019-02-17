import re

URL = 'https://www.imdb.com/search/title?title='

HEADERS = {'Accept-Language': 'en-US, en;q=0.5'}

YEAR_REGEX = re.compile(r'[1|2][9|0]\d\d')
