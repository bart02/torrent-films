from provider import Provider
from torrent import Torrents

rutracker = Provider(domain='https://rutracker.org/forum/',
                     auth={
                         'request': {'url': 'login.php',
                                     'login_field': 'login_username',
                                     'password_field': 'login_password',
                                     'params': {'login': 'Login'}},
                         'login': 'LOGIN',
                         'password': 'PASSWORD'
                     },
                     search={
                         'request': {'url_template': 'tracker.php?nm={}&prev_new=0&prev_oop=1&f[]=-1&o=10&s=2&oop=1&pn='},
                         'pages': {'selector': '.bottom_info .pg',
                                   'start': 0,
                                   'end': -1},
                         'rows': '#tor-tbl > tbody > tr',
                         'name': 'td.t-title a',
                         'size': {'selector': 'td.tor-size',
                                  'attribute': 'data-ts_text',
                                  'num': 0},
                         'link': 'td.tor-size a',
                         'magnet': None,
                         'seeds': '.seedmed',
                         'leeches': '.leechmed'
                     })

rutor = Provider(domain='http://rutor.info/',
                 search={
                     'request': {'url_template': 'search/0/0/300/2/{}'},
                     'pages': {'selector': '.bottom_info .pg',
                               'start': 0,
                               'end': -1},
                     'rows': '#index .gai, #index .tum',
                     'name': 'a[href*=torrent]',
                     'size': {'selector': 'td[align=right]',
                              'attribute': None,
                              'num': -1},
                     'link': 'a.downgif',
                     'magnet': 'a[href*=magnet]',
                     'seeds': '.green',
                     'leeches': '.red'
                 })

query = 'тайны следствия'

found = []
found += rutracker.search(query)
found += rutor.search(query)

tor = Torrents(found)

print()