import simpy
from Classes import Customer, Product, Seller
from Storage import DB
from Utils import *

db = DB()

## INIT PRODUCTS
for _ in range(20):
    product = Product(db)
    product.addToDB()

env = simpy.Environment()
employees = simpy.Resource(env, capacity=2)


def process_order(order):
    req = employees.request()
    yield req
    print(f"{env.now} A order is being processed")
    yield env.timeout(3)
    employees.release(req)
    print(f"{env.now} Order processed")


def orders():
    while True:
        if chanceTo(0.55, True, False):
            customer = Customer(db)
            customer.addToDB()
            print(f"{env.now} Customer {customer.name} ordered something!")
            env.process(process_order(None))
        yield env.timeout(1)


env.process(orders())

env.run(until=50)
