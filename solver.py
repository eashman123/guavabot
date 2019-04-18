import networkx as nx
from matplotlib import pyplot as plt
import random, heapq

def solve(client):
    client.end()
    client.start()
    #Our code begin

    loc = Locate(client)
    bot_locations = loc.find()

    rem = Move(client, bot_locations)
    rem.move()

    bookkeeping(client)
    #Our code end
    client.end()

class Locate:
    def __init__(self, client):
        self.client = client
        self.all_students = list(range(1, client.students + 1))
        self.num_bots = client.bots
        self.vertices = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1)) #non home vertices

    def find(self): #Returns list of vertices that the bots are likely on
        bot_resp = {}
        for vert in self.vertices:
            r = self.client.scout(vert, self.all_students)
            bot_resp[vert] = list(r.values()).count(True)
        return heapq.nlargest(int(self.num_bots*1.5), bot_resp, key = bot_resp.get)


class Move:
    def __init__(self, client, bot_locations):
        self.client=client
        self.home = client.home
        self.g = client.graph
        self.vertices = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))
        self.bot_locations = bot_locations

    def move(self): #moves all bots to home
        for vert in self.bot_locations:
            path = nx.shortest_path(self.g, vert, self.home, weight="weight")
            for i in range(len(path)-1):
                print(self.client.remote(path[i], path[i+1]))


def bookkeeping(client):
    print("Time taken: " + str(client.time))
    return
    print(client.cant_scout)
    print(client.bot_count)
    print(client.bot_locations)