import random

import Utils
from DB import DB

nextCustomerID = 1
nextSellerID = 1
nextProductID = 1


class CanBeAddedToDB:
    def __init__(self):
        self.id = 0
        self.tableName = ""

    def addToDB(self):
        DB[self.tableName][self.id] = self


class Product(CanBeAddedToDB):
    def __init__(self, id=None, name=None, demand=None, defaultPrice=None):
        global nextProductID
        self.tableName = "products"
        self.id = id if id is not None else nextProductID
        self.name = name if name is not None else "Product " + str(nextProductID)
        nextProductID += 1
        self.demand = demand if demand is not None else random.random() % 0.60
        self.defaultPrice = (
            defaultPrice if defaultPrice is not None else random.randint(5, 100)
        )


class StockItem:
    def __init__(self, productID=None, quantity=None, price=None):
        self.productID = (
            productID
            if productID is not None
            else random.randint(1, len(DB["products"]))
        )
        self.quantity = quantity if quantity is not None else random.randint(5, 200)
        defaultPrice = DB["products"][self.productID].defaultPrice
        self.price = (
            price
            if price is not None
            else random.randint(max(defaultPrice - 5, 0), defaultPrice + 5)
        )


class Seller(CanBeAddedToDB):
    def __init__(self, id=None, name=None, stock=None):
        global nextSellerID
        self.tableName = "sellers"
        self.id = id if id is not None else nextSellerID
        nextSellerID += 1
        self.name = name if name is not None else Utils.generateSellerFullname()
        self.stock = stock if stock is not None else []
        if stock is None:
            for _ in range(random.randint(2, 5)):
                self.stock.append(random.randint(1, 100))


class Customer(CanBeAddedToDB):
    def __init__(self, id=None, name=None, demand=None):
        global nextCustomerID
        self.tableName = "customers"
        self.id = id if id is not None else nextCustomerID
        nextCustomerID += 1
        self.name = name if name is not None else Utils.generateCustomerFullname()
        self.demand = demand if demand is not None else random.random()
