import sys
import json
import networkx as nx
from networkx.readwrite import json_graph
from repo import Repo

git_dir_path = sys.argv[1]
output_file = sys.argv[2]

r = Repo()
r.read_repo(git_dir_path, 5)
g = nx.Graph()
for commit in r:
    for change in commit['change']:
        g.add_node(commit['author_email'], bipartite=0)
        g.add_node(change['filename'], bipartite=1)
        g.add_edge(commit['author_email'], change['filename'])
top_nodes = set(n for n, d in g.nodes(data=True) if d['bipartite'] == 0)
bottom_nodes = set(g) - top_nodes
dev_graph = nx.bipartite.projected_graph(g, top_nodes)
remove = [node for node, degree
          in dev_graph.degree().items()
          if degree == 0]
dev_graph.remove_nodes_from(remove)
d3_formatted = json_graph.node_link_data(dev_graph)
with open(output_file, 'wb') as f:
    json.dump(d3_formatted, f, indent=4)
