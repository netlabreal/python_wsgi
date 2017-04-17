#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import json
from sqldb import MineDb
from wsgiref.simple_server import make_server

error = """
<html>
<head>
    <title>ERROR</title>
    <link rel="stylesheet" href="css/q.css">
</head>
<body>
<div class="main">
<H1>ERROR! FILE NOT FOUND!</H1>
</div>
</body>
</html>
"""


def return_html_get(path):
    rez = error
    resource = ""
    rpath = sys.path[0]
    # print(rpath)
    # ------Определяем путь-------------------------
    if path == "/":
        resource = os.path.join(rpath, "static", "index.html")
    elif path == "/comment":
        resource = os.path.join(rpath, "static", "comment.html")
    elif path == "/view":
        resource = os.path.join(rpath, "static", "view.html")
    elif path == "/stat":
        resource = os.path.join(rpath, "static", "stat.html")
    else:
        # resource = os.path.join(rpath, "static", path)
        resource = rpath+"/static/"+path
    # ----------------------------------------------
    if resource != "":
        try:
            with open(resource, 'r') as file:
                 rez = file.read()
        except Exception as e:
            print(e)
    # ---Определяем html или css--------------------
    if resource.endswith('.css'):
        header = [('Content-type', 'text/css'), ('Content-Length', str(len(rez)))]
    else:
        header = [('Content-type', 'text/html'),('Content-Length', str(len(rez)))]
    # ----------------------------------------------
    return [rez, header]


def return_html_post(path, request):
    rpath = sys.path[0]
    out = "0"
    if path == "/all_data":
        md = MineDb(os.path.join(rpath, 'test.db'))
        out = md.returndata("SELECT comments.*, regions.name, towns.name FROM comments INNER JOIN regions ON comments.region=regions.id INNER JOIN towns ON comments.town=towns.id;")
    elif path == "/st_data_r":
        md = MineDb('test.db')
        out = md.returndata("SELECT comments.region, regions.name, COUNT(comments.id) FROM comments INNER JOIN regions ON comments.region=regions.id GROUP BY regions.name;")
    elif path == "/st_data_t":
        md = MineDb('test.db')
        out = md.returndata("SELECT towns.name, COUNT(comments.id) FROM comments INNER JOIN towns ON comments.town=towns.id where comments.region=%s  GROUP BY towns.name;" % request)
    elif path == "/r_data":
        md = MineDb('test.db')
        out = md.returndata("SELECT * FROM regions;")
    elif path == "/t_data":
        md = MineDb('test.db')
        out = md.returndata("SELECT * FROM towns where rid=%s;" % request)
    elif path == "/del_data":
        md = MineDb('test.db')
        ss = 'DELETE FROM comments where id=%s;' % request
        out = md.execute(ss)
    elif path == "/add_data":
        # -------Преобразуем json-----------------------
        res = json.loads(request)
        res['region'] = int(res['region'])
        res['town'] = int(res['town'])
        # --------Заменяем [ на { для sql --------------
        dict = res
        keys = str(dict.keys())
        keys = keys.replace('[', '(')
        keys = keys.replace(']', ')')
        keys = keys.replace("u'", '')
        keys = keys.replace("'", '')

        vals = str(dict.values())
        vals = vals.replace('[', '(')
        vals = vals.replace(']', ')')
        vals = vals.replace("u", '')
        # ----------------------------------------------
        md = MineDb('test.db')
        ss = 'INSERT INTO comments %s VALUES %s;' % (keys, vals)
        out = md.execute(ss)
    # -------Возврат--------------------------------
    rez = json.dumps(out)
    header = [('Content-type', 'application/json;')]
    return [rez, header]


def application(environ, start_response):
    status = '200 OK'
    # --------Получаем POST данные------------------
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)
    # ------Определяем возврат------------------
    if environ['REQUEST_METHOD'] == 'POST':
        output, response_headers = return_html_post(environ['PATH_INFO'], request_body)
    else:
        output, response_headers = return_html_get(environ['PATH_INFO'])
    # ----------------------------------------------
    start_response(status, response_headers)
    return [output]


