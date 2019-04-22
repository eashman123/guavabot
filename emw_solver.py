from solver import Move
import networkx as nx
import random
from math import log, sqrt
import pickle

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
        s = list(range(1, client.students + 1))
        self.all_students = {st:1 for st in s}
        self.num_bots = client.bots
        self.vertices = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))  # non home vertices
        self.bot_locations = set()
        self.bot_count = {v:0 for v in self.vertices+[self.client.home]}
        self.test_size = self.set_test_size(client.students)
        epsilon = sqrt(log(client.students)/len(self.vertices))
        self.bot_resp = {}

        data = pickle.load(open("emw_data.p", "rb"))
        self.epsilon = data["epsilon"] if data["epsilon"]!=0 else epsilon
        self.thresh= data["thresh"]

    def find(self):
        for vert in self.vertices:
            if vert in self.bot_locations:
                continue
            if self.num_bots!=0:
                self.scout(vert)
        scouted = sorted(self.bot_resp, key=self.bot_resp.get, reverse=True)
        for u in scouted:
            if self.num_bots==0:
                break
            self.run_remote(u)
        return list(self.bot_locations)


    def scout(self, vert):
        test_size = self.get_test_size()
        r = self.client.scout(vert, self.choices(list(self.all_students.keys()), test_size))
        self.bot_resp[vert] = list(r.values()).count(True)
        if self.bot_resp[vert] > int(self.thresh*test_size):
            self.update_weights(vert, r)

    def update_weights(self, u, student_resp):
        del self.bot_resp[u]
        flag = self.run_remote(u)
        for student, resp in student_resp.items():
            if resp != flag:
                self.all_students[student] *= 1-self.epsilon

    def run_remote(self, u):
        v = self.cheapest_edge(u)[1]
        resp = self.client.remote(u, v)
        flag = False
        if resp > 0:
            self.bot_locations.add(v)
            if u in self.bot_locations:
                self.bot_locations.remove(u)
            if resp > self.bot_count[u]:
                flag = True
                self.num_bots -= resp - self.bot_count[u]
            self.bot_count[u] = 0
            self.bot_count[v] += resp

    def set_test_size(self, num_students, default=10):
        v = len(self.vertices)
        # return [min(10, num_students) for _ in range(v)]
        interval = (num_students-min(10, num_students/2))/v
        c = min(10, num_students/2)
        l = []
        for _ in range(v):
            l.append(round(c))
            c+=interval
        return l

    def get_test_size(self):
        return self.test_size.pop()

    def choices(self, population, k=1, weights=None,):
        if weights==None:
            weights=list(self.all_students.values())
            print(weights)
        a = set()
        while len(a)!=k:
            temp = random.choices(population, weights=weights, k=k-len(a))
            a.update(temp)
        return list(a)

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