from flask import Flask, request, render_template
from databaseManager import connection
from SPARQLWrapper import SPARQLWrapper, JSON
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
        
        '''Example 1'''
        
        # GET POST DATA on form submit
        
        result = request.form.getlist('key')
        
        # Connect to SPARQL SERVER      

        sparql = SPARQLWrapper("https://herokufuseki.herokuapp.com/WebSemantic/query")
        #sparql = SPARQLWrapper("https://herokufuseki.herokuapp.com/WebSemantic/sparql")
        #sparql = SPARQLWrapper("https://herokufuseki.herokuapp.com/WebSemantic/update")

        # QUERY THE SERVER
        print("pre-query")
        sparql.setQuery("""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX n1: <https://tpws/>
            SELECT DISTINCT ?offre_22 ?possede_43 ?situeA_65 ?ville_84 ?nom_103
            WHERE { ?offre_22 a n1:offre .
            ?possede_43 a n1:contact .
            ?offre_22 n1:possede ?possede_43 .
            ?possede_43 n1:situeA ?situeA_65 .
            ?situeA_65 n1:ville ?ville_84 .
            ?ville_84 n1:nom ?nom_103 .
            ?nom_103 rdfs:label 'LAVAL' . }
            LIMIT 200
        """)
        print("post-query")
        # RESPONSE FROM SERVER
        
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        
        # JSON FORMAT
        
        #print(results)
        #print(query)

        # result for user
        template = env.get_template('result.html')
        
    return render_template(template, result = result)
    
        