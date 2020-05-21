import sqlite3
import json

import flask
import re
import requests

app = flask.Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PATCH'])
def api_gateway(path):
    if flask.request.method == 'PATCH' and re.match('^netflix[/]original-content[/][0-9]+$', path):
        return requests.patch('http://127.0.0.1:8086/' + path, json=flask.request.get_json()).content
    elif flask.request.method == 'POST' and re.match('^netflix[/]original-content$', path):
        return requests.post('http://127.0.0.1:8087/' + path, data=flask.request.data).content
    elif flask.request.method == 'GET' and re.match('^netflix[/]original-content[/][0-9]+$', path):
        return requests.get('http://127.0.0.1:8086/' + path).content
    elif flask.request.method == 'GET' and len(flask.request.args) > 0:
        return requests.get('http://127.0.0.1:8085/' + path, params=flask.request.args).content
    elif flask.request.method == 'GET' and re.match('^netflix[/]original-content$', path):
        return requests.get('http://127.0.0.1:8085/' + path).content

    return 'You want path: %s' % path

if __name__ == '__main__':
    # Se ejecuta el servicio definiendo el host '0.0.0.0' 
    #  para que se pueda acceder desde cualquier IP
    app.run(host='0.0.0.0', port='8084', debug=True)