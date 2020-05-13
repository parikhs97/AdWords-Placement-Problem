import pandas as pd
import numpy as np
import random
import sys
import collections
import math
from operator import itemgetter

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
    sum = 0
    for row in bidder:
        if row[3] != 'Budget':
            AdvNeighbour[row[1]].append(int(row[0]))
        if row[3] != "" and row[3] != 'Budget':
            dictBidder[row[1]]=row[3]
            AdvBudget[int(row[0])] = int(row[3])
            sum = sum + int(row[3])
    return dictBidder,sum,AdvBudget,AdvNeighbour

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


#balance Algorithm
def balance(queries,queryDict,totalBudget,AdvBid,AdvNeighbour):
    res = 0
    total_revenue = 0

    for i in range(1):
        revenue = 0
        for q in queries:
            if q in queryDict.keys():
                sorted(queryDict[q], key=lambda x: x[3],reverse=True)
                for b in queryDict[q]:
                    if b[0] in AdvNeighbour[b[1]]:
                        if AdvBid[b[0]]<float(b[2]):
                            continue
                        else:
                            revenue = revenue + float(b[2])
                            AdvBid[b[0]] = float(AdvBid[b[0]]) - float(b[2])
                            b[3] = float(b[3]) - float(b[2])
                            # if AdvBid[b[0]]<=0:
                            #     AdvNeighbour[b[1]].remove(b[0])
                            break


        total_revenue = total_revenue + revenue
    return total_revenue




queries = readQueries("queries.txt")
bidder = readBidder("bidder_dataset.csv")
dictBidder,totalBudget,AdvBudget,AdvNeighbour = convertBidderToDict(bidder)
queryDict = convertBidDict1(queries)
random.seed(0)
revenue = balance(queries,queryDict,totalBudget,AdvBudget,AdvNeighbour)
print(revenue)
print(revenue/totalBudget)
