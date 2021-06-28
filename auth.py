# coding=utf-8

saved_username = 'admin'
saved_password = '123456'

def login(username, password):
    return username == saved_username and password == saved_password

def change_password(old, new):
    global saved_password
    if old == saved_password:
        saved_password = new
        return True
    return False
