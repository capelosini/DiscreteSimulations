import random

import Utils

nextCustomerID = 1


class Customer:
    def __init__(self, id=None, name=None, demand=None):
        global nextCustomerID
        self.id = id if id is not None else nextCustomerID
        nextCustomerID += 1
        self.name = name if name is not None else Utils.generateCustomerFullname()
        self.demand = demand if demand is not None else random.random()
