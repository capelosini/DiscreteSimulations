import random

import simpy
import Utils
from Classes import Customer, Order, Product, Truck
from Storage import DB, OrderStatus, TruckStatus

db = DB()

## INIT PRODUCTS
for _ in range(20):
    product = Product(db)
    product.addToDB()

env = simpy.Environment(60 * 6)
employees = simpy.Resource(env, capacity=50)
docks = simpy.Resource(env, capacity=6)

logger = Utils.Logger(env)
# logger.active = False

readyToShipOrders = []


def processOrder(order: Order):
    while not Utils.isWorkTime(env.now):
        yield env.timeout(1)

    req = employees.request()
    yield req

    order.changeStatus(OrderStatus.PROCESSING)
    logger.log(f"Order {order.id} is being processed", Utils.LogColor.YELLOW)

    TIME_PER_ITEM = 1.5
    TIME_SETUP = 1
    DESV = 1.0

    qtd_itens = len(order.products)

    base_time = (qtd_itens * TIME_PER_ITEM) + TIME_SETUP
    # normal dist
    total_time = max(0.5, random.normalvariate(base_time, DESV))

    yield env.timeout(total_time)

    employees.release(req)
    logger.log(
        f"Order {order.id} processed in {total_time:.2f} min and ready to be shipped!",
        Utils.LogColor.MAGENTA,
    )
    order.changeStatus(OrderStatus.PROCESSED)
    order.addToDB()
    readyToShipOrders.append(order)


def orders():
    while True:
        customer = Customer(db)
        customer.addToDB()
        order = customer.order(env=env)
        logger.log(
            f"Customer {customer.name} ordered products {order.products}!",
            Utils.LogColor.BLUE,
        )
        env.process(processOrder(order))
        yield env.timeout(Utils.getActualReceiveOrderTimeout(env))


def truckPickup(truck: Truck):
    global readyToShipOrders
    with docks.request() as req:
        yield req

        logger.log(
            f"{truck.type.name} Truck {truck.id} docked and started loading.",
            Utils.LogColor.YELLOW,
        )
        truck.changeStatus(TruckStatus.Loading)

        capacity = truck.type.value

        loadedCount = 0
        ordersLoaded = []
        for i in range(len(readyToShipOrders)):
            if i >= len(readyToShipOrders):
                break
            order = readyToShipOrders[i]
            if order.totalUnits <= capacity - loadedCount:
                orderToLoad = readyToShipOrders.pop(i)
                yield env.timeout(len(orderToLoad.products))
                loadedCount += orderToLoad.totalUnits
                ordersLoaded.append(orderToLoad)
                truck.orders.append(orderToLoad)
            if loadedCount >= capacity:
                break
        if loadedCount > 0:
            totalOrdersLoadedCount = len(ordersLoaded)
            for order in ordersLoaded:
                order.changeStatus(OrderStatus.SHIPPED)
            logger.log(
                f"{truck.type.name} Truck finished loading {loadedCount}/{capacity} product units with {totalOrdersLoadedCount} orders and left dock.",
                Utils.LogColor.GREEN,
            )
            truck.changeStatus(TruckStatus.Shipped)
            truck.addToDB()
        else:
            logger.log(
                f"{truck.type.name} Truck left empty (no orders ready).",
                Utils.LogColor.RED,
            )


def trucksArrival():
    while True:
        while not Utils.isWorkTime(env.now):
            yield env.timeout(1)

        truck = Truck(db, env)
        truck.addToDB()

        logger.log(f"{truck.type.name} Truck {truck.id} arrived!", Utils.LogColor.BLUE)

        env.process(truckPickup(truck))

        yield env.timeout(Utils.getActualTruckTimeout(env))


env.process(orders())
env.process(trucksArrival())

env.run(until=60 * 18)


db.plot_analytics()
