class Stores:
    _elctronics = {'ardes': {'query_url': 'https://ardes.bg/products?q=', 'title': '.isTruncated',
                             'price': '.price-num', 'url': '.product-head', 'javascript': False},
                   'jarcomputers': {'query_url': 'https://www.jarcomputers.com/search?q=', 'title': '.s2 p',
                                    'price': '.s3 td.price', 'url': '.s2', 'javascript': False},
                   'technopolis': {'query_url': 'https://www.technopolis.bg/en/search/?query=',
                                   'title': '.item-name a',
                                   'price': '.price-value', 'url': '.preview', 'javascript': False},
                   'laptopbg': {'query_url': 'https://laptop.bg/search?utf8=%E2%9C%93&q=', 'title': 'article h2',
                                'price': '.price', 'url': 'article', 'javascript': False},
                   'plesio': {'query_url': 'https://plesio.bg/search.html?keyword=', 'title': '.productTitle h2',
                              'price': '.productPrice', 'url': '.productImage', 'javascript': False}
                   }

    _general = {'emag': {'query_url': 'https://www.emag.bg/search/', 'title': '.card-section-mid a',
                         'price': '.product-new-price', 'url': '.card-section-mid h2', 'javascript': False},
                'ozone': {'query_url': 'https://www.ozone.bg/instantsearchplus/result/?q=BANG!',
                          'title': '.isp_product_title', 'price': '.isp_product_price .price-main',
                          'url': '.isp_product_info', 'javascript': True}
                }

    _board_games = {'boardgames-bg': {'query_url': 'https://boardgames-bg.com/?dispatch=products.search&subcats=Y&'
                                                   'pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y'
                                                   '&search_performed=Y&search_id=&q=',
                                      'title': '.product-title', 'price': '.ty-price', 'url': '.ty-grid-list__image',
                                      'javascript': False},
                    'big bag': {'query_url': 'https://bigbag.bg/search.html?phrase=',
                                'title': '.c-product-grid__product-title-link', 'price': '.price-value',
                                'url': '.c-product-grid__product-title', 'javascript': False},
                    'time2play': {'query_url': 'https://www.time2play.bg/search?query=', 'title': '.product-title a',
                                  'price': '.product-price', 'url': '.product-title', 'javascript': False},
                    'table games': {'query_url': 'https://tablegames.bg/search.html?phrase=',
                                    'title': '.product-title.ellipsis a', 'price': '.price-withtax',
                                    'url': '.product-image-bg', 'javascript': False}
                    }

    _furniture = {'': {'query_url': ''},
                  'title': '', 'price': '', 'url': '', 'javascript': ''}

    def get_store(self, store):
        if store == 'electronics':
            return self._elctronics
        elif store == 'general':
            return self._general
        elif store == 'board games':
            return self._board_games
        return None
