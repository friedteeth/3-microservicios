import sqlite3
import json

import flask

app = flask.Flask(__name__)

@app.route('/netflix/original-content/<int:id>', methods=['GET', 'PATCH'])
def get_and_patch(id):
    if flask.request.method == 'GET':
        return get(id)
    elif flask.request.method == 'PATCH':
        return patch(id)

def get(id):
    query = 'SELECT * FROM original_content WHERE id={id}'.format(id=id)
    sqlite_conn = get_database_connection('./mac/original_content.db')
    sqlite_cursor = sqlite_conn.cursor()
    sqlite_cursor.execute(query)
    data = sqlite_cursor.fetchall()

    if not data:
        return json.dumps(get_error_response('Movie does not exist'))

    result = convert_cursor_to_json(data)
    return json.dumps(result)

def patch(id):
    query = 'UPDATE original_content SET'
    json_data = flask.request.get_json()
    valid_keys = ['name', 'type', 'genre', 'imdb_rating']
    actual_valid_keys = []

    for key in json_data:
        if key in valid_keys:
            actual_valid_keys.append(key)
    
    if len(actual_valid_keys) > 0:
        for i,key in enumerate(actual_valid_keys):
            query += ' {field}'.format(field=key)
            if json_data[key] == 'NULL':
                query += '=NULL'
            else:
                query += '="{key_value}"'.format(key_value=json_data[key])
            if i < len(actual_valid_keys)-1:
                query += ','

    query += ' WHERE id={id}'.format(id=id)
    try:
        sqlite_conn = get_database_connection('./mac/original_content.db')
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.execute(query)
        sqlite_conn.commit()
    except:
        return json.dumps(get_error_response())

    return json.dumps(get_success_resonse())

def get_database_connection(database_path):
    conn = sqlite3.connect(database_path)
    return conn

def convert_cursor_to_json(cursor_data):
    result_list = []
    for e in cursor_data:
        temp_dict = {}
        temp_dict['id'] = e[0]
        temp_dict['name'] = e[1]
        temp_dict['type'] = e[2]
        temp_dict['genre'] = e[3]
        temp_dict['imdb_rating'] = e[4]
        result_list.append(temp_dict)
    return result_list

def get_success_resonse():
    json_dict = {}
    json_dict['success'] = 'Patch successful'
    return json_dict

def get_error_response(message):
    json_dict = {}
    json_dict['error'] = message
    return json_dict

if __name__ == '__main__':
    # Se ejecuta el servicio definiendo el host '0.0.0.0' 
    #  para que se pueda acceder desde cualquier IP
    app.run(host='0.0.0.0', port='8086', debug=True)