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

            lead_time = (end_time - start_time) if (end_time and start_time) else None
            process_duration = (
                (proc_end - proc_start) if (proc_end and proc_start) else None
            )

            row = {
                "id": o.id,
                "status": o.status.name,
                "start_time": start_time,
                "shipped_time": end_time,  # Needed for max time calculation
                "lead_time": lead_time,
                "process_duration": process_duration,
            }
            order_data.append(row)
        df_orders = pd.DataFrame(order_data)

        # --- TRUCK DATA ---
        truck_data = []
        for t in self.trucks.values():
            arrived = t.timing.get(TruckStatus.Arrived)
            shipped = t.timing.get(TruckStatus.Shipped)
            wait_time = (shipped - arrived) if (arrived and shipped) else None

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
        fig, axes = plt.subplots(3, 2, figsize=(14, 15))
        fig.suptitle("Logistics Simulation Dashboard", fontsize=16)

        # CALCULATE METRICS
        avg_lead_time = 0
        median_lead_time = 0
        throughput_per_hour = 0
        arrival_per_hour = 0

        if not df_orders.empty:
            # Determine total simulation time based on last event
            max_time_orders = df_orders["shipped_time"].max()
            max_time_arrival = df_orders["start_time"].max()
            total_sim_time = max(
                max_time_orders if pd.notna(max_time_orders) else 0,
                max_time_arrival if pd.notna(max_time_arrival) else 0,
            )

            # --- Rate Calculations ---
            total_shipped = len(df_orders.dropna(subset=["lead_time"]))
            total_created = len(df_orders)

            if total_sim_time > 0:
                # Calculate per Hour (assuming sim time is in minutes)
                throughput_per_hour = (total_shipped / total_sim_time) * 60
                arrival_per_hour = (total_created / total_sim_time) * 60

            completed_orders = df_orders.dropna(subset=["lead_time"])

            if not completed_orders.empty:
                avg_lead_time = completed_orders["lead_time"].mean()
                median_lead_time = completed_orders["lead_time"].median()

                # --- Plot 1: Lead Time Distribution ---
                axes[0, 0].hist(
                    completed_orders["lead_time"],
                    bins=25,
                    color="skyblue",
                    edgecolor="white",
                    alpha=0.8,
                    label="Lead Time",
                )
                axes[0, 0].axvline(
                    median_lead_time,
                    color="purple",
                    linestyle="-",
                    linewidth=3,
                    label=f"Median: {median_lead_time:.1f}m",
                )
                axes[0, 0].axvline(
                    avg_lead_time,
                    color="red",
                    linestyle="--",
                    linewidth=2,
                    label=f"Avg: {avg_lead_time:.1f}m",
                )
                axes[0, 0].set_title("Customer Wait Time Distribution")
                axes[0, 0].set_ylabel("Frequency")
                axes[0, 0].legend()

        # --- Plot 2: Processing vs Waiting Time ---
        if not df_orders.empty:
            sample = df_orders.head(50).dropna(subset=["lead_time", "process_duration"])
            if not sample.empty:
                axes[0, 1].plot(
                    sample["id"],
                    sample["lead_time"],
                    label="Total Lead Time",
                    marker="o",
                    alpha=0.5,
                )
                axes[0, 1].plot(
                    sample["id"],
                    sample["process_duration"],
                    label="Work Time",
                    marker="x",
                    color="green",
                )
                axes[0, 1].set_title("Total vs Work Time (First 50 Orders)")
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
            axes[1, 1].set_title(
                f"Throughput (Avg: {throughput_per_hour:.1f} orders/h)"
            )  # Added to Title
            axes[1, 1].set_xlabel("Simulation Time")
            axes[1, 1].grid(True)

        # --- Plot 5: Truck Turnaround Time ---
        if not df_trucks.empty and "wait_time" in df_trucks.columns:
            completed_trucks = df_trucks.dropna(subset=["wait_time"])
            if not completed_trucks.empty:
                axes[2, 0].scatter(
                    completed_trucks["arrival_time"],
                    completed_trucks["wait_time"],
                    c="orange",
                    edgecolor="black",
                    alpha=0.7,
                )
                axes[2, 0].set_title("Truck Turnaround Time")
                axes[2, 0].set_xlabel("Arrival Time")
                axes[2, 0].set_ylabel("Wait Time (min)")
                axes[2, 0].grid(True, linestyle="--")

        # --- Plot 6: Summary Text ---
        axes[2, 1].axis("off")

        summary_text = (
            f"SIMULATION METRICS\n"
            f"------------------\n"
            f"Orders Shipped: {len(df_orders.dropna(subset=['lead_time']))}\n"
            f"\n"
            f"SYSTEM RATES (Speed):\n"
            f"Demand (In):   {arrival_per_hour:.1f} orders/hour\n"
            f"Capacity (Out):{throughput_per_hour:.1f} orders/hour\n"  # NEW METRIC
            f"\n"
            f"WAIT TIME:\n"
            f"Median: {median_lead_time:.2f} min\n"
            f"Average:{avg_lead_time:.2f} min\n"
        )

        # Add warning if system is overloaded
        if arrival_per_hour > throughput_per_hour:
            summary_text += f"\n[!] WARNING: DEMAND > CAPACITY\n    Backlog is growing!"

        axes[2, 1].text(0.1, 0.3, summary_text, fontsize=12, family="monospace")

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()
