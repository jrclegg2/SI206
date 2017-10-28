import networkx as nx

G = nx.Graph()
G.add_edge("A", "B", sign="+")
G.add_edge("A", "C", sign="+")
G.add_edge("A", "D", sign="+")
G.add_edge("A", "E", sign="+")
G.add_edge("B", "C", sign="+")
G.add_edge("B", "D", sign="+")
G.add_edge("B", "E", sign="+")
G.add_edge("C", "D", sign="+")
G.add_edge("C", "E", sign="+")
G.add_edge("D", "E", sign="+")

graphTwo = nx.Graph()
graphTwo.add_edge("A", "B", sign="-")
graphTwo.add_edge("A", "C", sign="+")
graphTwo.add_edge("A", "D", sign="+")
graphTwo.add_edge("A", "E", sign="+")
graphTwo.add_edge("B", "C", sign="-")
graphTwo.add_edge("B", "D", sign="-")
graphTwo.add_edge("B", "E", sign="-")
graphTwo.add_edge("C", "D", sign="+")
graphTwo.add_edge("C", "E", sign="+")
graphTwo.add_edge("D", "E", sign="+")

graphThree = nx.Graph()
graphThree.add_edge("A", "B", sign="+")
graphThree.add_edge("A", "C", sign="-")
graphThree.add_edge("A", "D", sign="+")
graphThree.add_edge("A", "E", sign="+")
graphThree.add_edge("B", "C", sign="+")
graphThree.add_edge("B", "D", sign="+")
graphThree.add_edge("B", "E", sign="+")
graphThree.add_edge("C", "D", sign="+")
graphThree.add_edge("C", "E", sign="+")
graphThree.add_edge("D", "E", sign="+")

numberNodes = G.number_of_nodes()

def checkAcrossGroups (G):
    numNodes = G.number_of_nodes()
    index = 0
    while index < numNodes:
        dict ={'groupA' : [], 'groupB' : []}
        starterNode = G.nodes()[index]
        index += 1
        dict['groupA'].append(starterNode)
        for x in G.neighbors(starterNode):
            if G.edge[starterNode][x]['sign'] == '+':
                dict['groupA'].append(x)
            elif G.edge[starterNode][x]['sign'] == '-':
                dict['groupB'].append(x)
        for y in dict['groupA']:
            for z in dict['groupB']:
                if G.edge[y][z]['sign'] == '+':
                    return False
    return True

def allPositive (G):
    numPositive = 0
    for node in G.nodes():
        for neighbor in G.neighbors(node):
            if G.edge[node][neighbor]['sign'] == '+':
                numPositive += 1
            if G.edge[node][neighbor]['sign'] == '-':
                return False
    numPositiveFixed = numPositive / 2 # Gets out all repeat instances
    if numPositiveFixed == G.number_of_edges():
        return True

def balancedGraph(G):
    if allPositive(G) == True:
        return True
    if checkAcrossGroups(G) == True:
        return True
    else:
        return False

print ("Test One: ", balancedGraph(G))
print ("Test Two: ", balancedGraph(graphTwo))
print ("Test Three: ", balancedGraph(graphThree))
