from Traversals import bfs_path
import heapq
from collections import deque
from Simulator import Simulator
import sys

class Solution:

    def __init__(self, problem, isp, graph, info):
        self.problem = problem
        self.isp = isp
        self.graph = graph
        self.info = info

    def output_paths(self):
        paths, bandwidths, priorities = {}, {}, {}
        paths = bfs_path(self.graph, self.isp, self.info["list_clients"])
        bandwidths = self.info["bandwidths"]
        temp = sorted(self.info["list_clients"], key=lambda x: self.get_hold(x))
        default_priority = 1
        for client in temp:
            priorities.update({client: default_priority})
            default_priority += 1

        band = {}
        for path in paths.values():
            for node in path:
                if node not in band:
                    band[node] = 1
                else:
                    band[node] = band[node] + 1
                if band[node] > bandwidths[node]:
                    bandwidths[node] = band[node]

        return (paths, bandwidths, priorities)