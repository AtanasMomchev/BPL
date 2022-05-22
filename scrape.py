import requests
import logging
from Stores import Stores
from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession, HTMLSession
from threading import Thread, Lock


class Scrape:
    """
    This class will be used to query different sites and scrape product title price and url.
    """
    log = logging.getLogger(__name__)

    def __init__(self, product_name: str, product_model: str, categories):
        """
        :param product_name: Name of product to query should be string.
        :param product_model: Model of product to query should be string. Can be empty string.
        :param categories: List of categories from which to query.
        """
        self.product_name = product_name
        self.product_model = product_model
        if product_model:
            self.product = f'{product_name} {product_model}'
        else:
            self.product = product_name
        # replace all spaces with + sign for query purpose
        self.product_query = self.product.replace(' ', '+')
        self.categories = categories
        self._sectors = ('electronics', 'general', 'board games')
        self.thread_results = []
        self.htmls = {}
        # always append general section since it can contain anything
        if not self.categories:
            self.categories = self._sectors
        else:
            self.categories.append("general")

    store = Stores()
    _products = []

    def get_html(self, data, key):
        self.htmls[key] = requests.get(data + self.product_query)

    # def get_html_js(self, data, key):
    #     session = HTMLSession()
    #     res = session.get(data + self.product_query)
    #     self.htmls[key] = res

    def scrape_standard(self, data, res_html, key):
        soup = BeautifulSoup(res_html[key].text, 'html.parser')
        product_title = soup.select(f'{data["title"]}')
        product_price = soup.select(f'{data["price"]}')
        product_url = soup.select(f'{data["url"]}')
        self.thread_results.append([product_title, product_price, product_url, key])

    def scrape_javascript(self, data, res_html, key):
        session = HTMLSession()
        res = session.get(data['query_url'] + self.product_query)
        res.html.render()
        soup = BeautifulSoup(res.html.html, 'html.parser')
        product_title = soup.select(f'{data["title"]}')
        product_price = soup.select(f'{data["price"]}')
        product_url = soup.select(f'{data["url"]}')
        self.thread_results.append([product_title, product_price, product_url, key])

    def get_product_data(self, product_title, product_price, product_url):
        """
        Query site for a product. Take title, price and url.
        Iterate over products from query and if title and module are contained in the query result
        add them to a list as a map. The iteration goes only trough first 5 items.
        The data is parsed with python html.parser and uses beautiful soup to get different tags or classes.
        :param data: A map of site items that are used for Beautiful soup to do css query. Data must contain:
        1. query url to which the product is appended
        2. a html tag or class by witch the title of the product will be searched
        3. a html tag or class by witch the price of the product will be searched
        4. a html tag or class in which the a.href is contained
        :return: List of Maps.
        """

        product_data = []

        for idx, title in enumerate(product_title):
            if idx > 5:
                break
            if self.product_model.lower() in product_title[idx].getText().lower() and \
                    self.product_name.lower() in product_title[idx].getText().lower():
                try:
                    prod = {'title': product_title[idx].getText(),
                            'price': product_price[idx].getText(),
                            'url': product_url[idx].a.get('href', None)}
                    product_data.append(prod)
                except (IndexError, ValueError):
                    pass
        return product_data

    @staticmethod
    def _fix_product(store, products):
        """
        This method is to fix some of the collected data from get_product_data method.
        :param store: the store from which the data was collected
        :param products: the product data that is going to be fixed
        :return: None
        """
        for prod in products:
            if store == 'ardes':
                prod['price'] = prod['price'][:-4]
                prod['url'] = 'https://ardes.bg' + prod['url']
            elif store == 'technopolis':
                prod['url'] = 'https://technopolis.bg' + prod['url']
            elif store == 'emag':
                prod['title'] = prod['title'].strip()
                prod['price'] = prod['price'][:-6]
            elif store == 'plesio':
                prod['url'] = 'https://plesio.bg' + prod['url']
            elif store == 'big bag':
                prod['url'] = 'https://bigbag.bg' + prod['url']
            elif store == 'table games':
                prod['url'] = 'https://tablegames.bg' + prod['url']

    def generate_products_info(self):
        """
        This method iterates over categories and stores in the categories.
        Calls method to query data per category per store.
        Calls method to fix data.
        :return: List that contains lists of maps with product data.
        """
        products = []
        threads = []

        for category in self.categories:
            if category.lower() in self._sectors:
                for key, value in self.store.get_store(category).items():
                    if not value['javascript']:
                        thread = Thread(target=self.get_html, args=(value['query_url'], key))
                        threads.append(thread)
                        thread.start()
                    # else:
                    #     self.get_html_js(value['query_url'], key)

                for i in threads:
                    i.join()

                for key, value in self.store.get_store(category).items():
                    if not value['javascript']:
                        self.scrape_standard(value, self.htmls, key)
                    else:
                        self.scrape_javascript(value, self.htmls, key)
                for i in self.thread_results:
                    products_title, product_price, product_url, key = i
                    self.log.info(f'Adding products for store: {key}')
                    prod = self.get_product_data(products_title, product_price, product_url)
                    self._fix_product(key, prod)
                    products.append(prod)
            else:
                self.log.warning(f"No such category {category}")
            self.thread_results.clear()
        return products


s = Scrape('tp-link', 'archer ax10', ['electronics'])
for item in s.generate_products_info():
    print(item)
