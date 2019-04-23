from local_server import *
import argparse

if __name__=="__main__":
    instances = ["toronto_12_17"]
    for inst in instances:
        parser = argparse.ArgumentParser(description='Guavabot local server: move all bots home!')
        parser.add_argument('--instance', dest='instance_name', default=inst,
                        help='The local instance to always serve.')
        args = parser.parse_args()

        instance_name = args.instance_name

        app.run(debug=True)

