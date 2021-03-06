from model import DNServer, Node
import pandas as pd

NUMBER_OF_NODE = 100
nodeList = []
for i in range(NUMBER_OF_NODE):
    node = Node(i,correctSendingProbability=0.95)
    nodeList.append(node)


server = DNServer(nodeList)

# Simulate
server.simulate(days=3)


print("OLDU")

results,data =  server.getCurrentState()

for result in results:
    print(result)

print("Attacking Phase")

NUMBER_OF_NODE_ATTACKER = 50
nodeListAttacker = []
for i in range(100,100+NUMBER_OF_NODE_ATTACKER):
    node = Node(i,correctSendingProbability=0.7,isAttacker=True)
    nodeListAttacker.append(node)

server = DNServer(nodeList + nodeListAttacker)

# Simulate
server.simulate(days=1)


print("OLDU")

results,data =  server.getCurrentState()

#results = sorted(results, key=lambda x: x[1], reverse=True)
for result in results:
    print(result)

print(data)

