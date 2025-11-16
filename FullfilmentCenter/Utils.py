import random

import DB


def generateCustomerFullname():
    return random.choice(DB.first_names) + " " + random.choice(DB.last_names)


def generateSellerFullname():
    return generateCustomerFullname() + " Seller"


def chanceTo(successRate, returnIfSuccess, returnIfFail):
    return returnIfSuccess if random.random() < successRate else returnIfFail
