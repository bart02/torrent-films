import requests
from bs4 import BeautifulSoup
from torrent import Torrent

session = requests.Session()

domain = 'https://rutracker.org/forum/'

resp = session.post(domain + 'login.php',
                    {'login_username': 'LOGIN', 'login_password': 'PASSWORD', 'login': 'Login'})

# print(resp.status_code)
# with open('a.html', 'w') as f:
#     f.write(resp.text)

soup = BeautifulSoup(resp.text, "html.parser")
if soup.select_one('#logged-in-username') is not None:
    print(soup.select_one('#logged-in-username').text)
    authored = True
else:
    print(soup.select_one('.warnColor1.tCenter.mrg_16').text)
    authored = False

if not authored:
    raise Exception

resp = session.get(domain + 'tracker.php?nm={}&prev_new=0&prev_oop=1&f[]=-1&o=10&s=2&oop=1&pn='.format('Поймай меня если сможешь 2002'))
soup = BeautifulSoup(resp.text, "html.parser")
pgs = list(map(lambda x: x['href'], soup.select('.bottom_info .pg')[:-1]))
torrents = soup.select('#tor-tbl > tbody > tr')
for pg in pgs:
    pgresp = session.get(domain + pg)
    pgsoup = BeautifulSoup(pgresp.text, "html.parser")
    torrents += pgsoup.select('#tor-tbl > tbody > tr')

print(len(torrents))
torrents_obj = []
for e in torrents:
    try:
        name = e.select_one('td.t-title a').text
        size = e.select_one('td.tor-size a').text[:-2]
        link = e.select_one('td.tor-size a')['href']
        seeds = e.select_one('.seedmed').text
        leeches = e.select_one('.leechmed').text

        torrents_obj.append(Torrent(session, name, size, link, seeds, leeches))
    except AttributeError:
        pass

print(type(torrents_obj[0]))
