import os, sys
from statistics import mean, stdev
from math import sqrt
import pickle

def test(n, solver="solver", teval=False):
    n = int(n)
    teval = True if teval=='True' else False
    scores=[]
    for i in range(n):
        score = float(os.popen("python client.py --solver {}".format(solver)).readlines()[-1].split()[-1])
        print(score)
        scores.append(score)
    evaluated_scores = sorted(scores)[int(len(scores)*.12):]
    if teval:
        scores=evaluated_scores
    print("Average: " + str(mean(scores)))
    print("Standard Deviation: " + str(stdev(scores)))
    return mean(scores), stdev(scores)

def compare(total_tests, solver1, solver2):
    total_tests = int(total_tests)
    mean1, stdev1 = test(total_tests//2, solver1)
    mean2, stdev2 = test(total_tests//2, solver2)
    dstdev = sqrt(abs(pow(stdev1,2)-pow(stdev2, 2)))
    print("D Average: " + str(mean1-mean2))
    print("D Standard Deviation: " + str(dstdev))

def oprtimize_mw(solver):
    #https://wiki.python.org/moin/UsingPickle - have solver load values from file, edit file in between iterations
    if (solver=='emw_solver'):
        performance={}
        epsilon = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
        thresh = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
        for ep in epsilon:
            for th in thresh:
                data = {"thresh":th, "epsilon":ep}
                m,s = test(30, solver=solver)
                performance[(ep,th)] = (m,s)
        best = max(performance.keys(), key = lambda k: performance[k][0])
        print("Best Values: " + str(best))
        print("Performance: " + str(performance[best]))

    if solver=='mw_solver':
        pass

if __name__=="__main__":
    arguments = sys.argv
    mapping = {'test':test, 'compare':compare, 'optimize_mw':oprtimize_mw}
    f = mapping[arguments.pop(1)]
    if len(arguments)==2:
        f(arguments[1])
    elif len(arguments)==3:
        f(arguments[1], arguments[2])
    elif len(arguments)==4:
        f(arguments[1], arguments[2], arguments[3])