from flask import session
import mysql.connector

class Account:
    def __intit__(self, email, name, password, hp_no):
        self.email = email
        self.name = name
        self.password = password
        self.hp_no = hp_no
        self.status = "active"

    def login():

        return 1

    def logout():

        return 2
