import networkx as nx
from networkx.algorithms import approximation
import random
# must explain why we used this
import copy

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
        self.num_students = len(self.all_students)
        self.num_bots = client.bots
        self.vertices = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1)) #non home vertices
        self.test_size = min(client.students, 10)

        self.scouting_data = {}
        self.weights = {}
        self.distribution = {}

        #important stats choices
        self.epsilon = 0.4
        self.proportion_of_testing = 0.85

        self.num_students_to_consider = min(5, int(self.num_students / 2))
        self.threshold_to_call_remote = 0.6

    # should we implement a dictionary such that when a student has been wrong many times, we start to trust them
    # since they can only be wrong so many times? This only matters if we look at every vertex
    def find(self):
        scouted = self.scouting()
        bots_left = self.num_bots
        bot_locs = set()
        bot_count = {v:0 for v in self.vertices+[self.client.home]}

        if self.weights == {} or self.distribution == {}:
            self.weights, self.distribution = self.initialize_mw()

        # important stat choice here
        num_of_remote_calls = int(len(scouted) * self.proportion_of_testing)

        for u in scouted:
            v = self.cheapest_edge(u)[1]
            
            if num_of_remote_calls > 0:
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

                loss_dict = self.update_curr_loss(resp, u)
                self.update_mw(loss_dict)
                num_of_remote_calls -= 1
            else:
                # explain why I used copy.deepcopy
                vertex_data = self.scouting_data.get(u)
                students_by_descending_weights = sorted(self.weights, key=self.weights.get, reverse=True)

                num_of_true = 0
                for i in range(self.num_students_to_consider):
                    if vertex_data.get(students_by_descending_weights[i]) == True:
                        num_of_true += 1

                if float(num_of_true / self.num_students_to_consider) >= self.threshold_to_call_remote:
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

                    loss_dict = self.update_curr_loss(resp, u)
                    self.update_mw(loss_dict)

        return list(bot_locs)

    def update_curr_loss(self, bots_moved, vertex):
        loss_dict = {}
        vertex_data = self.scouting_data.get(vertex)

        if bots_moved == 0:
            for student in vertex_data.keys():
                if vertex_data.get(student) == True:
                    loss_dict[student] = 1
                else:
                    loss_dict[student] = 0

        else:
            for student in vertex_data.keys():
                if vertex_data.get(student) == True:
                    loss_dict[student] = 0
                else:
                    loss_dict[student] = 1

        return loss_dict


    def scouting(self): #Returns list of vertices that the bots are likely on
        bot_resp = {}
        for vert in self.vertices:
            r = self.client.scout(vert, random.choices(self.all_students, k=self.test_size))
            bot_resp[vert] = list(r.values()).count(True)
            self.scouting_data[vert] = r

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

    def initialize_mw(self):
        weights = {}
        distribution = {}
        for student_id in self.all_students:
            weights[student_id] = 1
            distribution[student_id] = float(1 / self.num_students)

        return weights, distribution

    # could simplify exponential stression to improve runtime?
    def update_mw(self, loss_dict):
        #assert len(loss_vector) == self.test_size
        sum_of_weights = 0

        for key in loss_dict.keys():
            new_weight = float(self.weights.get(key) * ((1 - self.epsilon) ** loss_dict.get(key)))
            self.weights[key] = new_weight

            sum_of_weights += new_weight


        # choose statistic --> sum_of_weights as sum of total weights or of only for students used that round>
        #sum_of_weights = sum(self.weights

        for key in loss_dict.keys():
            new_proportion = float(self.weights.get(key) / sum_of_weights)
            self.distribution[key] = new_proportion





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
        shared = self.shared_cost()
        naive = self.naive_cost()
        return self.shared_path if shared<naive else self.naive_path

    def naive_cost(self):
        return sum([nx.shortest_path_length(self.g, vert, self.home, weight="weight") for vert in self.bot_locations])

    def shared_cost(self):
        rem = self.shared_path()
        return sum([self.g[r[0]][r[1]]["weight"] for r in rem])



def bookkeeping(client):
    print("Time taken: " + str(client.time))
    print(client.bots)
    return
    print(client.cant_scout)
    print(client.bot_count)
    print(client.bot_locations)