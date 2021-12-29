from enum import Enum
import random as rd
import pandas as pd

class Block(Enum):
    Valid = 1
    Invalid = 2
    
class TrustState(Enum):
    FullyTrustworthy = 1
    Trustworthy = 2
    Beginner = 3
    Suspicious = 4
    Untrusted = 5
class Node:
    def __init__(self, id, correctSendingProbability=0.9):
        self.id = id
        self.trustPoint = 0
        self.neighbors = []
        self.limit = 25

        self.BlockCount = 0

        self.isReachedToLimit = False
        self.isTrusted = ""
        self.isActive = True

        self.sended = [0,0] #  (Valid, Invalid)

        self.correctSendingProbability = correctSendingProbability
    # If the sended blockchain correct, this function will be called to increase trust point
    def addTrustPoint(self, k=0.07, epsilon=10**-3):
        self.trustPoint = self.trustPoint + 1/(k * (abs(self.trustPoint)+epsilon))

    # If the sended blockchain wrong, ithis function will be called to reduce trust point
    def reduceTrustPoint(self, j=0.3,c = -5):
        self.trustPoint = self.trustPoint - (j*abs(self.trustPoint)) + c
    
    # Reduce the trust point with time
    def timedReduce(self, d=0.99993):
        self.trustPoint *= d

    # Connect to neighbors from server
    def connectNeighbors (self,neighbors:list):
        self.neighbors = neighbors

        if len(neighbors) > self.limit:
            raise ValueError("Nodes cannot have more than ", self.limit)
        else:
            pass
    
    # Sending to the server
    def send(self):
        self.BlockCount += 1

        probabality = rd.random()
        
        if probabality > self.correctSendingProbability:
            # Yanlış
            self.sended[1] += 1
            return Block.Invalid
        else:
            self.sended[0] += 1
            return Block.Valid


class DNServer:
    def __init__(self, nodes : list, timedReduceMinutes=30):
        self.nodes = nodes
        self.timer = 0
        self.timedReduceMinutes = timedReduceMinutes
    def tick(self):
        
        # Get all blocks from all nodes (every 10 min)
        
            # Update Trust Points by checking valid or invalid blocks

            # Update Trust States for each node

        if self.timer % 10 == 0:
            # Get all blocks
            for node in self.nodes:
                block = node.send() 
                if block == Block.Invalid:
                    node.reduceTrustPoint()
                else:
                    node.addTrustPoint()
        # Send newly Updated Lists to all connected Nodes (every 30 minutes)
            # Get the recommendations and send it to all nodes
        

        if self.timer%30 == 0:
            for node in self.nodes:
                #recommendationList = self.recommendNeighbors()
                #node.connectNeighbors(recommendationList)
                pass

        # Reduce the Trust point if desired minutes passed
        if self.timer%self.timedReduceMinutes == 0:
            for node in self.nodes:
                node.timedReduce()

        # Increase the timer        
        self.timer += 1

    def simulate(self, days=10):
        for i in range(0, days*24*60):
            self.tick()


    def recommendNeighbors(self):
        # List of Nodes should be return
        pass

    def getCurrentState(self):

        results = []

        for node in self.nodes:
            results.append( (node.id, node.trustPoint, node.sended))
        
        #state = pd.DataFrame(self.nodes)

        return results


