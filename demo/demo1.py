#!/usr/bin/env python
#encoding=utf-8

import json
from flask import Blueprint, render_template, session, redirect, url_for, request, \
    Response, flash, g, jsonify, abort
from data.neo4j_database import database
from data.data_init import *
driver = database()

mod1 = Blueprint('demo1', __name__)

@mod1.route("/demo1")
def home1():
    return render_template('demo1.html')

@mod1.route("/demo1/graphdata")
def get_graph_data():
    with driver.session() as session:
        results=session.run('MATCH (p1)-[r1]->(p2) RETURN p1,p2,r1').values()
        nodeList=[]
        edgeList=[]
        for result in results:
            nodeList.append(result[0])
            nodeList.append(result[1])
            nodeList=list(set(nodeList))
            edgeList.append(result[2])
        
        edgeList=list(set(edgeList))
        nodes = list(map(buildNodes, nodeList))
        edges= list(map(buildEdges,edgeList))
        # nodes = list(map(buildNodes,session.run("MATCH (n) RETURN n").value()))
        # edges= list(map(buildEdges,session.run("MATCH ()-[r]->() RETURN r").value()))
    # print(results)
    # print(nodes)
    # print(edges)
    json_data = json.dumps({"nodes": nodes, "edges": edges})
    callback = request.args.get('callback')
    return Response('{}({})'.format(callback, json_data))