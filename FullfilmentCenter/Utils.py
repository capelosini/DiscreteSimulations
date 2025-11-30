import random

import Storage


def generateCustomerFullname():
    return random.choice(Storage.first_names) + " " + random.choice(Storage.last_names)


def generateSellerFullname():
    return generateCustomerFullname() + " Seller"


def generateOrderItemsCount():
    return random.choices([1, 2, 3, 4, 5], weights=[0.4, 0.3, 0.15, 0.1, 0.05], k=1)[
        0
    ]  # Empirical Distribution


def generateItemCount():
    return random.choices([1, 2, 3, 4, 5], weights=[0.5, 0.25, 0.1, 0.075, 0.05], k=1)[
        0
    ]  # Empirical Distribution


def generateOrderProducts(db: Storage.DB):
    products = db.getTable("products")
    ids = random.choices(
        products.keys(),
        weights=[p.demand for p in products.values()],
        k=generateOrderItemsCount(),
    )


def chanceTo(successRate, returnIfSuccess, returnIfFail):
    return returnIfSuccess if random.random() < successRate else returnIfFail
