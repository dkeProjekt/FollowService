from py2neo import Graph, Node, Relationship, NodeMatcher
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from py2neo.client import json
from pymongo import MongoClient
import json as js

app = Flask(__name__)
CORS(app, support_credentials=True)

# Verbindung zur Datenbank erstellen
try:
    graph = Graph('bolt://localhost:7687', auth=('neo4j', 'secret'))
    print('SUCCESS: Connected to the Neo4j Database.')
except Exception as e:
    print('ERROR: Could not connect to the Neo4j Database. See console for details.')
    raise SystemExit(e)


@app.route('/create', methods=['POST'])
def create():
    if not request.json:
        abort(400)
    name = request.json.get("name")
    a = Node('Person', name=name)
    graph.create(a)

    return jsonify({'created': True, 'name': name})


@app.route('/follow', methods=['POST'])
def follow():
    if not request.json:
        abort(400)
    name = request.json.get("name")
    followName = request.json.get("followName")

    graph.run("MATCH (a:Person {name: $name}),(b:Person {name: $followName})MERGE (a)-[r:FOLLOWS]->(b)", name=name,
              followName=followName).data()

    return jsonify({'follows': True})


@app.route('/unfollow', methods=['POST'])
def unfollow():
    if not request.json:
        abort(400)
    name = request.json.get("name")
    unfollowName = request.json.get("unfollowName")

    graph.run("MATCH(a:Person {name:$name})-[r:FOLLOWS]->(b:Person {name:$unfollowName}) DELETE r", name=name,
              unfollowName=unfollowName).data()

    return jsonify({'unfollow': True})


@app.route('/getfollowed', methods=['GET'])
def getfollowed():
    if not request.json:
        abort(400)
    name = request.json.get("name")

    t = graph.run("MATCH(a: Person{name: $name})-[r: FOLLOWS]->(FOLGT)RETURN FOLGT", name=name).data()

    return jsonify(t)


@app.route('/get_all_users', methods=['GET'])
def get_all_users():
    client = MongoClient(
        "mongodb+srv://Adri25:adri1234@cluster0.taxsc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    database = client['PRDKE']
    collection = database['UserData']
    users = collection.find()
    user_names = []
    for user in users:
        user_names.append(user["name"])

    user_names_json = js.dumps(user_names)
    return jsonify({'get_all_users_successful': True, "list_of_users": user_names_json})


if __name__ == '__main__':
    app.run(debug=True, port=5005)

