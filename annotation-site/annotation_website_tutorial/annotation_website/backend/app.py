import csv
import json
import logging
import pickle
from datetime import date

import pymysql
from flask import Flask, request, jsonify, \
    send_from_directory
from flask_cors import CORS
from pymysql import cursors

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='myapp.log',
    filemode='w')

app = Flask(__name__)
CORS(app)


def load_from_file(filename):
    with open(filename, 'rb') as f:
        url_list_divided = pickle.load(f)
    return url_list_divided


def load_from_json_file(filename):
    with open(filename, 'r') as f:
        url_list_json = json.load(f)
    return url_list_json


# these 2 objects are image-caption data to be annotated, saved by pickle.dump
# Format:
# [
#   [(caption_1, url_1, source_1), (caption_2, url_2, source_2), ...] # annotator 1
#   [(caption_1, url_1, source_1), (caption_2, url_2, source_2), ...] # annotator 2
#   ...
# ]
#{'id':[(caption, url, source),(caption, url, source), ...]}
url_list = load_from_file('url_list.pkl')
test_url_list = load_from_file('url_list_divided.pkl')


@app.route('/', methods=('GET', 'POST',))
def hello_world():
    return 'Hello World!'


@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    id_annotator = request.args.get('id_annotator')
    passwd_annotator = request.args.get('passwd_annotator')
    req_json = request.get_json()
    app.logger.info(req_json)
    if req_json:
        id_annotator = req_json['id_annotator']
        passwd_annotator = req_json['passwd_annotator']
    app.logger.info('{} {} is trying to log in'.format(id_annotator, passwd_annotator))

    if id_annotator and passwd_annotator:

        db = pymysql.connect('localhost', 'merterm', '1234567890', 'google_annotation')

        cursor = db.cursor(cursors.DictCursor)
        sql = "SELECT * FROM `annotator` WHERE id_annotator='" + id_annotator + "'"
        # sql = "SELECT `id_annotator`, `passwd_annotator` FROM `annotator` WHERE id_annotator='" + id_annotator + "'"
        app.logger.debug('Database query: %s', sql)
        cursor.execute(sql)
        data = cursor.fetchone()
        app.logger.debug('Database query result: {}'.format(data))
        db.close()

        # logged in
        if data and data['passwd_annotator'] == passwd_annotator:
            return jsonify({'code': 200, 'msg': 'logged in', 'token': id_annotator})

    return jsonify({'code': 400, 'msg': 'error'})


@app.route('/index', methods=['POST', 'OPTIONS'])
def index():
    token = request.headers.get('token')
    if not token:
        app.logger.debug('{} is trying to get batches.'.format(token))
        return jsonify({'code': 400, 'msg': 'error'})
    app.logger.debug('{} is trying to get batches.'.format(token))
    batches = []

    batches = []
    if token.isdigit():
        id_annotator = int(token)
        batches = url_list[id_annotator - 1]
    elif token == 'test':
        batches = test_url_list[0]
    else:
        return jsonify({'code': 400, 'msg': 'id error'})

    ret = list(range(1, len(batches) + 1))
    return jsonify({'code': 200, 'id_batches': ret})


@app.route('/getone', methods=['POST', 'OPTIONS'])
def get_one():
    token = request.headers.get('token')
    id_batch = request.headers.get('id_batch')
    id_image = request.headers.get('id_image')
    if not token or id_batch is None or id_image is None:
        app.logger.debug('{} {} {} is trying to get one.'.format(token, id_image, id_batch))
        app.logger.debug(request.headers)
        return jsonify({'code': 400, 'msg': 'error'})
    id_batch = int(id_batch) - 1
    id_image = int(id_image) - 1
    app.logger.debug('{} is trying to get image {} in batch {}.'.format(token, id_image, id_batch))
    batches = []

    batches = []
    if token.isdigit():
        id_annotator = int(token)
        batches = url_list[id_annotator - 1]
    elif token == 'test':
        batches = test_url_list[0]
    else:
        return jsonify({'code': 400, 'msg': 'id error'})

    if id_batch >= len(batches) or id_batch < 0:
        return jsonify({'code': 400, 'msg': 'bad id_batch'})
    if id_image >= len(batches[id_batch]) or id_image < 0:
        return jsonify({'code': 400, 'msg': 'bad id_image'})
    app.logger.debug('size sanity check: {} {} {}'.format(id_image, id_batch, len(batches[id_batch])))
    ret = batches[id_batch][id_image]
    app.logger.debug('returning {}'.format(ret))
    source = 'test' if token == 'test' else ret[2]
    return jsonify({'code': 200, 'caption': ret[0], 'url': ret[1], 'source': source})


