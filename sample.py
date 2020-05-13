import pandas as pd
import numpy as np
import random
import sys
import collections
import math
from operator import itemgetter
import operator
#read queries.txt
def readQueries(filename):
    queries = pd.read_csv(filename,header=None, names=['Queries'])
    queries = [line.strip() for line in queries['Queries'].values]
    return queries

#read bidder_dataset.csv
def readBidder(filename):
    bidder = []
    file = open(filename)
    for line in file:
        l = []
        l = line.strip().split(",")
        bidder.append(l)
    file.close()
    return bidder

#convert bidder to dict with keyword and budget
def convertBidderToDict(bidder):
    dictBidder = dict()
    AdvBudget = dict()
    AdvNeighbour = collections.defaultdict(list)
    NumBid = dict()
    sum = 0
    for row in bidder:
        if row[3] != 'Budget':
            AdvNeighbour[row[1]].append(int(row[0]))
        if row[3] != "" and row[3] != 'Budget':
            dictBidder[row[1]]=row[3]
            AdvBudget[int(row[0])] = int(row[3])
            sum = sum + int(row[3])
            NumBid[int(row[0])] = float(row[2])
    return dictBidder,sum,AdvBudget,AdvNeighbour,AdvBudget,NumBid

#creating a dict with bidder and bid placed
def convertBidDict1(queries):
    bidder = pd.read_csv("bidder_dataset.csv")
    queryDict = dict()
    for query in queries:
        if query not in queryDict.keys():
            x = bidder.loc[(bidder.Keyword == query)]
            y = x.sort_values(by='Budget', ascending=False)
            a = [i for i in y.values.tolist()]
            queryDict[query] = a
    return queryDict


def calculate_psi(queryDict, AdvBid,AdvTotalNochange):
    psiDict = {}
    for x in queryDict:
        if AdvTotalNochange[x[0]] == 0:
            continue
        xu = round(((AdvTotalNochange[x[0]]-float(AdvBid[x[0]]))/AdvTotalNochange[x[0]]))
        psi_xu = 1 - pow(math.e, (xu - 1))
        psiDict[x[0]] = psi_xu*x[2]
    psiDict = sorted(psiDict.items(), key=operator.itemgetter(1),reverse=True)
    return psiDict

#msvv Algorithm
def msvv(queries,queryDict,totalBudget,AdvBid,AdvNeighbour,AdvTotalNochange,NumBid):
    res = 0
    total_revenue = 0

    for i in range(100):
        revenue = 0
        for q in queries:
            if q in queryDict.keys():
                psiDict = calculate_psi(queryDict[q],AdvBid,AdvTotalNochange)
                for b in psiDict:
                    if b[0] in AdvNeighbour[q]:
                        if float(AdvBid[b[0]])< float(NumBid[b[0]]):
                            continue
                        else:
                            revenue = revenue + float(NumBid[b[0]])
                            AdvBid[b[0]] = float(AdvBid[b[0]]) - float(NumBid[b[0]])
                            if float(AdvBid[b[0]])<=0:
                                AdvNeighbour[q].remove(b[0])
                            break
        total_revenue = total_revenue + revenue
    return total_revenue




queries = readQueries("queries.txt")
bidder = readBidder("bidder_dataset.csv")
dictBidder,totalBudget,AdvBudget,AdvNeighbour,AdvTotalNochange,NumBid = convertBidderToDict(bidder)
queryDict = convertBidDict1(queries)
random.seed(0)
revenue = msvv(queries,queryDict,totalBudget,AdvBudget,AdvNeighbour,AdvTotalNochange,NumBid)
print(revenue)
print(revenue/totalBudget)
