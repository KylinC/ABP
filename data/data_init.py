def buildNodes(nodeRecord): #构建web显示节点
    if(len(nodeRecord._labels) != 0):
        data = {"id": nodeRecord._id, "label": list(nodeRecord._labels)[0]} #将集合元素变为list，然后取出值
        if(data['label'] == 'Movie'):
            data.update({'category': 0})
        else:
            data.update({'category': 1})
    else:
        data = {"id": nodeRecord._id}
    data.update(dict(nodeRecord._properties))
    if('title' in data):
        data["name"] = data["title"]
    return data
 
 
def buildEdges(relationRecord): #构建web显示边
    data = {"id":relationRecord._id,
            "source": relationRecord.start_node._id,
            "target":relationRecord.end_node._id,
            "name": relationRecord.type}
    return data