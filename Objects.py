class Node:

    """
    Parent class for the router and the client
    """

    def __init__(self, identifier, bandwidth=float("inf"), neighbors = set()):

        self.id = identifier
        self.bandwidth = bandwidth
        self.neighbors = neighbors

    def __repr__(self):
        return "{}(ID: {}, bandwidth: {})".format(self.__class__.__name__, self.id, self.bandwidth)


class Client(Node):

    def __init__(self, identifier, path, packet, bandwidth, neighbors, is_rural=False):

        super(Client, self).__init__(identifier, bandwidth, neighbors)

        self.delay = 0
        self.delay_optimal = 1
        self.path = path
        self.packet = packet
        self.is_rural = is_rural
        self.has_received = False

    def __repr__(self):
        return "{}(ID: {}, bandwidth: {}, path: {}, packet: {}, is_rural: {}, has_received: {})".format(self.__class__.__name__, self.id, self.bandwidth, self.path, self.packet, self.is_rural, self.has_received)


class Packet:

    """
    Packet object, not actually "forwarded" in the technical sense of the word
    but its location variable helps keep track of how far along in its path it is
    """

    def __init__(self, client, path, priority=0):

        self.client = client
        self.delay = 0
        self.location = 0
        self.priority = priority
        self.path = path

    def __repr__(self):
        return "{} (Client: {}, Delay: {}, Location: {}, Priority: {}, Path: {})".format(self.__class__.__name__, self.client, self.delay, self.location, self.priority, self.path)
