import random
from enum import Enum

import Storage
from rich import print
from simpy import Environment


class LogColor(Enum):
    GREEN = "[green]"
    BLUE = "[blue]"
    YELLOW = "[yellow]"
    RED = "[red]"
    PURPLE = "[purple]"
    CYAN = "[cyan]"
    MAGENTA = "[magenta]"
    BOLD_RED = "[bold red]"
    BOLD_GREEN = "[bold green]"
    BOLD_BLUE = "[bold blue]"
    BOLD_YELLOW = "[bold yellow]"
    BOLD_PURPLE = "[bold purple]"
    BOLD_CYAN = "[bold cyan]"
    BOLD_MAGENTA = "[bold magenta]"


class Logger:
    def __init__(self, env: Environment):
        self.env = env
        self.active = True

    def log(self, message: str, color: LogColor):
        if self.active:
            print(f"{color.value}{self.env.now:.3f}: {message}")


def generateCustomerFullname():
    return random.choice(Storage.first_names) + " " + random.choice(Storage.last_names)


def generateSellerFullname():
    return generateCustomerFullname() + " Seller"


def empiricalDist(values: list, weights: list[float], k=1):
    res = random.choices(values, weights=weights, k=k)
    return res[0] if k == 1 else res


def generateOrderItemsCount() -> int:
    return int(empiricalDist([1, 2, 3, 4, 5], [0.4, 0.3, 0.15, 0.1, 0.05]))


def generateItemCount() -> int:
    return int(empiricalDist([1, 2, 3, 4, 5], [0.5, 0.25, 0.1, 0.075, 0.05]))


def generateOrderProducts(db: Storage.DB):
    products = db.getTable("products")
    keys = list(products.keys())
    ids = random.choices(
        keys,
        weights=[products[p].demand for p in keys],
        k=generateOrderItemsCount(),
    )
    return {id: generateItemCount() for id in ids}


def getCurrentOrderRate(simTime):
    actual = (simTime / 60) % 24

    if 0 <= actual < 6:
        return 15 / 60  # Early Moring
    elif 6 <= actual < 10:
        return 30 / 60  # Morning
    elif 10 <= actual < 14:
        return 120 / 60  # Midday
    elif 14 <= actual < 18:
        return 80 / 60  # Afternoon
    else:
        return 60 / 60  # Night


def getActualReceiveOrderTimeout(env):
    # Exponential Distribution
    lambdaRate = getCurrentOrderRate(env.now)
    return random.expovariate(lambdaRate)


def getCurrentTruckRate(simTime):
    actual = (simTime / 60) % 24

    if 0 <= actual < 6:
        return 0  # Early Moring
    elif 6 <= actual < 10:
        return 25 / 60  # Morning
    elif 10 <= actual < 14:
        return 50 / 60  # Midday
    elif 14 <= actual < 18:
        return 20 / 60  # Afternoon
    else:
        return 0  # Night


def getActualTruckTimeout(env):
    # Exponential Distribution
    lambdaRate = getCurrentTruckRate(env.now)
    return random.expovariate(lambdaRate)


def isWorkTime(simTime):
    actual = (simTime / 60) % 24

    if actual >= 6 and actual < 18:
        return True
    else:
        return False


def chanceTo(successRate, returnIfSuccess, returnIfFail):
    return returnIfSuccess if random.random() < successRate else returnIfFail
