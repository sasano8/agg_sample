import hashlib
import json
from time import time


class GraphManager:
    ...


class BlockChainNetwork:
    def __init__(self):
        self.nodes = set()

    def append(self, node):
        ...

    def leave(self, node):
        ...


class BlockChainNetworkNode:
    def recieve(self, block):
        ...

    def consent(self):
        ...


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
