import sqlite3
import json
import flask
from urllib.request import urlopen
import json
import requests
#Titulo
#Type
#imdbID
#
app = flask.Flask(__name__)

@app.route('/netflix/original-content', methods=['POST'])
def create():
    if flask.request.method == 'POST':
        return create()

def create():
    query = 'INSERT INTO original_content (name, type, genre, imdb_rating) VALUES('
    json_data = flask.request.get_json()
    values = data_content(json_data['name'])
    if not values:
        return json.dumps(get_error_response('Movie not found'))
    query += '"' + values["name"] + '",'
    query += '"' + values["type"] + '",'
    query += '"' + values["genre"] +  '",'
    query += '"' + values["imdb_rating"] + '")'

    try:
        sqlite_conn = get_database_connection('./mac/original_content.db')
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.execute(query)
        sqlite_conn.commit()
    except:
        return json.dumps(get_error_response('Invalid data'))

    return json.dumps(get_success_resonse())

def data_content(title):
    url = 'http://www.omdbapi.com/?apikey=7f5131b3&t={title}'.format(title=title.replace(' ', '+'))
    print(url)
    r = requests.get(url)
    data = r.json()
    print(str(data))
    values = {}
    if data['Response'] == 'True':
        values = {
            'name' : data['Title'],
            'type' : data['Type'],
            'genre' : data['Genre'],
            'imdb_rating' : data['imdbRating']
            }
    return values

def get_database_connection(database_path):
    conn = sqlite3.connect(database_path)
    return conn

def get_success_resonse():
    json_dict = {}
    json_dict['success'] = 'Movie added'
    return json_dict

def get_error_response(message):
    json_dict = {}
    json_dict['error'] = message
    return json_dict

if __name__ == '__main__':
    # Se ejecuta el servicio definiendo el host '0.0.0.0'
    #  para que se pueda acceder desde cualquier IP
    app.run(host='0.0.0.0', port='8087', debug=True)
