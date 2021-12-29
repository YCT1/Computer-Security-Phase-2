from enum import Enum
import random as rd
import numpy as np
import pandas as pd
from scipy.stats import binom
from random import normalvariate
import math

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
    def __init__(self, id, correctSendingProbability=0.9, isAttacker = False):
        self.id = id
        self.trustPoint = 0
        self.neighbors = []
        self.limit = 25

        self.BlockCount = 0

        self.isReachedToLimit = False
        self.trustState = TrustState.Beginner
        self.isActive = True

        self.isAttacker = isAttacker
        self.sended = [0,0] #  (Valid, Invalid)
        self.ratio = [0,0] # (Attacker,Trusted)

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
        # Reduce the Trust point if desired minutes passed
        if self.timer%self.timedReduceMinutes == 0:
            for node in self.nodes:
                if node.trustState != TrustState.Beginner:
                    node.timedReduce()
        
        # Get all blocks from all nodes (every 10 min)
        
            # Update Trust Points by checking valid or invalid blocks

            # Update Trust States for each node

        if self.timer % 10 == 0:
            # Get all blocks
            nodesSortedTrusted = []
            for node in self.nodes:
                block = node.send() 
                if block == Block.Invalid:
                    node.reduceTrustPoint()
                else:
                    node.addTrustPoint()
                
                # Update Nodes Trust
                if node.BlockCount < 10:
                    node.trustState = TrustState.Beginner
                else:
                    if node.trustPoint > 10:
                        node.trustState = TrustState.Trustworthy
                        nodesSortedTrusted.append(node)
                    elif node.trustPoint <= 10 and node.trustPoint > -25:
                        node.trustState = TrustState.Suspicious
                    elif node.trustPoint <= -25:
                        node.trustState = TrustState.Untrusted
                # Full Trustworthy
                
            # Gets trustworthy nodes and sorts according to trust point     
            nodesSortedTrusted = sorted(nodesSortedTrusted, key=lambda x: x.trustPoint, reverse=True)
            for i in range( int(len(nodesSortedTrusted)*0.2)):
                nodesSortedTrusted[i].trustState = TrustState.FullyTrustworthy
                
        # Send newly Updated Lists to all connected Nodes (every 30 minutes)
            # Get the recommendations and send it to all nodes
        

        if self.timer%30 == 0:
            for node in self.nodes:
                recommendationList = self.recommendNeighbors(node)
                node.connectNeighbors(recommendationList)
                attackerNumber = 0
                for reccomendation in recommendationList:
                    if reccomendation.isAttacker:
                        node.ratio[0] += 1
                        attackerNumber += 1
                    else:
                        node.ratio[1] += 1
                if attackerNumber == len(recommendationList):
                    print("CAPTURED:" ,node.id)
                            

        

        # Increase the timer        
        self.timer += 1

    def simulate(self, days=10):
        for i in range(0, days*24*60):
            self.tick()

    
    def normal_choice(self, lst, mean=None, stddev=None):
        if mean is None:
            # if mean is not specified, use center of list
            mean = (len(lst) - 1) / 2

        if stddev is None:
            # if stddev is not specified, let list be -3 .. +3 standard deviations
            stddev = len(lst) / 6

        while True:
            index = int(normalvariate(mean, stddev) + 0.5)
            if 0 <= index < len(lst):
                return lst[index]

    def recommendNeighbors(self, node:Node, k= 1 , j=0):

        state = node.trustState
        maxLimit = node.limit
        trustPoint = node.trustPoint

        # List of Nodes should be return
        recommendationList = []
        tempNodeList = self.nodes.copy()

        for node in self.nodes:
            if node.trustState == TrustState.Untrusted:
                tempNodeList.remove(node)
        
        # Check if the node is beginner
        tempNodeList = sorted(tempNodeList, key=lambda x: x.trustPoint, reverse=True)
        p = 0.0
        if state == TrustState.Beginner:
            p=0.5
        else:
            #p = 1 / (1+np.e**(-k*(trustPoint-j)))
            if trustPoint <= tempNodeList[int(len(tempNodeList) * 0.1)].trustPoint:
                p = 0.1
            elif (trustPoint <= tempNodeList[int(len(tempNodeList) * 0.2)].trustPoint):
                p = 0.2
            elif (trustPoint <= tempNodeList[int(len(tempNodeList) * 0.3)].trustPoint):
                p = 0.3
            elif (trustPoint <= tempNodeList[int(len(tempNodeList) * 0.4)].trustPoint):
                p = 0.4
            elif (trustPoint <= tempNodeList[int(len(tempNodeList) * 0.5)].trustPoint):
                p = 0.5
            elif (trustPoint <= tempNodeList[int(len(tempNodeList) * 0.6)].trustPoint):
                p = 0.6
            elif (trustPoint <= tempNodeList[int(len(tempNodeList) * 0.7)].trustPoint):
                p = 0.7
            elif (trustPoint <= tempNodeList[int(len(tempNodeList) * 0.8)].trustPoint):
                p = 0.8
            elif (trustPoint <= tempNodeList[int(len(tempNodeList) * 0.9)].trustPoint):
                p = 0.9
            else:
                p = 0.95

        for i in range(maxLimit):
                mean, var  = binom.stats(len(tempNodeList), p)
                result = self.normal_choice(tempNodeList,mean=mean,stddev=math.sqrt(var))
                recommendationList.append(result)
                tempNodeList.remove(result)    
        return recommendationList
        

    def getCurrentState(self):

        results = []
        
        for node in self.nodes:
            avgr = node.ratio[1] / (node.ratio[0]+ node.ratio[1])
            results.append( (node.id, node.trustPoint, node.sended, node.trustState.name, avgr))
        
        #state = pd.DataFrame(self.nodes)

        return results


