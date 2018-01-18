from flask import Flask, request
from databaseManager import connection

app = Flask(__name__)

@app.route("/")
def welcomePage():
    return "<strong>TP WEB SEMANTIQUE: Jonathan YUE CHUN, Valentin Bouchevreau, Quentin Levavasseur</strong>"
    
@app.route("/test")
def testPage():
    connection.connect()
    return "<strong style=\"'color':red\">" + connection.connect() + "</strong>"
    
@app.route("/query/<data>", methods=['GET', 'POST'])
def queryParser(data):
    if request.method == 'GET':
        return request.path
    else:
        return str(data)
        