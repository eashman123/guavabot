import networkx as nx
from networkx.algorithms import approximation
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
        paths = self.compare()()
        for path in paths:
            self.client.remote(path[0], path[1])

    def naive_path(self): #returns a list of remotes
        rem = []
        for vert in self.bot_locations:
            s = nx.shortest_path(self.g, vert, self.home, weight="weight")
            for i in range(len(s)-1):
                rem.append([s[i], s[i+1]])
        return rem

    def shared_path(self): #returns a list of remotes
        s = approximation.steiner_tree(self.g, self.bot_locations + [self.home])
        unop = []
        for vert in self.bot_locations:
            sh = nx.shortest_path(s, vert, self.home, weight="weight")
            for i in range(len(sh)-1):
                unop.append([sh[i], sh[i+1]])
        rem=[]
        for i in range(len(unop)):
            if unop[i] not in unop[i+1:]:
                rem.append(unop[i])
        return rem

    def compare(self):
        shared = float('inf')
        shared = self.shared_cost()
        naive = self.naive_cost()
        print(naive, shared)
        return self.shared_path if shared<naive else self.naive_path

    def naive_cost(self):
        return sum([nx.shortest_path_length(self.g, vert, self.home, weight="weight") for vert in self.bot_locations])

    def shared_cost(self):
        rem = self.shared_path()
        return sum([self.g[r[0]][r[1]]["weight"] for r in rem])



def bookkeeping(client):
    print("Time taken: " + str(client.time))
    return
    print(client.cant_scout)
    print(client.bot_count)
    print(client.bot_locations)