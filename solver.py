import networkx as nx
import random

def solve(client):
    client.end()
    client.start()
    #Our code begin


    loc = Locate(client)
    loc.find()

    rem = Move(client)
    rem.move()


    #Our code end
    client.end()

class Locate:
    def __init__(self, client):
        self.all_students = list(range(1, client.students + 1))
        self.num_bots = client.bots
        self.vertices = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))

    def find(self): #Finds location of all bots
        pass

class Move:
    def __init__(self, client):
        self.home = client.home
        self.vertices = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))

    def move(self): #moves all bots to home
        pass