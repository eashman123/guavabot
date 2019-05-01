import os
from statistics import mean, stdev
from multiprocessing import Process
import pickle

def run_server(n):
    os.system("python my_server.py {}".format(n))

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

def optimize_mw(solver):
    '''
    Optimize solver
    :param solver: Name of solver
    :return: None; prints out best values in test
    '''
    if solver=='emw_solver':
        performance={}
        n = 100
        p = Process(target=run_server, args=(n,))
        p.start()

        epsilon = [0]
        thresh = [i/10 for i in range(5,11)]
        test_size = list(range(10,41))
        for ep in epsilon:
            for th in thresh:
                for t in test_size:
                    data = {"epsilon": ep, "thresh": th, "test_size": t}
                    pickle.dump(data, open("emw_data.p", "wb"))
                    print(pickle.load(open("emw_data.p", "rb")))
                    m, s = test(n, solver=solver)
                    performance[(ep,th,t)] = (m, s)
        p.terminate()
        ep,th,t = max(performance.keys(), key = lambda k: performance[k][0])
        data = {"epsilon": ep, "thresh": th, "test_size": t}
        pickle.dump(data, open("emw_data.p", "wb"))
        print("Best Values: " + str(data))
        print("Performance: " + str(performance[(ep, th, t)]))

    if solver=='mw_solver':
        pass
    while(True):
        pass

optimize_mw("emw_solver")