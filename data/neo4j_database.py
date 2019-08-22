from neo4j import GraphDatabase

def database(user = 'neo4j', pwd = '123'):
    driver = GraphDatabase.driver("bolt://192.168.15.150:7687", auth=(user, pwd))
    return driver