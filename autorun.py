import os, sys
from statistics import mean, stdev

def test(n=30, teval=False):
    scores=[]
    for i in range(n):
        score = float(os.popen("python client.py --solver solver").readlines()[-1].split()[-1])
        print(score)
        scores.append(score)
    evaluated_scores = sorted(scores)[int(len(scores)*.12):]
    if teval:
        scores=evaluated_scores
    print("Average: " + str(mean(scores)))
    print("Standard Deviation: " + str(stdev(scores)))

if __name__=="__main__":
    arguments = sys.argv
    if len(arguments)==1:
        test(30, True)
    else:
        assert len(arguments)==2, "Must only include 1 argument"
        test(int(arguments[1]))
