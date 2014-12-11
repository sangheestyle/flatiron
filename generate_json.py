import sys
import argparse

from repo import Repo
from developer_graph import DeveloperGraph


parser = argparse.ArgumentParser(description='Generate node link data to be used by presenter')
parser.add_argument('--g', help="Git repo path", type=str, required=True)
parser.add_argument('--o', help="Output file name", type=str, required=True)
parser.add_argument('--m', help="Past n month", type=str, required=True)
args = parser.parse_args()

git_dir_path = args.g
output_file = args.o

r = Repo()
r.read_repo(git_dir_path, args.m)
dev_graph = DeveloperGraph()
dev_graph.read_repo(r)
dev_graph.project()
print "Number of vertices:", len(dev_graph.projected_graph)
dev_graph.write_json(args.o)
