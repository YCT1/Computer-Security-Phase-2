from enum import Enum
import random as rd

class Block(Enum):
    Valid = 1
    Invalid = 2
    
class TrustState(Enum):
    FullyTrustworthy = 1
    Trustworthy = 2
    Beginner = 3
    Suspicious = 4
    Untrusted = 5

class DNServer:
    def __init__(self, nodes : list, timedReduceMinutes=30):
        self.nodes = nodes
        self.timer = 0
        self.timedReduceMinutes = timedReduceMinutes
    def tick(self):
        #Do Something
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
        pass

class Node:
    def __init__(self, id, DNServer: DNServer, correctSendingProbabity=0.9):
        self.id = id
        self.trustPoint = 0
        self.neighbors = []
        self.limit = 25

        self.BlockCount = 0

        self.isReachedToLimit = False
        self.isTrusted = ""
        self.isActive = True

        self.DNServer = DNServer

        self.correctSendingProbabity = correctSendingProbabity
    # If the sended blockchain correct, this function will be called to increase trust point
    def addTrustPoint(self, k=0.07):
        self.trustPoint = self.trustPoint + 1/(k * self.trustPoint)

    # If the sended blockchain wrong, ithis function will be called to reduce trust point
    def reduceTrustPoint(self, j=0.3,c = -5):
        self.trustPoint = self.trustPoint - (j*self.trustPoint) + c
    
    # Reduce the trust point with time
    def timedReduce(self, d=0.99993):
        self.trustPoint *= d

    # Connect to neighbors via server
    def connectNeighbors (self):
        neighbors = self.DNServer.recommendNeighbors()
        self.neighbors = neighbors

        if len(neighbors) > self.limit:
            raise ValueError("Nodes cannot have more than ", self.limit)
        else:
            pass
    
    # Sending to the server
    def send(self, block:Block):
        self.BlockCount += 1

        probabality = rd.random()
        
        
        if probabality > self.correctSendingProbabity:
            # Yanlış
            return block.Invalid
        else:
            return block.Valid