@app.route('/export', methods=['POST', 'OPTIONS'])
def export():
    token = request.headers.get('token')
    if not token or token != 'admin':
        app.logger.info('{} is trying to export.'.format(token))
        app.logger.debug(request.headers)
        return jsonify({'code': 400, 'msg': 'error'})

    db = pymysql.connect('localhost', 'merterm', '1234567890', 'google_annotation')

    cursor = db.cursor()
    sql = "SELECT * FROM `annotation`"
    app.logger.debug('Database query: %s', sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    # app.logger.debug('Database query result: {}'.format(data))

    date_today = date.today().strftime('%m%d')

    with open('output_{}.tsv'.format(date_today), 'w') as fp:
        writer = csv.writer(fp, delimiter='\t', lineterminator='\n')
        col_names = [col[0] for col in cursor.description]
        writer.writerow(col_names)
        writer.writerows(data)
    db.close()

    return jsonify({'code': 200, 'msg': 'success'})


@app.route('/download')
def download():
    token = request.headers.get('token')
    app.logger.info('{} is trying to download.'.format(token))
    if not token or token != 'admin':
        app.logger.debug(request.headers)
        return jsonify({'code': 400, 'msg': 'error'})
    date_today = date.today().strftime('%m%d')

    return send_from_directory('.', 'output_{}.tsv'.format(date_today), as_attachment=True)


@app.route('/rmdb')
def rmdb():
    token = request.headers.get('token')
    app.logger.info('{} is trying to download.'.format(token))
    if not token or token != 'admin':
        app.logger.debug(request.headers)
        return jsonify({'code': 400, 'msg': 'error'})

    db = pymysql.connect('localhost', 'merterm', '1234567890', 'google_annotation')

    cursor = db.cursor()
    sql = "delete FROM `annotation`"
    app.logger.debug('Database deletion: %s', sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    app.logger.debug('Database deletion result: {}'.format(data))
    db.commit()
    db.close()
    return jsonify({'code': 200, 'msg': 'error'})


@app.route('/annotate', methods=['POST', 'OPTIONS'])
def annotate():
    app.logger.debug(request.headers)
    token = request.headers.get('token')
    id_batch = request.headers.get('id_batch')
    id_image = request.headers.get('id_image')
    url = request.headers.get('url')
    caption = request.headers.get('caption')
    jsdata = request.get_json()
    if not token or id_batch is None or id_image is None or not url or not caption or not jsdata:
        app.logger.debug('{} {} {} {} {} is trying to annotate.'.format(token, id_image, id_batch, url, caption))
        app.logger.debug(jsdata)
        return jsonify({'code': 400, 'msg': 'error'})
    app.logger.info('{} {} {} {} {} is trying to annotate.'.format(token, id_image, id_batch, url, caption))
    app.logger.debug(jsdata)
    id_batch = int(id_batch) - 1
    id_image = int(id_image) - 1

    batches = []
    if token.isdigit():
        id_annotator = int(token)
        batches = url_list[id_annotator - 1]
    elif token == 'test':
        batches = test_url_list[0]
    else:
        return jsonify({'code': 400, 'msg': 'id error'})

    if id_batch >= len(batches) or id_batch < 0:
        return jsonify({'code': 400, 'msg': 'bad id_batch'})
    if id_image >= len(batches[id_batch]) or id_image < 0:
        return jsonify({'code': 400, 'msg': 'bad id_image'})

    db = pymysql.connect('localhost', 'merterm', '1234567890', 'google_annotation')

    cursor = db.cursor(cursors.DictCursor)
    caption = caption.replace("'", "''")
    url = url.replace("'", "''")

    other = jsdata['other']
    other = other.replace("'", "''")
    other = other.replace("\r", "|")
    other = other.replace("\n", "|")

    values = "NULL, \'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\'".format(
        token, caption,
        url,
        jsdata['cb0'],
        jsdata['cb1'],
        jsdata['cb2'],
        jsdata['cb3'],
        jsdata['cb4'],
        jsdata['cb5'],
        jsdata['cb6'],
        other,
        jsdata['cbWhen'],
        jsdata['cbHow'],
        jsdata['cbWhere'],
        jsdata['Identification'],
        jsdata['source'],
        jsdata['cbBrokenImg'],
        jsdata['cbMetaGood'],
        jsdata['cbMetaBad'],
        jsdata['cbVisible1'],
        jsdata['cbVisible2'],
        jsdata['cbVisible3'],
        jsdata['cbVisible4'],
        jsdata['cbVisible5'],
        jsdata['cbSubjectiveGood'],
        jsdata['cbSubjectiveBad'],
        jsdata['cbStory1'],
        jsdata['cbStory2'],
        jsdata['cbStory3'],
        jsdata['cbStory4'],
        jsdata['cbStory5'],
    )
    sql = "INSERT INTO annotation () VALUES ({})".format(values)
    app.logger.debug('Database insertion: %s', sql)
    cursor.execute(sql)
    db.commit()
    db.close()

    id_image += 1
    if id_image >= len(batches[id_batch]):
        return jsonify({'code': 200, 'id_image': -1})
    else:
        return jsonify({'code': 200, 'id_image': id_image + 1})


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


if __name__ == '__main__':
    app.run(debug=True)
