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
        
@app.route("/map", methods=['GET', 'POST'])
def mapPage():
    if request.method == 'POST':
        template = env.get_template('map.html')
        
        # GET POST DATA on form submit
        
        result = request.form.getlist('key')

        print(result)
        
        # Connect to SPARQL SERVER      

        sparql = SPARQLWrapper("http://jyc.northeurope.cloudapp.azure.com:8085/WebSemantic/query")
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
            LIMIT 5
        """)

        # RESPONSE FROM SERVER
        # JSON FORMAT

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        
        # JSON FORMAT

        print(results)

        listOffers=[]
        for obj in results['results']['bindings']:
            listOffers.append([obj['label_100']['value'],
                float(obj['label_lat']['value']),
                float(obj['label_long']['value'])])

        print(listOffers)
        
        return render_template(template, result = listOffers)

@app.route("/graph", methods=['GET', 'POST'])
def graphPage():
    if request.method == 'POST':
        template = env.get_template('graph.html')
        
        chart = {"renderTo": 1, "type": 2, "height": 3,}
        series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
        title = {"text": 'My Title'}
        xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
        yAxis = {"title": {"text": 'yAxis Label'}}


        edges = [
                {"from": 1, "to": 0}, #LA CLE DOIT TOUJOURS ETRE UN STRING
                {"from": 2, "to": 0},
                {"from": 3, "to": 0},
                {"from": 3, "to": 2},
                {"from": 4, "to": 0},
                {"from": 5, "to": 0},
                {"from": 6, "to": 0},
                {"from": 7, "to": 0},
                {"from": 8, "to": 0},
                {"from": 9, "to": 0},
                {"from": 11, "to": 10},
                {"from": 11, "to": 3},
                {"from": 11, "to": 2},
                {"from": 11, "to": 0},
                {"from": 12, "to": 11},
                {"from": 13, "to": 11},
                {"from": 14, "to": 11},
                {"from": 15, "to": 11},
                {"from": 17, "to": 16},
                {"from": 18, "to": 16},
                {"from": 18, "to": 17},
                {"from": 19, "to": 16},
                {"from": 19, "to": 17},
                {"from": 19, "to": 18},
                {"from": 20, "to": 16},
                {"from": 20, "to": 17},
                {"from": 20, "to": 18},
                {"from": 20, "to": 19},
                {"from": 21, "to": 16},
                {"from": 21, "to": 17},
                {"from": 21, "to": 18},
                {"from": 21, "to": 19},
                {"from": 21, "to": 20},
                {"from": 22, "to": 16},
                {"from": 22, "to": 17},
                {"from": 22, "to": 18},
                {"from": 22, "to": 19},
                {"from": 22, "to": 20},
                {"from": 22, "to": 21},
                {"from": 23, "to": 16},
                {"from": 23, "to": 17},
                {"from": 23, "to": 18},
                {"from": 23, "to": 19},
                {"from": 23, "to": 20},
                {"from": 23, "to": 21},
                {"from": 23, "to": 22},
                {"from": 23, "to": 12},
                {"from": 23, "to": 11},
                {"from": 24, "to": 23},
                {"from": 24, "to": 11},
                {"from": 25, "to": 24},
                {"from": 25, "to": 23},
                {"from": 25, "to": 11},
                {"from": 26, "to": 24},
                {"from": 26, "to": 11},
                {"from": 26, "to": 16},
                {"from": 26, "to": 25},
                {"from": 27, "to": 11},
                {"from": 27, "to": 23},
                {"from": 27, "to": 25},
                {"from": 27, "to": 24},
                {"from": 27, "to": 26},
                {"from": 28, "to": 11},
                {"from": 28, "to": 27},
                {"from": 29, "to": 23},
                {"from": 29, "to": 27},
                {"from": 29, "to": 11},
                {"from": 30, "to": 23},
                {"from": 31, "to": 30},
                {"from": 31, "to": 11},
                {"from": 31, "to": 23},
                {"from": 31, "to": 27},
                {"from": 32, "to": 11},
                {"from": 33, "to": 11},
                {"from": 33, "to": 27},
                {"from": 34, "to": 11},
                {"from": 34, "to": 29},
                {"from": 35, "to": 11},
                {"from": 35, "to": 34},
                {"from": 35, "to": 29},
                {"from": 36, "to": 34},
                {"from": 36, "to": 35},
                {"from": 36, "to": 11},
                {"from": 36, "to": 29},
                {"from": 37, "to": 34},
                {"from": 37, "to": 35},
                {"from": 37, "to": 36},
                {"from": 37, "to": 11},
                {"from": 37, "to": 29},
                {"from": 38, "to": 34},
                {"from": 38, "to": 35},
                {"from": 38, "to": 36},
                {"from": 38, "to": 37},
                {"from": 38, "to": 11},
                {"from": 38, "to": 29},
                {"from": 39, "to": 25},
                {"from": 40, "to": 25},
                {"from": 41, "to": 24},
                {"from": 41, "to": 25},
                {"from": 42, "to": 41},
                {"from": 42, "to": 25},
                {"from": 42, "to": 24},
                {"from": 43, "to": 11},
                {"from": 43, "to": 26},
                {"from": 43, "to": 27},
                {"from": 44, "to": 28},
                {"from": 44, "to": 11},
                {"from": 45, "to": 28},
                {"from": 47, "to": 46},
                {"from": 48, "to": 47},
                {"from": 48, "to": 25},
                {"from": 48, "to": 27},
                {"from": 48, "to": 11},
                {"from": 49, "to": 26},
                {"from": 49, "to": 11},
                {"from": 50, "to": 49},
                {"from": 50, "to": 24},
                {"from": 51, "to": 49},
                {"from": 51, "to": 26},
                {"from": 51, "to": 11},
                {"from": 52, "to": 51},
                {"from": 52, "to": 39},
                {"from": 53, "to": 51},
                {"from": 54, "to": 51},
                {"from": 54, "to": 49},
                {"from": 54, "to": 26},
                {"from": 55, "to": 51},
                {"from": 55, "to": 49},
                {"from": 55, "to": 39},
                {"from": 55, "to": 54},
                {"from": 55, "to": 26},
                {"from": 55, "to": 11},
                {"from": 55, "to": 16},
                {"from": 55, "to": 25},
                {"from": 55, "to": 41},
                {"from": 55, "to": 48},
                {"from": 56, "to": 49},
                {"from": 56, "to": 55},
                {"from": 57, "to": 55},
                {"from": 57, "to": 41},
                {"from": 57, "to": 48},
                {"from": 58, "to": 55},
                {"from": 58, "to": 48},
                {"from": 58, "to": 27},
                {"from": 58, "to": 57},
                {"from": 58, "to": 11},
                {"from": 59, "to": 58},
                {"from": 59, "to": 55},
                {"from": 59, "to": 48},
                {"from": 59, "to": 57},
                {"from": 60, "to": 48},
                {"from": 60, "to": 58},
                {"from": 60, "to": 59},
                {"from": 61, "to": 48},
                {"from": 61, "to": 58},
                {"from": 61, "to": 60},
                {"from": 61, "to": 59},
                {"from": 61, "to": 57},
                {"from": 61, "to": 55},
                {"from": 62, "to": 55},
                {"from": 62, "to": 58},
                {"from": 62, "to": 59},
                {"from": 62, "to": 48},
                {"from": 62, "to": 57},
                {"from": 62, "to": 41},
                {"from": 62, "to": 61},
                {"from": 62, "to": 60},
                {"from": 63, "to": 59},
                {"from": 63, "to": 48},
                {"from": 63, "to": 62},
                {"from": 63, "to": 57},
                {"from": 63, "to": 58},
                {"from": 63, "to": 61},
                {"from": 63, "to": 60},
                {"from": 63, "to": 55},
                {"from": 64, "to": 55},
                {"from": 64, "to": 62},
                {"from": 64, "to": 48},
                {"from": 64, "to": 63},
                {"from": 64, "to": 58},
                {"from": 64, "to": 61},
                {"from": 64, "to": 60},
                {"from": 64, "to": 59},
                {"from": 64, "to": 57},
                {"from": 64, "to": 11},
                {"from": 65, "to": 63},
                {"from": 65, "to": 64},
                {"from": 65, "to": 48},
                {"from": 65, "to": 62},
                {"from": 65, "to": 58},
                {"from": 65, "to": 61},
                {"from": 65, "to": 60},
                {"from": 65, "to": 59},
                {"from": 65, "to": 57},
                {"from": 65, "to": 55},
                {"from": 66, "to": 64},
                {"from": 66, "to": 58},
                {"from": 66, "to": 59},
                {"from": 66, "to": 62},
                {"from": 66, "to": 65},
                {"from": 66, "to": 48},
                {"from": 66, "to": 63},
                {"from": 66, "to": 61},
                {"from": 66, "to": 60},
                {"from": 67, "to": 57},
                {"from": 68, "to": 25},
                {"from": 68, "to": 11},
                {"from": 68, "to": 24},
                {"from": 68, "to": 27},
                {"from": 68, "to": 48},
                {"from": 68, "to": 41},
                {"from": 69, "to": 25},
                {"from": 69, "to": 68},
                {"from": 69, "to": 11},
                {"from": 69, "to": 24},
                {"from": 69, "to": 27},
                {"from": 69, "to": 48},
                {"from": 69, "to": 41},
                {"from": 70, "to": 25},
                {"from": 70, "to": 69},
                {"from": 70, "to": 68},
                {"from": 70, "to": 11},
                {"from": 70, "to": 24},
                {"from": 70, "to": 27},
                {"from": 70, "to": 41},
                {"from": 70, "to": 58},
                {"from": 71, "to": 27},
                {"from": 71, "to": 69},
                {"from": 71, "to": 68},
                {"from": 71, "to": 70},
                {"from": 71, "to": 11},
                {"from": 71, "to": 48},
                {"from": 71, "to": 41},
                {"from": 71, "to": 25},
                {"from": 72, "to": 26},
                {"from": 72, "to": 27},
                {"from": 72, "to": 11},
                {"from": 73, "to": 48},
                {"from": 74, "to": 48},
                {"from": 74, "to": 73},
                {"from": 75, "to": 69},
                {"from": 75, "to": 68},
                {"from": 75, "to": 25},
                {"from": 75, "to": 48},
                {"from": 75, "to": 41},
                {"from": 75, "to": 70},
                {"from": 75, "to": 71},
                {"from": 76, "to": 64},
                {"from": 76, "to": 65},
                {"from": 76, "to": 66},
                {"from": 76, "to": 63},
                {"from": 76, "to": 62},
                {"from": 76, "to": 48},
                {"from": 76, "to": 58}
            ]
       
        nodes = [
                {"id": 0, "label": "Myriel", "group": 1},
                {"id": 1, "label": "Napoleon", "group": 1},
                {"id": 2, "label": "Mlle.Baptistine", "group": 1},
                {"id": 3, "label": "Mme.Magloire", "group": 1},
                {"id": 4, "label": "CountessdeLo", "group": 1},
                {"id": 5, "label": "Geborand", "group": 1},
                {"id": 6, "label": "Champtercier", "group": 1},
                {"id": 7, "label": "Cravatte", "group": 1},
                {"id": 8, "label": "Count", "group": 1},
                {"id": 9, "label": "OldMan", "group": 1},
                {"id": 10, "label": "Labarre", "group": 2},
                {"id": 11, "label": "Valjean", "group": 2},
                {"id": 12, "label": "Marguerite", "group": 3},
                {"id": 13, "label": "Mme.deR", "group": 2},
                {"id": 14, "label": "Isabeau", "group": 2},
                {"id": 15, "label": "Gervais", "group": 2},
                {"id": 16, "label": "Tholomyes", "group": 3},
                {"id": 17, "label": "Listolier", "group": 3},
                {"id": 18, "label": "Fameuil", "group": 3},
                {"id": 19, "label": "Blacheville", "group": 3},
                {"id": 20, "label": "Favourite", "group": 3},
                {"id": 21, "label": "Dahlia", "group": 3},
                {"id": 22, "label": "Zephine", "group": 3},
                {"id": 23, "label": "Fantine", "group": 3},
                {"id": 24, "label": "Mme.Thenardier", "group": 4},
                {"id": 25, "label": "Thenardier", "group": 4},
                {"id": 26, "label": "Cosette", "group": 5},
                {"id": 27, "label": "Javert", "group": 4},
                {"id": 28, "label": "Fauchelevent", "group": 0},
                {"id": 29, "label": "Bamatabois", "group": 2},
                {"id": 30, "label": "Perpetue", "group": 3},
                {"id": 31, "label": "Simplice", "group": 2},
                {"id": 32, "label": "Scaufflaire", "group": 2},
                {"id": 33, "label": "Woman1", "group": 2},
                {"id": 34, "label": "Judge", "group": 2},
                {"id": 35, "label": "Champmathieu", "group": 2},
                {"id": 36, "label": "Brevet", "group": 2},
                {"id": 37, "label": "Chenildieu", "group": 2},
                {"id": 38, "label": "Cochepaille", "group": 2},
                {"id": 39, "label": "Pontmercy", "group": 4},
                {"id": 40, "label": "Boulatruelle", "group": 6},
                {"id": 41, "label": "Eponine", "group": 4},
                {"id": 42, "label": "Anzelma", "group": 4},
                {"id": 43, "label": "Woman2", "group": 5},
                {"id": 44, "label": "MotherInnocent", "group": 0},
                {"id": 45, "label": "Gribier", "group": 0},
                {"id": 46, "label": "Jondrette", "group": 7},
                {"id": 47, "label": "Mme.Burgon", "group": 7},
                {"id": 48, "label": "Gavroche", "group": 8},
                {"id": 49, "label": "Gillenormand", "group": 5},
                {"id": 50, "label": "Magnon", "group": 5},
                {"id": 51, "label": "Mlle.Gillenormand", "group": 5},
                {"id": 52, "label": "Mme.Pontmercy", "group": 5},
                {"id": 53, "label": "Mlle.Vaubois", "group": 5},
                {"id": 54, "label": "Lt.Gillenormand", "group": 5},
                {"id": 55, "label": "Marius", "group": 8},
                {"id": 56, "label": "BaronessT", "group": 5},
                {"id": 57, "label": "Mabeuf", "group": 8},
                {"id": 58, "label": "Enjolras", "group": 8},
                {"id": 59, "label": "Combeferre", "group": 8},
                {"id": 60, "label": "Prouvaire", "group": 8},
                {"id": 61, "label": "Feuilly", "group": 8},
                {"id": 62, "label": "Courfeyrac", "group": 8},
                {"id": 63, "label": "Bahorel", "group": 8},
                {"id": 64, "label": "Bossuet", "group": 8},
                {"id": 65, "label": "Joly", "group": 8},
                {"id": 66, "label": "Grantaire", "group": 8},
                {"id": 67, "label": "MotherPlutarch", "group": 9},
                {"id": 68, "label": "Gueulemer", "group": 4},
                {"id": 69, "label": "Babet", "group": 4},
                {"id": 70, "label": "Claquesous", "group": 4},
                {"id": 71, "label": "Montparnasse", "group": 4},
                {"id": 72, "label": "Toussaint", "group": 5},
                {"id": 73, "label": "Child1", "group": 10},
                {"id": 74, "label": "Child2", "group": 10},
                {"id": 75, "label": "Brujon", "group": 4},
                {"id": 76, "label": "Mme.Hucheloup", "group": 8}
            ]

        return render_template(template, result1 = edges, result2 = nodes, result3 = title)
        
@app.route("/resultOffersByCity", methods=['GET', 'POST'])
def getForm():
    if request.method == 'POST':
        
        '''Example 1'''
        
        # GET POST DATA on form submit
        
        result = request.form.getlist('key')

        # Connect to SPARQL SERVER      

        sparql = SPARQLWrapper("http://jyc.northeurope.cloudapp.azure.com:8085/WebSemantic/query")
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
        template = env.get_template('resultOffersByCity.html')
        
    return render_template(template, city = str(result[0]), offers = listOffers, result1 = edges, result2 = nodes)

@app.route("/resultTypesOffersByCity", methods=['GET', 'POST'])
def getForm2():
    if request.method == 'POST':
        # GET POST DATA on form submit
        
        result = request.form.getlist('key')

        # Connect to SPARQL SERVER      

        sparql = SPARQLWrapper("http://jyc.northeurope.cloudapp.azure.com:8085/WebSemantic/query")
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
            LIMIT 50
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