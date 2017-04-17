#!/usr/bin/env python
#!coding: utf8
import sqlite3
import os


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
