def buildNodes(nodeRecord):
    if(len(nodeRecord._labels) != 0):
        data = {"id": nodeRecord._id, "label": list(nodeRecord._labels)[0], "symbolSize": 15} #将集合元素变为list，然后取出值
        if(data['label'] == 'FlowControl'):
            data.update({'category': 1})
        else:
            data.update({'category': 0})
    else:
        data = {"id": nodeRecord._id}
    data.update(dict(nodeRecord._properties))
    if('title' in data):
        data["name"] = data["title"]
    data["detail"] = str(nodeRecord._properties)
    return data


def buildNodesforroute(nodeRecord):
    if(len(nodeRecord._labels) != 0):
        data = {"id": nodeRecord._id, "label": list(nodeRecord._labels)[0], "symbolSize": 15}
        data_property = dict(nodeRecord._properties)
        print(data_property)
        if(data['label'] == 'FlightObject'):
            data.update({'category': 0})
        elif(data['label'] == 'RoutePoint'):
            data.update({'category': 3})
        elif(data['label'] == 'RouteSegment'):
            data.update({'category': 1})
        else:
            data.update({'category': 2})
    else:
        data = {"id": nodeRecord._id, "symbolSize": 20}
    data.update(dict(nodeRecord._properties))
    if('title' in data):
        data["name"] = data["title"]
    data["detail"] = str(nodeRecord._properties)
    return data
 
 
def buildEdges(relationRecord):
    data = {"id":relationRecord._id,
            "source": relationRecord.start_node._id,
            "target":relationRecord.end_node._id,
            "name": relationRecord.type,
            }
    return data