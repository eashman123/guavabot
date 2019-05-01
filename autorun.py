import os, sys
from statistics import mean, stdev
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

def compare(n, *args):
    '''
    Compares n different solvers
    :param n: Number of tests to run for each solver
    :param args: Names of solver
    :return: None; prints out score of best Solver
    '''
    total_tests = int(n)
    scores= {solver: test(n, solver) for solver in args}
    best = max(scores, key=lambda s: scores[s][0])
    print("Best Solver: " + best)
    print("Average: " + str(scores[best][0]))
    print("Standard Deviation: " + str(scores[best][1]))

def optimize_mw(solver):
    '''
    Optimize solver
    :param solver: Name of solver
    :return: None; prints out best values in test
    '''
    if solver=='emw_solver':
        performance={}
        data = {"epsilon": 0.6, "thresh" : 1.0}
        for i in range(10,21):
            data["test_size"] = i
            pickle.dump(data, open("emw_data.p", "wb"))
            m,s = test(100, solver=solver)
            print(pickle.load(open("emw_data.p", "rb" )))
            performance[i] = (m,s)
        p.terminate()
        best = max(performance.keys(), key = lambda k: performance[k][0])
        data = data = {"epsilon": 0.6, "test_size": best, "thresh": 1.0}
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
    arguments = sys.argv[1:]
    mapping = {'test':test, 'compare':compare, 'optimize_mw':optimize_mw}
    f = mapping[arguments.pop(0)]
    f(*arguments)