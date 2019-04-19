import os, sys

def test(n):
    sum=0
    for i in range(n):
        score = float(os.popen("python client.py --solver solver").readlines()[-1].split()[-1])
        sum+=score
        print(score)
    print("Average: " + str(sum/n))

if __name__=="__main__":
    arguments = sys.argv
    assert len(arguments)==2, "Must only include 1 argument"
    assert isinstance(int(arguments[1]), int), "Must only be a number"
    test(int(arguments[1]))
