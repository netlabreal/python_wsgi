#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import json
import sqlite3
from wsgiref.simple_server import make_server


# Класс доступа к БД
class MineDb(object):

    def __init__(self, db_name):
        self.db_name = db_name
        rez = ""
        # Путь к скрипту инициализации БД
        sql_script = os.path.join(os.path.dirname(db_name), 'db.sql')
        # Если скрипт существует и БД нет, то создать БД и инициализировать ее
        if os.path.exists(sql_script) & os.path.exists(self.db_name) is False:
            try:
                with open(sql_script, 'r') as file:
                    # Считываем скрипт в переменную
                    rez = file.read()
            except Exception as e:
                print(e)
        if rez != "":
            try:
                # Подключение к БД
                con = sqlite3.connect(self.db_name)
                cur = con.cursor()
                # выполнение скрипта
                cur.executescript(rez)
                con.commit()
                print("Инициализация БД!")
            except sqlite3.Error as e:
                print(e)
            finally:
                # Закрытие соединения с БД
                if con:
                    con.close()

    # Возвращение данных из БД по произвольному sql
    def returndata(self, sql):
        rez = None
        try:
            # Подключение к БД
            con = sqlite3.connect(self.db_name)
            cursor = con.cursor()
            # выполнение sql
            cursor.execute(sql)
            rez = cursor.fetchall()
        except sqlite3.Error as e:
            print(e)
        finally:
            # Закрытие соединения с БД
            if con:
                con.close()
        return rez

    # Выполнить sql
    def execute(self, sql):
        rez = 0
        try:
            # Подключение к БД
            con = sqlite3.connect(self.db_name)
            cursor = con.cursor()
            # выполнение sql
            if cursor.execute(sql):
                rez = 1
                con.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            # Закрытие соединения с БД
            if con:
                con.close()
        return rez


class Application(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._rpath = sys.path[0]
        self._error = """
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

    def return_html_get(self, path):
        rez = self._error
        resource = ""
        # ------Определяем путь-------------------------
        if path == "/":
            resource = os.path.join(self._rpath, "static", "index.html")
        elif path == "/comment":
            resource = os.path.join(self._rpath, "static", "comment.html")
        elif path == "/view":
            resource = os.path.join(self._rpath, "static", "view.html")
        elif path == "/stat":
            resource = os.path.join(self._rpath, "static", "stat.html")
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
            # Возвращаем все комментарии соединенные с т. регионы и т. города
            out = md.returndata(
                "SELECT comments.*, regions.name, towns.name FROM comments INNER JOIN regions ON comments.region=regions.id INNER JOIN towns ON comments.town=towns.id;")
        elif path == "/st_data_r":
            md = MineDb(os.path.join(self._rpath, 'test.db'))
            # Возвращаем кол-во комментариев в разрезе регионов
            out = md.returndata(
                "SELECT comments.region, regions.name, COUNT(comments.id) FROM comments INNER JOIN regions ON comments.region=regions.id GROUP BY regions.name;")
        elif path == "/st_data_t":
            md = MineDb(os.path.join(self._rpath, 'test.db'))
            # Возвращаем кол-во комментариев по определенному региону в разрезе города
            out = md.returndata(
                "SELECT towns.name, COUNT(comments.id) FROM comments INNER JOIN towns ON comments.town=towns.id where comments.region=%s  GROUP BY towns.name;" % request)
        elif path == "/r_data":
            md = MineDb(os.path.join(self._rpath, 'test.db'))
            # Возвращаем все регионы
            out = md.returndata("SELECT * FROM regions;")
        elif path == "/t_data":
            md = MineDb(os.path.join(self._rpath, 'test.db'))
            # Возвращаем все города по определенному региону
            out = md.returndata("SELECT * FROM towns where rid=%s;" % request)
        elif path == "/del_data":
            md = MineDb(os.path.join(self._rpath, 'test.db'))
            # Удаляем комментарий
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
            # Добавляем комментарий
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
            output, response_headers = self.return_html_post(environ['PATH_INFO'], request_body)
        else:
            output, response_headers = self.return_html_get(environ['PATH_INFO'])
        # ----------------------------------------------
        start_response(status, response_headers)
        return [output]

    def run(self):
        """ создание тестового сервера и запуск приложения на нем """
        httpd = make_server(self._host, self._port, self)
        print('Serving on {host}:{port}'.format(host=self._host, port=self._port))
        httpd.serve_forever()


if __name__ == "__main__":
    app = Application('192.168.2.222', 8080)
    app.run()
