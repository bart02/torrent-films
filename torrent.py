domain = 'https://rutracker.org/forum/'

class Torrent:
    def __init__(self, session, name, size, link, seeds, leeches):
        self.session = session
        self.name = name
        self.size = int(size)
        self.link = link
        self.seeds = int(seeds)
        self.leeches = int(leeches)

        # self.tor = session.get(domain + link).content