class Application(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._rpath = sys.path[0]

    def return_html_get(self, path):
        rez = error
        resource = ""
        # ------Определяем путь-------------------------
        if path == "/":
            resource = os.path.join(rpath, "static", "index.html")
        elif path == "/comment":
            resource = os.path.join(rpath, "static", "comment.html")
        elif path == "/view":
            resource = os.path.join(rpath, "static", "view.html")
        elif path == "/stat":
            resource = os.path.join(rpath, "static", "stat.html")
        else:
            resource = self._rpath + "/static/" + path
        # ----------------------------------------------
        if resource != "":
            try:
                with open(resource, 'r') as file:
                    rez = file.read()
            except Exception as e:
                print(e)
        # ---Определяем html или css--------------------
        if resource.endswith('.css'):
            header = [('Content-type', 'text/css'), ('Content-Length', str(len(rez)))]
        else:
            header = [('Content-type', 'text/html'), ('Content-Length', str(len(rez)))]
        # ----------------------------------------------
        return [rez, header]

    def return_html_post(self, path, request):
        out = "0"
        if path == "/all_data":
            md = MineDb(os.path.join(self._rpath, 'test.db'))
            out = md.returndata(
                "SELECT comments.*, regions.name, towns.name FROM comments INNER JOIN regions ON comments.region=regions.id INNER JOIN towns ON comments.town=towns.id;")
        elif path == "/st_data_r":
            md = MineDb(os.path.join(self._rpath, 'test.db'))
            out = md.returndata(
                "SELECT comments.region, regions.name, COUNT(comments.id) FROM comments INNER JOIN regions ON comments.region=regions.id GROUP BY regions.name;")
        elif path == "/st_data_t":
            md = MineDb(os.path.join(self._rpath, 'test.db'))
            out = md.returndata(
                "SELECT towns.name, COUNT(comments.id) FROM comments INNER JOIN towns ON comments.town=towns.id where comments.region=%s  GROUP BY towns.name;" % request)
        elif path == "/r_data":
            md = MineDb(os.path.join(self._rpath, 'test.db'))
            out = md.returndata("SELECT * FROM regions;")
        elif path == "/t_data":
            md = MineDb(os.path.join(self._rpath, 'test.db'))
            out = md.returndata("SELECT * FROM towns where rid=%s;" % request)
        elif path == "/del_data":
            md = MineDb(os.path.join(self._rpath, 'test.db'))
            ss = 'DELETE FROM comments where id=%s;' % request
            out = md.execute(ss)
        elif path == "/add_data":
            # -------Преобразуем json-----------------------
            res = json.loads(request)
            res['region'] = int(res['region'])
            res['town'] = int(res['town'])
            # --------Заменяем [ на { для sql --------------
            dict = res
            keys = str(dict.keys())
            keys = keys.replace('[', '(')
            keys = keys.replace(']', ')')
            keys = keys.replace("u'", '')
            keys = keys.replace("'", '')

            vals = str(dict.values())
            vals = vals.replace('[', '(')
            vals = vals.replace(']', ')')
            vals = vals.replace("u", '')
            # ----------------------------------------------
            md = MineDb(os.path.join(self._rpath, 'test.db'))
            ss = 'INSERT INTO comments %s VALUES %s;' % (keys, vals)
            out = md.execute(ss)
        # -------Возврат--------------------------------
        rez = json.dumps(out)
        header = [('Content-type', 'application/json;')]
        return [rez, header]

    def __call__(self, environ, start_response):
        status = '200 OK'
        # --------Получаем POST данные------------------
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size)
        # ------Определяем возврат------------------
        if environ['REQUEST_METHOD'] == 'POST':
            output, response_headers = return_html_post(environ['PATH_INFO'], request_body)
        else:
            output, response_headers = return_html_get(environ['PATH_INFO'])
        # ----------------------------------------------
        start_response(status, response_headers)
        return [output]

    def run(self):
        """ server """
        httpd = make_server(self._host, self._port, self)
        print('Serving on {host}:{port}'.format(host=self._host, port=self._port))
        httpd.serve_forever()


if __name__ == "__main__":
    app = Application('192.168.2.222', 8080)
    app.run()
