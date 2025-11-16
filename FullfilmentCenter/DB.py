import random

from Classes import Customer

first_names = [
    "Bob",
    "Alice",
    "Charlie",
    "David",
    "Eve",
    "Frank",
    "Grace",
    "Hannah",
    "Isaac",
    "Jack",
    "Kate",
    "Liam",
    "Mia",
    "Nathan",
    "Olivia",
    "Peter",
    "Quinn",
    "Rachel",
    "Sam",
    "Tina",
    "Uma",
    "Victor",
    "Wendy",
    "Xander",
    "Yara",
    "Zoe",
]

last_names = [
    "Smith",
    "Johnson",
    "Williams",
    "Jones",
    "Brown",
    "Davis",
    "Miller",
    "Wilson",
    "Moore",
    "Taylor",
    "Anderson",
    "Thomas",
    "Jackson",
    "White",
    "Harris",
    "Martin",
    "Thompson",
    "Garcia",
    "Martinez",
    "Robinson",
    "Clark",
    "Rodriguez",
    "Lewis",
    "Lee",
    "Walker",
    "Hall",
    "Allen",
    "Young",
]

customers = []
for i in range(15):
    customers.append(Customer())

products = {
    0: {"name": "Product 1", "demand": 0.45},
    1: {"name": "Product 2", "demand": 0.50},
    2: {"name": "Product 3", "demand": 0.25},
    3: {"name": "Product 4", "demand": 0.25},
    4: {"name": "Product 5", "demand": 0.10},
    5: {"name": "Product 6", "demand": 0.05},
    6: {"name": "Product 7", "demand": 0.30},
    7: {"name": "Product 8", "demand": 0.30},
    8: {"name": "Product 9", "demand": 0.40},
    9: {"name": "Product 10", "demand": 0.56},
    10: {"name": "Product 11", "demand": 0.60},
    11: {"name": "Product 12", "demand": 0.35},
    12: {"name": "Product 13", "demand": 0.55},
    13: {"name": "Product 14", "demand": 0.12},
    14: {"name": "Product 15", "demand": 0.45},
}

sellers = {
    0: {
        "name": "Seller 1",
        "stock": {
            0: {"price": 10, "quantity": 100},
            1: {"price": 15, "quantity": 150},
            14: {"price": 20, "quantity": 50},
            8: {"price": 12, "quantity": 30},
            6: {"price": 13, "quantity": 65},
        },
    },
    1: {
        "name": "Seller 2",
        "stock": {
            2: {"price": 10, "quantity": 25},
            12: {"price": 15, "quantity": 120},
            10: {"price": 22, "quantity": 95},
            5: {"price": 19, "quantity": 100},
            7: {"price": 35, "quantity": 45},
            1: {"price": 13, "quantity": 70},
            11: {"price": 10, "quantity": 60},
        },
    },
    2: {
        "name": "Seller 3",
        "stock": {
            3: {"price": 10, "quantity": 52},
            6: {"price": 15, "quantity": 25},
            13: {"price": 20, "quantity": 100},
            4: {"price": 22, "quantity": 150},
            9: {"price": 45, "quantity": 23},
        },
    },
}

orders = [
    # {
    #     "id": 1,
    #     "cart": [{"seller": 0, "product": 0, "quantity": 5}],
    #     "total": 5,
    # }
]
