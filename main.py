from flask import Flask, request, render_template
from databaseManager import connection
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import os
import sys
from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('main', 'views'),
    autoescape=select_autoescape(['html', 'xml'])
)

app = Flask(__name__)

class mydict(dict):
    def __str__(self):
        return json.dumps(self)

@app.route("/")
def welcomePage():

    sparqlCities = SPARQLWrapper("https://herokufuseki.herokuapp.com/WebSemantic/query")

    # QUERY THE SERVER

    sparqlCities.setQuery("""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX n1: <https://tpws/>
        SELECT DISTINCT ?label_69
        WHERE { ?ville_1 a n1:ville .
        ?ville_1 n1:nom ?nom_50 .
        ?nom_50 rdfs:label ?label_69 . }
        ORDER BY ?label_69
    """)

    # RESPONSE FROM SERVER

    sparqlCities.setReturnFormat(JSON)
    cities = sparqlCities.query().convert()
    
    listCities=[]
    for obj in cities['results']['bindings']:
        listCities.append(obj['label_69']['value'])

    # JSON FORMAT

    template = env.get_template('queryform.html')
    return render_template(template, result1 = listCities)
    
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

        sparql.setQuery("""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX n1: <https://tpws/>
            SELECT DISTINCT ?label_100 
            WHERE { ?offre_22 a n1:offre .
            ?offre_22 n1:nom ?nom_100 .
            ?nom_100 rdfs:label ?label_100 .
            ?possede_43 a n1:contact .
            ?offre_22 n1:possede ?possede_43 .
            ?possede_43 n1:situeA ?situeA_65 .
            ?situeA_65 n1:ville ?ville_84 .
            ?ville_84 n1:nom ?nom_103 .
            ?nom_103 rdfs:label '"""+str(result[0])+"""' . }
            ORDER BY ?label_100
            LIMIT 50
        """)

        # RESPONSE FROM SERVER
        # JSON FORMAT

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        
        # JSON FORMAT

        listOffers=[]
        for obj in results['results']['bindings']:
            listOffers.append(obj['label_100']['value'])

        edges = []
        nodes = [{"id": 0, "label": result[0], "group": 1}]

        cpt = 1
        for o in listOffers:
            nodes.append({"id": cpt, "label": o, "group": 2})
            edges.append({"from": cpt, "to": 0})
            cpt = cpt +1


        nodes = [mydict(n) for n in nodes]

        # result for user
        template = env.get_template('result.html')
        
    return render_template(template, city = str(result[0]), offers = listOffers, result1 = edges, result2 = nodes)