from flask import Flask, request, render_template
from databaseManager import connection
import os
import sys
from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('main', 'views'),
    autoescape=select_autoescape(['html', 'xml'])
)

app = Flask(__name__)


@app.route("/")
def welcomePage():
    template = env.get_template('queryform.html')
    return render_template(template)
    
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
        
@app.route("/result", methods=['GET', 'POST'])
def getForm():
    if request.method == 'POST':
      result = request.form
      # logic (db connection and sparkl query parser)
      
      
      
      # result for user
      template = env.get_template('result.html')
      return render_template(template, result = result)
    
        