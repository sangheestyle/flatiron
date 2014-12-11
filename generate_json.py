import sys
import json
import argparse

import networkx as nx
from networkx.readwrite import json_graph

from repo import Repo


parser = argparse.ArgumentParser(description='Generate node link data to be used by presenter')
parser.add_argument('--g', help="Git repo path", type=str, required=True)
parser.add_argument('--o', help="Output file name", type=str, required=True)
args = parser.parse_args()

git_dir_path = args.g
output_file = args.o

r = Repo()
r.read_repo(git_dir_path, 2)
g = nx.Graph()
for commit in r:
    author_email = commit['author_email']
    company = author_email.split('@')[-1]
    g.add_node(author_email, bipartite=0, company=company)
    for change in commit['change']:
        if change['del'] > 0 and change['ins'] > 0:
            g.add_node(change['filename'], bipartite=1)
            g.add_edge(commit['author_email'], change['filename'])
            insertions = 0
            deletions = 0
            if type(change['del']) is int:
                deletions = change['del']
            if type(change['ins']) is int:
                insertions = change['ins']
            if ("deletions" not in g.node[author_email]) or \
               ("insertions" not in g.node[author_email]):
                g.node[author_email].update({"deletions":deletions})
                g.node[author_email].update({"insertions":insertions})
            else:
                g.node[author_email]["deletions"] += deletions
                g.node[author_email]["insertions"] += insertions
top_nodes = set(n for n, d in g.nodes(data=True) if d['bipartite'] == 0)
bottom_nodes = set(g) - top_nodes
dev_graph = nx.bipartite.projected_graph(g, top_nodes)
remove = [node for node, degree
          in dev_graph.degree().items()
          if degree < 1]
dev_graph.remove_nodes_from(remove)
print "Number of vertices:", len(dev_graph)
d3_formatted = json_graph.node_link_data(dev_graph)
with open(output_file, 'wb') as f:
    json.dump(d3_formatted, f, indent=4)
