from flask import Flask, jsonify
from providers import rutracker, rutor
from torrent import Torrents

from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=8)

app = Flask(__name__)

tasks = {}
tasks_ai = 0

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/api/search/<query>')
def make_task(query):
    global tasks_ai
    tasks[tasks_ai] = pool.apply_async(search, [query])
    tasks_ai += 1
    return str(tasks_ai - 1)

@app.route('/api/task/<int:id>')
def status(id):
    if tasks[id].ready():
        return jsonify(tasks[id].get())
    else:
        return 'Not ready'


def search(query, *args, **kwards):
    print('started')
    found = []
    found += rutracker.search(query)
    found += rutor.search(query)

    tor = Torrents(found)

    return list(map(dict, tor))


if __name__ == '__main__':
    app.run()
