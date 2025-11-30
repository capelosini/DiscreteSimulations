import random
from enum import Enum

import Storage
import Utils
from simpy import Environment

nextCustomerID = 1
nextSellerID = 1
nextProductID = 1
nextOrderID = 1
nextTruckID = 1


class CanBeAddedToDB:
    def __init__(self):
        self.id = 0
        self.tableName = ""
        self.db = Storage.DB()

    def addToDB(self):
        self.db.addToTable(self.tableName, self.id, self)


class Product(CanBeAddedToDB):
    def __init__(
        self, db: Storage.DB, id=None, name=None, demand=None, defaultPrice=None
    ):
        global nextProductID
        self.db = db
        self.tableName = "products"
        self.id = id if id is not None else nextProductID
        self.name = name if name is not None else "Product " + str(nextProductID)
        nextProductID += 1
        self.demand = demand if demand is not None else random.random() % 0.60
        self.defaultPrice = (
            defaultPrice if defaultPrice is not None else random.randint(5, 100)
        )


# Will not be used!
class StockItem:
    def __init__(self, db: Storage.DB, productID=None, quantity=None, price=None):
        self.db = db
        self.productID = (
            productID
            if productID is not None
            else random.randint(1, len(self.db.getTable("products")))
        )
        self.quantity = quantity if quantity is not None else random.randint(5, 200)
        defaultPrice = self.db.getTable("products")[self.productID].defaultPrice
        self.price = (
            price
            if price is not None
            else random.randint(max(defaultPrice - 5, 0), defaultPrice + 5)
        )


# Will not be used!
class Seller(CanBeAddedToDB):
    def __init__(self, db: Storage.DB, id=None, name=None, stock=None):
        global nextSellerID
        self.db = db
        self.tableName = "sellers"
        self.id = id if id is not None else nextSellerID
        nextSellerID += 1
        self.name = name if name is not None else Utils.generateSellerFullname()
        self.stock = stock if stock is not None else []
        if stock is None:
            for _ in range(random.randint(2, 5)):
                item = StockItem(self.db)
                while item.productID in self.stock:
                    item = StockItem(self.db)
                self.stock.append(item.productID)


class HasTrackedStatus:
    def __init__(self):
        self.env = None
        self.status = None
        self.timing = {}

    def changeStatus(self, status: Enum):
        self.status = status
        self.timing[status] = self.env.now


class Order(CanBeAddedToDB, HasTrackedStatus):
    def __init__(
        self,
        db: Storage.DB,
        env: Environment,
        id=None,
        customerID=None,
        productsIDs=None,
    ):
        global nextOrderID
        self.db = db
        self.env = env
        self.tableName = "orders"
        self.id = id if id is not None else nextOrderID
        nextOrderID += 1
        self.customerID = customerID
        self.products = productsIDs if productsIDs is not None else {}
        self.status = Storage.OrderStatus.PENDING
        self.timing = {Storage.OrderStatus.PENDING: env.now}
        self.totalUnits = sum(self.products.values())


class Customer(CanBeAddedToDB):
    def __init__(self, db: Storage.DB, id=None, name=None, demand=None):
        global nextCustomerID
        self.db = db
        self.tableName = "customers"
        self.id = id if id is not None else nextCustomerID
        nextCustomerID += 1
        self.name = name if name is not None else Utils.generateCustomerFullname()
        self.demand = demand if demand is not None else random.random()

    def order(self, env: Environment, productsIDs: list[int] = []):
        if len(productsIDs) == 0:
            productsIDs = Utils.generateOrderProducts(self.db)
        order = Order(self.db, env, customerID=self.id, productsIDs=productsIDs)
        order.addToDB()
        return order


class Truck(CanBeAddedToDB, HasTrackedStatus):
    def __init__(self, db: Storage.DB, env: Environment, id=None, type=None):
        global nextTruckID
        self.db = db
        self.env = env
        self.status = Storage.TruckStatus.Arrived
        self.tableName = "trucks"
        self.id = id if id is not None else nextTruckID
        nextTruckID += 1
        self.type = (
            type
            if type is not None
            else Utils.empiricalDist(
                [
                    Storage.TruckType.Small,
                    Storage.TruckType.Medium,
                    Storage.TruckType.Large,
                ],
                [0.35, 0.35, 0.3],
            )
        )
        self.orders = []
        self.timing = {Storage.TruckStatus.Arrived: self.env.now}
