from solver import Move, solve

def solve(client):
    client.end()
    client.start()
    #Our code begin

    loc = Locate(client)
    bot_locations = loc.find()

    rem = Move(client, bot_locations)
    rem.move()

    print("Time taken: " + str(client.time))
    #Our code end
    client.end()

class Locate():
    def __init__(self, client):
        self.client = client
        self.g = client.graph
        self.all_students = list(range(1, client.students + 1))
        self.num_bots = client.bots
        self.vertices = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))  # non home vertices
        self.test_size = min(client.students, 10)
        self.bot_locations = [] #confirmed bot locations
        self.explored = set()

    def find(self):
        bot_resp = {}
        bots_left = self.num_bots
        for u in self.exploration_set():
            v = self.cheapest_edge(u)[1]
            resp = self.client.remote(u, v)
            if resp > 0:
                self.bot_locations.append(v)
                bots_left-= 1
                if u in self.bot_locations:
                    self.bot_locations.remove(u)
            if bots_left == 0:
                break
        return self.bot_locations


    def exploration_set(self): #vertices left to scout
        while self.explored!=set(self.vertices):
            a = Move(self.client, self.bot_locations)
            rems = a.compare()()
            exception = set()
            for remote in rems:
                exception.add(remote[0])
                exception.add(remote[1])
            e_set= set(self.vertices).difference(exception, self.explored)
            explore = e_set.pop()
            self.explored.add(explore)
            yield explore

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
