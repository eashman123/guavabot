import os, sys
from statistics import mean, stdev
from math import sqrt

def test(n, solver="solver", teval=False):
    teval = True if arguments[3]=='True' else False
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
    mean1, stdev1 = test(total_tests//2, solver1)
    mean2, stdev2 = test(total_tests//2, solver2)
    dstdev = sqrt(pow(stdev1,2)-pow(stdev2, 2))
    print("D Average: " + str(mean1-mean2))
    print("D Standard Deviation: " + str(dstdev))

def oprtimize_mw(solver):
    #https://wiki.python.org/moin/UsingPickle - have solver load values from file, edit file in between iterations
    if (solver=='emw_solver'):
        pass
    if solver=='mw_solver':
        pass

if __name__=="__main__":
    arguments = sys.argv
    mapping = {'test':test, 'compare':compare, 'optimize_mw':oprtimize_mw}
    f = mapping[arguments.pop(1)]
    if len(arguments)==2:
        f(int(arguments[1]))
    elif len(arguments)==3:
        f(int(arguments[1]), arguments[2])
    elif len(arguments)==4:
        f(int(arguments[1]), arguments[2], arguments[3])