class Torrent:
    def __init__(self, provider, name, size, link, seeds, leeches):
        self.provider = provider
        self.name = name
        self.size = int(size)
        self.link = link
        self.seeds = int(seeds)
        self.leeches = int(leeches)

        # self.tor = session.get(domain + link).content


class Torrents:
    torrents = []

    def __init__(self, *args):
        for e in args:
            if type(e) != Torrent:
                raise Exception('only torrent class')
            self.append(e)


    def append(self, x):
        if x in self.torrents:
            raise Exception('in')
        self.torrents.append(x)
