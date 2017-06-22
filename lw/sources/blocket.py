import urllib.parse
import urllib.request
import re

import bs4

from . import BaseSource, sources
from ..data.db import ListingItem


class BlocketSource(BaseSource):

    BASE_URL = 'https://www.blocket.se/hela_sverige?q={0}'

    def query(self, key):
        with urllib.request.urlopen(self.BASE_URL.format(urllib.parse.quote_plus(key))) as response:
            html = response.read()

        soup = bs4.BeautifulSoup(html, 'html.parser')
        items = soup.find_all('article', id=re.compile('^item_\d+'))
        for item in items:
            heading = item.find(attrs={'class': ['media-heading']})
            price = item.find(attrs={'class': ['list_price']})

            yield ListingItem._make([
                item['id'],
                heading.a['title'],
                '',
                heading.a['href'],
                price.string,
                'blocket'
            ])

sources.append(BlocketSource())
