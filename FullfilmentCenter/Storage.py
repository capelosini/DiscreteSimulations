from enum import Enum

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class OrderStatus(Enum):
    PENDING = 1
    PROCESSING = 2
    PROCESSED = 3
    SHIPPED = 4


class TruckType(Enum):
    Small = 10
    Medium = 20
    Large = 30


class TruckStatus(Enum):
    Arrived = 1
    Loading = 2
    Shipped = 3


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
        self.orders = {}
        self.trucks = {}

    def getTable(self, tableName: str) -> dict:
        return self.__dict__.get(tableName, {})

    def addToTable(self, tableName, name, value) -> None:
        self.__dict__.get(tableName, {}).update({name: value})

    def __str__(self):
        res = ""
        for table in self.__dict__:
            res += f"{table}: {[e.__dict__ for e in self.__dict__[table].values()]}\n"
        return res

    def plot_analytics(self):
        print("Generating Analytics...")

        # Extract Order Data
        order_data = []
        for o in self.orders.values():
            start_time = o.timing.get(OrderStatus.PENDING)
            end_time = o.timing.get(OrderStatus.SHIPPED)
            proc_start = o.timing.get(OrderStatus.PROCESSING)
            proc_end = o.timing.get(OrderStatus.PROCESSED)

            row = {
                "id": o.id,
                "status": o.status.name,
                "start_time": start_time,
                "lead_time": (end_time - start_time)
                if (end_time and start_time)
                else None,
                "process_duration": (proc_end - proc_start)
                if (proc_end and proc_start)
                else None,
            }
            order_data.append(row)
        df_orders = pd.DataFrame(order_data)

        # --- TRUCK DATA ---
        truck_data = []
        for t in self.trucks.values():
            arrived = t.timing.get(TruckStatus.Arrived)
            shipped = t.timing.get(TruckStatus.Shipped)

            # Calculate Wait Time (Turnaround Time)
            wait_time = None
            if arrived is not None and shipped is not None:
                wait_time = shipped - arrived

            row = {
                "id": t.id,
                "type": t.type.name,
                "capacity": t.type.value,
                "arrival_time": arrived,
                "shipped_time": shipped,
                "wait_time": wait_time,
            }
            truck_data.append(row)
        df_trucks = pd.DataFrame(truck_data)

        # 2. PLOTTING
        # ---------------------------------------------------------
        # Changed layout to 3 rows, 2 columns to fit new graphs
        fig, axes = plt.subplots(3, 2, figsize=(14, 15))
        fig.suptitle("Logistics Simulation Dashboard", fontsize=16)

        # --- Plot 1: Order Lead Time Distribution ---
        if not df_orders.empty and "lead_time" in df_orders.columns:
            completed_orders = df_orders.dropna(subset=["lead_time"])
            if not completed_orders.empty:
                axes[0, 0].hist(
                    completed_orders["lead_time"],
                    bins=20,
                    color="skyblue",
                    edgecolor="black",
                )
                axes[0, 0].set_title("Order Lead Time Distribution (Customer Wait)")
                axes[0, 0].set_xlabel("Minutes")
                axes[0, 0].set_ylabel("Frequency")

        # --- Plot 2: Processing vs Waiting Time (Bottleneck Check) ---
        if not df_orders.empty:
            sample = df_orders.head(50).dropna(subset=["lead_time", "process_duration"])
            if not sample.empty:
                axes[0, 1].plot(
                    sample["id"],
                    sample["lead_time"],
                    label="Total Lead Time",
                    marker="o",
                )
                axes[0, 1].plot(
                    sample["id"],
                    sample["process_duration"],
                    label="Active Work Time",
                    marker="x",
                )
                axes[0, 1].set_title("Total vs Active Time (First 50 Orders)")
                axes[0, 1].legend()

        # --- Plot 3: Truck Fleet Composition ---
        if not df_trucks.empty:
            type_counts = df_trucks["type"].value_counts()
            axes[1, 0].pie(
                type_counts,
                labels=type_counts.index,
                autopct="%1.1f%%",
                startangle=90,
                colors=["#ff9999", "#66b3ff", "#99ff99"],
            )
            axes[1, 0].set_title("Truck Fleet Composition")

        # --- Plot 4: Cumulative Orders Shipped ---
        if not df_orders.empty and "lead_time" in df_orders.columns:
            shipped_orders = df_orders.dropna(subset=["lead_time"]).copy()
            shipped_orders["shipped_timestamp"] = (
                shipped_orders["start_time"] + shipped_orders["lead_time"]
            )
            shipped_orders = shipped_orders.sort_values("shipped_timestamp")
            shipped_orders["cumulative"] = range(1, len(shipped_orders) + 1)

            axes[1, 1].plot(
                shipped_orders["shipped_timestamp"],
                shipped_orders["cumulative"],
                color="green",
                lw=2,
            )
            axes[1, 1].set_title("Throughput: Cumulative Orders Shipped")
            axes[1, 1].set_xlabel("Simulation Time")
            axes[1, 1].grid(True)

        # --- [NEW] Plot 5: Truck Turnaround Time (Arrived -> Shipped) ---
        if not df_trucks.empty and "wait_time" in df_trucks.columns:
            completed_trucks = df_trucks.dropna(subset=["wait_time"])

            if not completed_trucks.empty:
                # Scatter plot: X axis = When they arrived, Y axis = How long they waited
                # This helps visualize if the dock gets congested later in the day
                sc = axes[2, 0].scatter(
                    completed_trucks["arrival_time"],
                    completed_trucks["wait_time"],
                    c="orange",
                    edgecolor="black",
                    s=50,
                    alpha=0.7,
                )
                axes[2, 0].set_title("Truck Turnaround Time (Wait + Load)")
                axes[2, 0].set_xlabel("Time of Arrival (Sim Time)")
                axes[2, 0].set_ylabel("Duration at Dock (Minutes)")
                axes[2, 0].grid(True, linestyle="--")

                # Add a trend line or average line
                avg_wait = completed_trucks["wait_time"].mean()
                axes[2, 0].axhline(
                    y=avg_wait, color="r", linestyle="-", label=f"Avg: {avg_wait:.1f}m"
                )
                axes[2, 0].legend()
            else:
                axes[2, 0].text(
                    0.5, 0.5, "No trucks completed loading yet", ha="center"
                )

        # --- Plot 6: Empty (or Summary Text) ---
        axes[2, 1].axis("off")  # Hide the empty 6th slot

        # Summary Statistics text in the empty slot
        summary_text = (
            f"SIMULATION SUMMARY\n"
            f"------------------\n"
            f"Total Orders: {len(df_orders)}\n"
            f"Shipped Orders: {len(df_orders.dropna(subset=['lead_time']))}\n"
            f"Total Trucks Arrived: {len(df_trucks)}\n"
            f"Trucks Fully Served: {len(df_trucks.dropna(subset=['wait_time']))}\n"
        )
        axes[2, 1].text(0.1, 0.5, summary_text, fontsize=12, family="monospace")

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()
