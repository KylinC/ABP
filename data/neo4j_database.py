from neo4j import GraphDatabase

def database(user = 'neo4j', pwd = '19980511'):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=(user, pwd))
    return driver