# coding=utf-8

from flask import Flask, request
from gevent.pywsgi import WSGIServer
import auth
import search
import analyse

port = 5000
app = Flask(__name__,
            static_folder="public",
            static_url_path="/")

@app.route("/auth/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if auth.login(username, password):
        return 'ok'
    else:
        return 'fail', 403

@app.route("/auth/set_password", methods=['POST'])
def set_password():
    old = request.form['old']
    new = request.form['new']
    if auth.change_password(old, new):
        return 'ok'
    else:
        return 'fail', 403

@app.route("/search_article")
def search_article():
    return search.query(request.args.get('keywords'), request.args.get('start'), request.args.get('end'))

@app.route("/get_label")
def get_label():
    return analyse.get_label(request.args.get('level'))

@app.route("/get_label_stat")
def get_label_stat():
    return analyse.get_label_stat(request.args.get('level'))

@app.route("/get_court_stat")
def get_court_stat():
    if request.args.get('labels') == None or request.args.get('labels') == '':
        labels = []
    else:
        labels = request.args.get('labels').split(',')
    return analyse.get_court_stat(labels)

@app.route("/get_decision_stat")
def get_decision_stat():
    if request.args.get('labels') == None or request.args.get('labels') == '':
        labels = []
    else:
        labels = request.args.get('labels').split(',')
    return analyse.get_decision_stat(labels)

@app.route("/get_person_stat")
def get_person_stat():
    if request.args.get('labels') == None or request.args.get('labels') == '':
        labels = []
    else:
        labels = request.args.get('labels').split(',')
    return analyse.get_person_stat(labels, request.args.get('defendant') == 'true')

@app.route("/get_law_stat")
def get_law_stat():
    if request.args.get('labels') == None or request.args.get('labels') == '':
        labels = []
    else:
        labels = request.args.get('labels').split(',')
    return analyse.get_law_stat(labels)

@app.route("/get_clause_stat")
def get_clause_stat():
    if request.args.get('labels') == None or request.args.get('labels') == '':
        labels = []
    else:
        labels = request.args.get('labels').split(',')
    return analyse.get_clause_stat(labels, request.args.get('law'))

@app.route("/get_year_stat")
def get_year_stat():
    if request.args.get('labels') == None or request.args.get('labels') == '':
        labels = []
    else:
        labels = request.args.get('labels').split(',')
    return analyse.get_year_stat(labels)

@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file('favicon.ico')

@app.route("/<path>")
def default(path):
    return app.send_static_file('index.html')

@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    environ.headers['Access-Control-Allow-Method']='*'
    environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ

http_server = WSGIServer(('', port), app)
print('Server listening at http://localhost:%d' % port)
http_server.serve_forever()