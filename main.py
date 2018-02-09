from flask import Flask, request, render_template
from databaseManager import connection
from SPARQLWrapper import SPARQLWrapper, JSON
from decimal import *
import json
import os
import sys
from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('main', 'views'),
    autoescape=select_autoescape(['html', 'xml'])
)


fusekiURL = "http://jyc.northeurope.cloudapp.azure.com:8085/WebSemantic/query"

app = Flask(__name__)

class mydict(dict):
    def __str__(self):
        return json.dumps(self)

@app.route("/")
def welcomePage():
    global fusekiURL
    print(fusekiURL)
    sparqlCities = SPARQLWrapper(fusekiURL)

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
        
@app.route("/map", methods=['GET', 'POST'])
def mapPage():
    if request.method == 'POST':
        template = env.get_template('map.html')
        
        # GET POST DATA on form submit
        
        result = request.form.getlist('key')

        # Connect to SPARQL SERVER      
        global fusekiURL
        sparql = SPARQLWrapper(fusekiURL)
        #sparql = SPARQLWrapper("https://herokufuseki.herokuapp.com/WebSemantic/sparql")
        #sparql = SPARQLWrapper("https://herokufuseki.herokuapp.com/WebSemantic/update")

        # QUERY THE SERVER

        sparql.setQuery("""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX n1: <https://tpws/>
            SELECT DISTINCT ?label_100 ?label_long ?label_lat
            WHERE { ?offre_22 a n1:offre .
            ?offre_22 n1:nom ?nom_100 .
            ?nom_100 rdfs:label ?label_100 .
            ?offre_22 n1:possede ?possede_43 .
            ?possede_43 n1:situeA ?situeA_65 .
            ?situeA_65 n1:ville ?ville_84 .
            ?ville_84 n1:nom ?nom_103 .
            ?nom_103 rdfs:label '"""+str(result[0])+"""' . 
            ?situeA_65 n1:longitude ?longitude .
            ?situeA_65 n1:latitude ?latitude .
            ?longitude rdfs:label ?label_long .
            ?latitude rdfs:label ?label_lat .}
        """)

        # RESPONSE FROM SERVER
        # JSON FORMAT

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        
        # JSON FORMAT

        listOffers=[]
        for obj in results['results']['bindings']:
            listOffers.append([""+obj['label_100']['value'].replace('"','')+"",
                float(obj['label_lat']['value']),
                float(obj['label_long']['value'])])

        print(listOffers)
        
        return render_template(template, result = listOffers)

@app.route("/graph", methods=['GET', 'POST'])
def graphPage():
    if request.method == 'POST':
        template = env.get_template('graph.html')
    
        nodes = [
                {"id": 0, "label": "Offre", "group": 1},
                {"id": 1, "label": "Nom", "group": 2},
                {"id": 2, "label": "TypeActivité", "group": 2},
                {"id": 3, "label": "Contact", "group": 2},
                {"id": 4, "label": "NuméroDeTéléphone", "group": 3},
                {"id": 5, "label": "AdresseMail", "group": 3},
                {"id": 6, "label": "UrlSiteWeb", "group": 3},
                {"id": 7, "label": "Localisation", "group": 3},
                {"id": 8, "label": "Latitude", "group": 4},
                {"id": 9, "label": "Longitude", "group": 4},
                {"id": 10, "label": "Adresse", "group": 4},
                {"id": 11, "label": "Ville", "group": 4},
                {"id": 12, "label": "Nom", "group": 5},
                {"id": 13, "label": "CodePostal", "group": 5}
            ]

        edges = [
                {"from": 1, "to": 0},
                {"from": 2, "to": 0},
                {"from": 3, "to": 0},
                {"from": 4, "to": 3},
                {"from": 5, "to": 3},
                {"from": 6, "to": 3},
                {"from": 7, "to": 3},
                {"from": 8, "to": 7},
                {"from": 9, "to": 7},
                {"from": 10, "to": 7},
                {"from": 11, "to": 7},
                {"from": 12, "to": 11},
                {"from": 13, "to": 11}
            ]

        return render_template(template, result1 = edges, result2 = nodes)
        
@app.route("/resultOffersByCity", methods=['GET', 'POST'])
def getForm():
    if request.method == 'POST':
        
        '''Example 1'''
        
        # GET POST DATA on form submit
        
        result = request.form.getlist('key')

        # Connect to SPARQL SERVER      
        global fusekiURL
        sparql = SPARQLWrapper(fusekiURL)
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
        template = env.get_template('resultOffersByCity.html')
        
        return render_template(template, city = str(result[0]), offers = listOffers, result1 = edges, result2 = nodes)

@app.route("/resultTypesOffersByCity", methods=['GET', 'POST'])
def getForm2():
    if request.method == 'POST':
        # GET POST DATA on form submit
        
        result = request.form.getlist('key')

        # Connect to SPARQL SERVER      
        global fusekiURL
        sparql = SPARQLWrapper(fusekiURL)
        #sparql = SPARQLWrapper("https://herokufuseki.herokuapp.com/WebSemantic/sparql")
        #sparql = SPARQLWrapper("https://herokufuseki.herokuapp.com/WebSemantic/update")

        # QUERY THE SERVER

        sparql.setQuery("""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX n1: <https://tpws/>
            SELECT DISTINCT ?label_100 ?label_1
            WHERE { ?offre_22 a n1:offre .
            ?offre_22 n1:nom ?nom_100 .
            ?nom_100 rdfs:label ?label_100 .
            ?possede_43 a n1:contact .
            ?offre_22 n1:possede ?possede_43 .
            ?possede_43 n1:situeA ?situeA_65 .
            ?situeA_65 n1:ville ?ville_84 .
            ?ville_84 n1:nom ?nom_103 .
            ?type_3 rdfs:label ?label_1 .
            ?offre_22 n1:type ?type_3 .
            ?nom_103 rdfs:label '"""+str(result[0])+"""' . }
            ORDER BY ?label_100
        """)

        # RESPONSE FROM SERVER
        # JSON FORMAT

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        
        # JSON FORMAT

        listOffers=[]
        listTypes=[]
        for obj in results['results']['bindings']:
            listOffers.append(obj['label_100']['value'])
            listTypes.append(obj['type_3']['value]'])
        
        edges = []
        nodes = [{"id": 0, "label": result[0], "group": 1}]

        cptO = 1
        cptT = 0
        for o in listOffers:
            nodes.append({"id": cptO, "label": o, "group": 2})
            edges.append({"from": cptO, "to": 0})
            
            cptT = cptO + 1
            for t in listTypes:
                nodes.append({"id": cptT, "label": t, "group": 3})
                edges.append({"from": cptT, "to": cptO})
                cptT = cptT + 1
            cptO = cptO + cptT
            cptO = cptO + 1

        nodes = [mydict(n) for n in nodes]

        # result for user
        template = env.get_template('resultOffersByCity.html')
        
        return render_template(template, city = str(result[0]), offers = listOffers, types = listTypes, result1 = edges, result2 = nodes)

@app.route("/resultNbOffersByCities", methods=['GET', 'POST'])
def getForm3():
    if request.method == 'POST':
        # GET POST DATA on form submit
        
        result = request.form.getlist('key')
        template = env.get_template('resultNbOffersByCities.html')    
        
        return render_template(template)