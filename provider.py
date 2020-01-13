import requests
from bs4 import BeautifulSoup
from torrent import Torrent, Torrents


class LoginException(Exception):
    pass


class Provider:
    session = requests.Session()

    def __init__(self, domain, search, auth=None):
        self.domain = domain
        self.search_params = search
        if auth is not None:
            self.auth(req=auth['request'], login=auth['login'], password=auth['password'])

    def auth(self, req, login, password):
        if 'params' in req and req['params']:
            params = req['params'].copy()
        else:
            params = {}
        params[req['login_field']] = login
        params[req['password_field']] = password

        response = self.session.post(self.domain + req['url'], params)
        response = BeautifulSoup(response.text, "html.parser")

        if response.select_one('#logged-in-username') is None:
            raise LoginException(response.select_one('.warnColor1.tCenter.mrg_16').text)

    def search(self, query):
        request = self.search_params['request']
        response = self.session.get(self.domain + request['url_template'].format(query))
        response = BeautifulSoup(response.text, "html.parser")

        rows = response.select(self.search_params['rows'])

        pages_params = self.search_params['pages']
        pages = list(map(lambda x: x['href'], response.select(pages_params['selector'])[pages_params['start']:pages_params['end']]))
        for pg in pages:
            response = self.session.get(self.domain + pg)
            response = BeautifulSoup(response.text, "html.parser")
            rows += response.select(self.search_params['rows'])

        torrents = []
        for row in rows:
            try:
                name = row.select_one(self.search_params['name']).text
                if self.search_params['size']['attribute'] is not None:
                    size = row.select(self.search_params['size']['selector'])[self.search_params['size']['num']][self.search_params['size']['attribute']]
                else:
                    size = row.select(self.search_params['size']['selector'])[self.search_params['size']['num']].text
                link = row.select_one(self.search_params['link'])['href']
                if self.search_params['magnet'] is not None:
                    magnet = row.select_one(self.search_params['magnet'])['href']
                else:
                    magnet = None
                seeds = row.select_one(self.search_params['seeds']).text
                leeches = row.select_one(self.search_params['leeches']).text

                if int(seeds) > 0:
                    torrents.append(Torrent(self, name, size, link, magnet, seeds, leeches))
            except AttributeError:
                pass

        return torrents
