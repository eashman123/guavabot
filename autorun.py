import os, sys
from statistics import mean, stdev
from math import sqrt
import pickle

def test(n, solver="solver", teval='True'):
    '''
    Runs n tests of solver
    :param n: Number of tests
    :param solver: Solver to sun
    :param teval: True if you want to drop lowest 12%
    :return: Tuple (Average Score, S.D. of Scores)
    '''
    n = int(n)
    teval = True if teval=='True' else False
    if teval:
        print("Dropping lowest 12%...")
    else:
        print("Scores Lives Matter")
    scores=[]
    for i in range(n):
        score = float(os.popen("python client.py --solver {}".format(solver)).readlines()[-1].split()[-1])
        print("Run " + str(i+1) + ": " + str(score))
        scores.append(score)
    evaluated_scores = sorted(scores)[int(len(scores)*.12):]
    if teval:
        scores=evaluated_scores
    print("Average: " + str(mean(scores)))
    print("Standard Deviation: " + str(stdev(scores)))
    return mean(scores), stdev(scores)

def compare(total_tests, solver1, solver2):
    '''
    Compares two different solvers
    :param total_tests: Number of tests to run. Will run total_tests/2 tests for each solver
    :param solver1: Name of one solver
    :param solver2: Name of other solver
    :return: None; prints out Difference in average score and S.D.
    '''
    total_tests = int(total_tests)
    mean1, stdev1 = test(total_tests//2, solver1)
    mean2, stdev2 = test(total_tests//2, solver2)
    dstdev = sqrt(abs(pow(stdev1,2)-pow(stdev2, 2)))
    print("D Average: " + str(mean1-mean2))
    print("D Standard Deviation: " + str(dstdev))

def oprtimize_mw(solver):
    '''
    Optimize solver
    :param solver: Name of solver
    :return: None; prints out best values in test
    '''
    if solver=='emw_solver':
        performance={}
        data = {"epsilon": 0, "test_size" : 20}
        thresh = [b/10 for b in range(5,11)]
        for i in thresh:
            data["thresh"] = i
            pickle.dump(data, open("emw_data.p", "wb"))
            m,s = test(100, solver=solver)
            print(pickle.load(open("emw_data.p", "rb" )))
            performance[i] = (m,s)
        best = max(performance.keys(), key = lambda k: performance[k][0])
        data = data = {"epsilon": 0.6, "test_size": 20, "thresh": best}
        pickle.dump(data, open("emw_data.p", "wb"))
        print("Best Values: " + str(data))
        print("Performance: " + str(performance[best]))

    if solver=='mw_solver':
        pass

if __name__=="__main__":
    '''
    Command: python autorun.py function *args
    This runs the function with the associated arguments.
    E.g. python autorun.py test 30 emw_solver
    This runs 30 tests of emw_solver
    '''
    arguments = sys.argv
    mapping = {'test':test, 'compare':compare, 'optimize_mw':oprtimize_mw}
    f = mapping[arguments.pop(1)]
    if len(arguments)==2:
        f(arguments[1])
    elif len(arguments)==3:
        f(arguments[1], arguments[2])
    elif len(arguments)==4:
        f(arguments[1], arguments[2], arguments[3])