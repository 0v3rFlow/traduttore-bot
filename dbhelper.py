#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3


class DBHelper:
    def __init__(self, dbname="dbchat"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    # Metodo per creare la tabella all'interno del db
    def create_table(self):
        # Statemant
        stmt = "CREATE TABLE IF NOT EXISTS user(id integer PRIMARY KEY, lingua_src text, lingua_dest text)"
        self.conn.execute(stmt)
        self.conn.commit()

    # Inserisco un nuovo record
    def add_item(self, chat_id, lingua_src, lingua_dest):
        stmt = "INSERT INTO user(id, lingua_src, lingua_dest) VALUES (?,?,?)"
        args = (chat_id, lingua_src, lingua_dest)
        self.conn.execute(stmt, args)
        self.conn.commit()

    # Cancello un nuovo record
    def delete_item(self, chat_id):
        stmt = "DELETE FROM user WHERE id = (?)"
        args = (chat_id)
        self.conn.execute(stmt, args)
        self.conn.commit()

    # Estrai record
    def get_items(self, chat_id):
        stmt = "SELECT * FROM user WHERE id = (?)"
        args = (chat_id)
        # return [x[0] for x in self.conn.execute(stmt,[args])]
        return [x for x in self.conn.execute(stmt,[args])]

    # Aggiorna record
    def update_items(self, chat_id, lingua_src, lingua_dest):
        stmt = "UPDATE user SET lingua_src = (?), lingua_dest = (?) where id = (?)"
        args = (lingua_src, lingua_dest, chat_id)
        self.conn.execute(stmt, args)
        self.conn.commit()
