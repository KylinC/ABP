from neo4j import GraphDatabase
from data.REdata import *
from data.neo4j_database import database

def KGgenerate(aim_statement):
    driver = database()

    aim_dict = addFlowControlToKG(aim_statement)
    aim_dict_list = list(aim_dict.keys())

    with driver.session() as session:
        aim_embed_state="'"+aim_statement+"'"
        aim_embed_code="'"+aim_dict["限流点"]+"_"+aim_dict["发布时间"]+"'"
        aim_embed_routepoint="'"+aim_dict["限流点"]+"'"
        aim_embed_route="'"+aim_dict["航路"]+"'"
        state="merge (n:FlowControl{name:'FlowControl',code:%s,content:%s})"%(aim_embed_code,aim_embed_state)
        session.run(state)
        relation_state1="match (n:FlowControl{code:%s}),(m:RoutePoint{code:%s}) merge (n)-[r:FlowControlRoutePoint]->(m)"%(aim_embed_code,aim_embed_routepoint)
        relation_state2="match (n:FlowControl{code:%s}),(m:Route{code:%s}) merge (n)-[r:FlowControlRoute]->(m)"%(aim_embed_code,aim_embed_route)
        session.run(relation_state1)
        session.run(relation_state2)
        for relation in aim_dict_list:
            embed_state = aim_dict[relation]
            embed_state = "'"+embed_state+"'"
            state="match (n:FlowControl{content:%s}) merge (n)-[r:%s]->(b:Element{name:%s})"%(aim_embed_state,relation,embed_state)
            session.run(state)
    return aim_dict

def generate_test():
    inputstr = r'"北京区管","上海","限制上海方向南苑,天津落地出UDINO H104航路 30分钟一架","军事活动","201810171657 ","201810172000 ","201810172200 "'
    print(KGgenerate(inputstr))

if __name__ == "__main__":
    generate_test()