import networkx as nx
from networkx.algorithms import approximation
import random

def solve(client):
    client.end()
    client.start()
    #Our code begin

    loc = Locate(client)
    bot_locations = loc.find()

    rem = Move(client, bot_locations)
    rem.move()

    # bookkeeping(client)
    #Our code end
    client.end()

class Locate:
    def __init__(self, client):
        self.client = client
        self.g = client.graph
        self.all_students = list(range(1, client.students + 1))
        self.num_bots = client.bots
        self.vertices = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1)) #non home vertices
        self.test_size = min(client.students, 10)

    def find(self):
        scouted = self.scouting()
        bots_left = self.num_bots
        bot_locs = set()
        bot_count = {v:0 for v in self.vertices+[self.client.home]}
        for u in scouted:
            v = self.cheapest_edge(u)[1]
            resp = self.client.remote(u, v)
            if resp>0:
                bot_locs.add(v)
                if u in bot_locs:
                    bot_locs.remove(u)
                if resp>bot_count[u]:
                    bots_left-=resp-bot_count[u]
                bot_count[u]=0
                bot_count[v]+=resp
            if bots_left==0:
                break
        return list(bot_locs)

    def scouting(self): #Returns list of vertices that the bots are likely on
        bot_resp = {}
        for vert in self.vertices:
            r = self.client.scout(vert, random.choices(self.all_students, k=self.test_size))
            bot_resp[vert] = list(r.values()).count(True)
        return sorted(bot_resp, key=bot_resp.get, reverse=True)
        # return heapq.nlargest(int(self.num_bots*1.5), bot_resp, key = bot_resp.get)

    def cheapest_edge(self, vertex):
        adj = self.g.edges(vertex)
        min=float('inf')
        edge=()
        for (u,v) in adj:
            try:
                weight = self.g.edges[u,v]['weight']
            except:
                continue
            if weight<min:
                min = weight
                edge = (u,v)
        return edge


class Move:
    def __init__(self, client, bot_locations):
        self.client=client
        self.home = client.home
        self.g = client.graph
        self.bot_locations = bot_locations

    def move(self): #moves all bots to home
        paths = self.compare()()
        for path in paths:
            self.client.remote(path[0], path[1])

    def naive_path(self): #returns a list of remotes
        return self.build_remote(self.g)

    def steiner_path(self): #returns a list of remotes
        s = approximation.steiner_tree(self.g, self.bot_locations + [self.home])
        unop = self.build_remote(s)
        rem=[]
        for i in range(len(unop)):
            if unop[i] not in unop[i+1:]:
                rem.append(unop[i])
        return rem

    def build_remote(self, graph):
        rem = []
        for vert in self.bot_locations:
            s = nx.shortest_path(graph, vert, self.home, weight="weight")
            for i in range(len(s) - 1):
                rem.append([s[i], s[i + 1]])
        return rem


    def compare(self):
        pathers = [self.steiner_path, self.naive_path]
        costs = {pather: self.path_cost(pather) for pather in pathers}
        return min(costs, key = costs.get)

    def path_cost(self, pather):
        rem = pather()
        return sum([self.g[r[0]][r[1]]["weight"] for r in rem])



def bookkeeping(client):
    print("Time taken: " + str(client.time))
    print(client.bots)
    return
    print(client.cant_scout)
    print(client.bot_count)
    print(client.bot_locations)