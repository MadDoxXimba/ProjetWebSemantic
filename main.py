from flask import Flask
app = Flask(__name__)

@app.route("/")
def welcomePage():
    return "<strong>TP WEB SEMANTIQUE: Jonathan YUE CHUN, Valentin Bouchevreau, Quentin Levavasseur</strong>"
    
@app.route("/test")
def testPage():
    return "<strong style=\"'color':red\"> Ceci est un test...</strong>"