from solver import Move
import random
from math import log, sqrt
from pickle import load

def solve(client):
    client.end()
    client.start()
    # Our code begin

    loc = Locate(client)
    bot_locations = loc.find()

    rem = Move(client, bot_locations)
    rem.move()

    # bookkeeping(client)
    # Our code end
    client.end()

class Locate:
    def __init__(self, client):
        self.client = client
        self.g = client.graph
        s = list(range(1, client.students + 1))
        self.all_students = {st: 1 for st in s}
        self.num_students = client.students
        self.num_bots = client.bots
        self.vertices = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))  # non home vertices
        self.bot_locations = set()
        self.bot_count = {v: 0 for v in self.vertices + [self.client.home]}
        self.bot_resp = {}


        # data = load(open("emw_data.p", "rb"))
        # self.epsilon = data["epsilon"] if data["epsilon"] != 0 else sqrt(log(client.students) / len(self.vertices))        self.epsilon = 0.17
        self.epsilon = 0.17
        self.test_size = client.students

    def find(self):
        for vert in self.vertices:
            if vert in self.bot_locations:
                continue
            if self.num_bots != 0:
                self.scout(vert)

        while self.num_bots!=0:
            u = max(self.bot_resp, key = lambda u: self.chance(u))
            student_resp = self.bot_resp.pop(u)
            obs = self.run_remote(u)
            self.update_weights(obs, student_resp)

        return list(self.bot_locations)

    def scout(self, vert):
        r = self.client.scout(vert, list(range(1, self.test_size+1)))
        self.bot_resp[vert] = r

    def update_weights(self, obs, student_resp):
        for student, resp in student_resp.items():
            if resp != obs:
                self.all_students[student] *= 1 - self.epsilon
        factor = self.num_students/sum(self.all_students.values())
        for student in self.all_students:
            self.all_students[student]*=factor

    def chance(self,u):
        student_resp=self.bot_resp[u]
        score=0
        val={False:0, True:1}
        for student, resp in student_resp.items():
            score+=val[resp]*self.all_students[student]
        return score


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
        return flag

    def cheapest_edge(self, vertex):
        adj = self.g.edges(vertex)
        min = float('inf')
        edge = ()
        for (u, v) in adj:
            try:
                weight = self.g.edges[u, v]['weight']
            except:
                continue
            if weight < min:
                min = weight
                edge = (u, v)
        return edge