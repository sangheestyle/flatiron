import sys
import json

import networkx as nx
from networkx.readwrite import json_graph


class DeveloperGraph(object):
    """
    Read repository and convert it into a graph
    """

    def __init__(self):
        self._g = nx.Graph()
        self._projected_graph = None

    @property
    def graph(self):
        return self._g

    @property
    def projected_graph(self):
        return self._projected_graph

    def read_repo(self, repo):
        for commit in repo:
            self._build_graph(commit)

    def _build_graph(self, commit):
        author_email = commit['author_email']
        company = author_email.split('@')[-1]
        self._g.add_node(author_email, bipartite=0, company=company)
        for change in commit['change']:
            if change['filename'].endswith('.java'):
                self._g.add_node(change['filename'], bipartite=1)
                self._g.add_edge(commit['author_email'], change['filename'])
                insertions = 0
                deletions = 0
                if type(change['del']) is int:
                    deletions = change['del']
                if type(change['ins']) is int:
                    insertions = change['ins']
                if ("deletions" not in self._g.node[author_email]) or \
                   ("insertions" not in self._g.node[author_email]):
                    self._g.node[author_email].update({"deletions":deletions})
                    self._g.node[author_email].update({"insertions":insertions})
                else:
                    self._g.node[author_email]["deletions"] += deletions
                    self._g.node[author_email]["insertions"] += insertions

    def project(self, mode=0):
        """
        Make general graph a one-mode projection graph

        Parameters:
            mode: 0 is developer, 1 is file
        """
        top_nodes = set(n for n, d in self._g.nodes(data=True) if d['bipartite'] == mode)
        bottom_nodes = set(self._g) - top_nodes
        self._projected_graph = nx.bipartite.projected_graph(self._g, top_nodes)
        remove = [node for node, degree
                  in self._projected_graph.degree().items()
                  if degree < 1]
        self._projected_graph.remove_nodes_from(remove)

    def write_json(self, output_path):
        d3_formatted = json_graph.node_link_data(self._projected_graph)
        with open(output_path, 'wb') as f:
            json.dump(d3_formatted, f, indent=4)
