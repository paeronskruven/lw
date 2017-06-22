import urllib.parse
import urllib.request

import bs4

from . import BaseSource, sources
from ..data.db import ListingItem


class TraderaSource(BaseSource):

    BASE_URL = 'http://www.tradera.com/search?sortBy=AddedOn&q={}'

    def query(self, key):
        with urllib.request.urlopen(self.BASE_URL.format(urllib.parse.quote_plus(key))) as response:
            html = response.read()

        soup = bs4.BeautifulSoup(html, 'html.parser')
        items = soup.find_all('li', attrs={'data-item-id': True})
        for item in items:
            heading = item.find(attrs={'class': ['item-card-details-header']})
            price = item.find(attrs={'class': ['item-card-details-price-amount']})

            yield ListingItem._make([
                item['data-item-id'],
                heading['title'],
                '',
                'http://www.tradera.com' + heading.a['href'],
                price.string,
                'tradera'
            ])

sources.append(TraderaSource())
