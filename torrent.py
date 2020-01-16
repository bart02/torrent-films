class Torrent:
    content = None
    _hash = None

    def __init__(self, provider, name, size, link, magnet, seeds, leeches):
        self.provider = provider
        self.name = name

        size = size.lower()
        self.size = float((size.replace('gb', '').replace('mb', '').replace('kb', '')))
        if 'kb' in size:
            self.size *= 1024
        elif 'mb' in size:
            self.size *= 1048576
        elif 'gb' in size:
            self.size *= 1073741824
        self.size = int(self.size)

        self._link = link
        self.magnet = magnet
        self.seeds = int(seeds)
        self.leeches = int(leeches)

        # self.tor = session.get(domain + link).content

    @property
    def link(self):
        if self._link.startswith('http'):
            return self._link
        else:
            return self.provider.domain + self._link

    def download_torrent(self):
        if self.content is None:
            self.content = self.provider.session.get(self.link).content

        return self.content

    def get_hash_from_torrent(self):
        from magneturi import bencode
        import hashlib

        self.download_torrent()

        decodedDict = bencode.bdecode(self.content)
        info_hash = hashlib.sha1(bencode.bencode(decodedDict["info"])).hexdigest()
        return info_hash

    def get_hash_from_magnet(self):
        return self.magnet.split('btih:')[1][:40]

    @property
    def hash(self):
        if self._hash is None:
            if self.magnet:
                self._hash = self.get_hash_from_magnet()
            else:
                self._hash = self.get_hash_from_torrent()

        return self._hash

    def __iter__(self):
        yield ('name', self.name)
        yield ('size', self.size)
        yield ('link', self.link)
        yield ('seeds', self.seeds)
        yield ('leeches', self.leeches)

    def __str__(self):
        return str(dict(self))


class Torrents(list):
    def __init__(self, seq):
        super().__init__()
        self.extend(seq)

    def extend(self, x):
        for e in x:
            self.append(e)

    def append(self, t):
        if type(t) != Torrent:
            raise Exception('not torrent object')

        if self.__contains__(t):
            raise Exception('already here')

        exists = False
        for e in self.__iter__():
            if abs(t.size - e.size) < 10485760:
                if e.hash == t.hash:
                    print('similar', e.link, t.link)
                    exists = True
                    break

        if not exists:
            super().append(t)
