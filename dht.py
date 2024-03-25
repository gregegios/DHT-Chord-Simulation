import random
from node import Node
import config
from hash import *
import time

class DHT:

    def __init__(self):
        self.nodeDict = {}
        self.nodeNum = 0
        self.hopsOfFindSuccessor = []

    # random id assignment
    def get_id(self):
        id = hash_data(random.randint(0, 2 **N ))

        while True:
            if id in self.nodeDict:
                id = hash_data(random.randint(0, 2 ** N))
            else:
                break
        return id

    # Adds node
    def join(self):

        start_time = time.time()  #xronometrhsh


        #elegxos oti den einai gemato to net
        if self.nodeNum >= 2 ** N:
            print(
                "Cannot add another node in the network because it reached maximum capacity -> 2**N ")
            quit()
        newNode = Node(self.get_id())
        #dhmiourgia prwtou node se periptwsh pou einai adeio to dyktio
        if self.nodeNum == 0:
            self.nodeDict[newNode.ID] = newNode
            # print(f"Joined: {self.nodeDict[newNode.ID]}")

        #deftero node
        elif self.nodeNum == 1:
            otherID = random.choice(list(self.nodeDict.keys()))
            # Update succsessor and predecessor of the other node
            self.nodeDict[otherID].pre = newNode.ID
            self.nodeDict[otherID].suc = newNode.ID
            self.nodeDict[otherID].fingerTable[0] = newNode.ID

            # Update succsessor kai predecessor tou New Node
            newNode.suc = otherID
            newNode.fingerTable[0] = otherID
            newNode.pre = otherID
            self.nodeDict[newNode.ID] = newNode


        # join node se periptwsh pou arithmos twn node sto dyktio panw apo 2
        else:
            randID = random.choice(list(self.nodeDict.keys()))
            sucNode = self.findSuccessor(self.nodeDict[randID], newNode.ID)
            newNode.suc = sucNode.ID
            newNode.fingerTable[0] = sucNode.ID

            # enhmerwsh successor
            self.notify(newNode)
            # prosthesh tou neou node
            self.nodeDict[newNode.ID] = newNode

            self.stabilize()

        # auxhsh sunmolou twn nodes me 1
        self.nodeNum += 1


        end_time = time.time()  # xronometrhsh arxh
        elapsed_time = end_time - start_time

        # print(f"Time taken for join: {elapsed_time} seconds")

    def nodeFailure(self):
        randID = random.choice(list(self.nodeDict.keys()))
        self.nodeDict.pop(randID)

    def removeNodeSafely(self):
        # epilogh tyxaiou node
        randID = random.choice(list(self.nodeDict.keys()))
        deletedNode = self.nodeDict[randID]
        self.nodeDict[deletedNode.pre].suc = deletedNode.suc
        self.nodeDict[deletedNode.pre].fingerTable[0] = deletedNode.suc

        self.nodeDict[deletedNode.suc].pre = deletedNode.pre

        self.nodeDict[deletedNode.suc].transfer_hash_table(
            deletedNode.hashTable)

        self.nodeDict.pop(randID)
        self.stabilize()

        self.nodeNum -= 1
        print("Deleted Node: ", randID)

    def notify(self, node):
        self.nodeDict[node.suc].pre = node.ID

    # statheropoiohsh enos node
    def stabilizeNode(self, node):
        if self.nodeDict[node.suc].pre != node.ID:
            node.suc = self.nodeDict[node.suc].pre
            self.nodeDict[node.suc].pre = node.ID

    # satatheropihsh gia olla ta nodes
    def stabilize(self):
        for item in self.nodeDict.items():
            self.stabilizeNode(item[1])

    # anazhthsh successor
    def findSuccessor(self, node, key, recordHops=False):
        currentNode = node
        hops = 0
        count = 0

        while True:

            if currentNode.pre is not None and between(currentNode.pre, currentNode.ID, key):
                if count != 0:
                    hops += 1
                if recordHops == True:
                    self.hopsOfFindSuccessor.append(hops)
                return self.nodeDict[currentNode.ID]
            else:  
                for i in range(N-1, 0, -1):
                    try:
                        if currentNode.fingerTable[i] is not None and not between(currentNode.ID, currentNode.fingerTable[i], key):
                            currentNode = self.nodeDict[currentNode.fingerTable[i]]
                            hops += 1
                            break
                    except:
                        continue
                currentNode = self.nodeDict[currentNode.suc]
                count += 1

    def fix_finger(self, node, i):
        ith_finger = (node.ID + 2**i) % 2**N
        node.fingerTable[i] = self.findSuccessor(node, ith_finger).ID

    def fix_all_fingers_of_node(self, node):
        for i in range(0, N):
            self.fix_finger(node, i)

    def fix_all_fingers_of_all_nodes(self):
        for pair in self.nodeDict.items():
            for i in range(0, N):
                self.fix_finger(pair[1], i)


    def insert_key_value_pair(self, key, value):
        randNodeID = random.choice(list(self.nodeDict.keys()))
        targetNode = self.findSuccessor(self.nodeDict[randNodeID], key)
        targetNode.save_key_value_pair(key, value)
        return targetNode

    def insert_values(self, value, hashedValue):
        for i, j in zip(hashedValue, value):
            self.insert_key_value_pair(i, j)

    def delete_pair(self, key):
        randID = random.choice(list(self.nodeDict.keys()))
        node = self.findSuccessor(self.nodeDict[randID], key)
        if node.hashTable[key] is not None:
            node.hashTable.pop(key)
            return True
        return False

    def print(self):
        for item in self.nodeDict.items():
            print(item[1])

    def print_density(self):
        network = ["_"] * 2**N
        for id in self.nodeDict:
            network[id] = "#"
        print("".join(network))

    def search_ft(self, id):
        for node in self.nodeDict:
            for finger in self.nodeDict[node].fingerTable:
                if finger == id:
                    return "ID Found in a finger tables"
        return "Finger NOT Found in finger Tables"

    def search_ft_none(self):
        for node in self.nodeDict:
            for finger in self.nodeDict[node].fingerTable:
                if finger is None:
                    return "there is a none value in fingertables"
        return "no None value found in finger tables"


