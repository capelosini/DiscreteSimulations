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
    "Walter",
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


class DB:
    def __init__(self):
        self.customers = {}
        self.products = {}
        self.sellers = {}
        self.orders = []

    def getTable(self, tableName: str) -> dict | list:
        return self.__dict__.get(tableName, {})

    def addToTable(self, tableName, name, value) -> None:
        self.__dict__.get(tableName, {}).update({name: value})
