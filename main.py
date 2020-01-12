from provider import Provider

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
                         'size': 'td.tor-size',
                         'link': 'td.tor-size a',
                         'seeds': '.seedmed',
                         'leeches': '.leechmed'
                     })

found = rutracker.search('поймай меня если сможешь 2002')
