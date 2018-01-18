from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def welcomePage():
    return "<strong>TP WEB SEMANTIQUE: Jonathan YUE CHUN, Valentin Bouchevreau, Quentin Levavasseur</strong>"
    
@app.route("/test")
def testPage():
    return "<strong style=\"'color':red\"> Ceci est un test...</strong>"
    
@app.route("/query/<data>", methods=['GET', 'POST'])
def queryParser(data):
    if request.method == 'GET':
        return request.path
    else:
        return str(data)
        