def between(ID1, ID2, key):
    if ID1 == ID2:
        return True
    wrap = ID1 > ID2 
    if not wrap:
        return True if key > ID1 and key <= ID2 else False
    else:
        return True if key > ID1 or key <= ID2 else False

#####################################################
    
dht = DHT()

for i in range(0, nodes):
    dht.join()
  
print("Number of nodes in the network: ", dht.nodeNum)

dht.removeNodeSafely()  
print("Number of nodes in the network: ", dht.nodeNum)

dht.fix_all_fingers_of_all_nodes()

dht.insert_values(data, hashedData)

# random_node = list(dht.nodeDict.items())[0][1]
# print("Hash table of a random node: ", random_node.ID)
# print(random_node.print_hash_table())
# print("Finger table of a random node: ")
# print(random_node.print_finger_table())


# print("Search for a key in the network")
randKey = hash_data('Cornell University')
randID = random.choice(list(dht.nodeDict.keys()))
# print("Key: ", randKey)
# print("Node: ", randID)
node_with_key = dht.findSuccessor(dht.nodeDict[randID], randKey).ID
# print("Node with key: ", node_with_key)

# print("Hash table of node with key")
# print(dht.nodeDict[node_with_key].hashTable)
ht_value_list = dht.nodeDict[node_with_key].hashTable[randKey]


def filter_by_awards(people, min_awards):
    """
    Filters the list of people, returning the names of those who have more than 'min_awards' awards.
    :param people: List of dictionaries containing person's details
    :param min_awards: Minimum number of awards required to be included in the result
    :return: List of names of people who have more than 'min_awards' awards
    """
    filtered_names = [person['name'] for person in people if int(person['awards']) > min_awards]

    return filtered_names

start_time = time.time()
print(filter_by_awards(ht_value_list, 1))
end_time = time.time()

elapsed_time = end_time - start_time
print("time elapsed for query:", elapsed_time)

