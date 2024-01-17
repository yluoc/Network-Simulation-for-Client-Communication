from Objects import Node, Client, Packet
from LinkedList import LinkedList
from collections import deque, defaultdict

class Simulator:

    def __init__(self):
        """
        Constructor
        """

    def validate_edge(self, node1, node2):
        return node1.id in node2.neighbors

    def local_bfs_path(self, graph, isp, list_clients):

        paths = {}

        graph_size = len(graph)
        priors = [-1]*graph_size
        search_queue = deque()
        search_queue.append(isp)

        while search_queue:
            node = search_queue.popleft()
            for neighbor in graph[node]:
                if (priors[neighbor] == -1 and neighbor != isp):
                    priors[neighbor] = node
                    search_queue.append(neighbor)

        for client in list_clients:
            path = []
            current_node = client
            while (current_node != -1):
                path.append(current_node)
                current_node = priors[current_node]
            path = path[::-1]
            paths[client] = path

        return paths

    def run(self, graph, isp, list_clients, paths, bandwidths, priorities, is_rural):
        """
        Runs the simulation based on the paths provided in Solution.py
        """
        shortest_paths = self.local_bfs_path(graph, isp, list_clients)

        packets = {c: Packet(c, paths[c]) for c in list_clients}

        self.clients = {
            c: Client(c, paths[c], packets[c], bandwidths[c], set(graph[c]), is_rural[c] if is_rural else False) for c in list_clients}

        nodes = {u: Node(u, bandwidths[u], set(graph[u])) for u in graph}

        if priorities:
            list_clients = sorted(
                list_clients, key=lambda client: priorities[client], reverse=True)

        active = set()

        list_clients = LinkedList(list_clients)

        while list_clients.size > 0:

            current = list_clients.begin()

            while current != list_clients.end():

                packet = packets[current.id]

                if not packet.path or packet.path[0] != isp:
                    receiving_client = self.clients[packet.client]
                    receiving_client.delay = float("inf")
                    list_clients.remove(current.id)
                    continue

                current_node = nodes[packet.path[packet.location]]

                if packet.location == len(packet.path) - 1:

                    if current_node.id == packet.client and packet.location >= len(shortest_paths[packet.client])-1:
                        receiving_client = self.clients[packet.client]
                        receiving_client.delay = packet.delay
                    else:
                        receiving_client.delay = float("inf")
                    list_clients.remove(current.id)
                    current = current.next
                    continue

                packet.delay += 1

                if current_node.bandwidth > 0:
                    active.add(current_node)
                    current_node.bandwidth -= 1
                    packet.location += 1
                    if not self.validate_edge(current_node, nodes[packet.path[packet.location]]):
                        list_clients.remove(packet.client)
                        self.clients[packet.client].delay = float("inf")

                current = current.next

            for node in active:
                node.bandwidth = bandwidths[node.id]
            active.clear()

    def get_delays(self, list_clients):
        return {client: self.clients[client].delay for client in list_clients}

    def get_clients(self, list_clients):
        return {client: self.clients[client] for client in list_clients}
