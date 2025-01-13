from collections import deque
from prettytable import PrettyTable
from Simulator import Simulator

class PrioritySimulator:
    def __init__(self, arrival_mean, service_mean, num_servers, priority_params):
        self.simulator = Simulator(arrival_mean, service_mean, num_servers)

        interarrival_times = self.calculate_interarrival_times(self.simulator.arrival_times)
        self.priorities = self.get_priorities(
            len(self.simulator.arrival_times),
            priority_params['A'],
            priority_params['M'],
            priority_params['Z'],
            priority_params['C'],
            priority_params['a'],
            priority_params['b'],
        )

        self.customers = [
            {
                "C.No": i + 1,
                "Arrival": self.simulator.arrival_times[i],
                "Interarrival": interarrival_times[i],
                "Service": self.simulator.service_times[i],
                "Priority": self.priorities[i],
                "Remaining": self.simulator.service_times[i],
                "Start": None,
                "End": None,
                "TAT": None,
                "Wait": 0,
                "Response": None,
            }
            for i in range(len(self.simulator.arrival_times))
        ]

        self.time = 0
        self.queue = deque()
        self.results = []
        self.num_servers = num_servers

    def calculate_interarrival_times(self, arrival_times):
        interarrival_times = [arrival_times[0]]
        for i in range(1, len(arrival_times)):
            interarrival_times.append(arrival_times[i] - arrival_times[i - 1])
        return interarrival_times

    def get_priorities(self, length, A, M, Z, C, a, b):
        priorities = []
        for _ in range(length):
            R = (A * Z + C) % M
            S = R / M
            Y = round((b - a) * S + a)
            priorities.append(Y)
            Z = R
        return priorities

    def process_customers(self):
        customers = sorted(self.customers, key=lambda x: x["Arrival"])
        server_end_times = [0] * self.num_servers
        server_busy_times = [0] * self.num_servers
        server_customers = [None] * self.num_servers

        while customers or self.queue or any(server_customers):
            while customers and customers[0]["Arrival"] <= self.time:
                self.queue.append(customers.pop(0))

            self.queue = deque(sorted(self.queue, key=lambda x: (x["Priority"], x["Arrival"])))

            for server_id in range(self.num_servers):
                if server_customers[server_id]:
                    current_customer = server_customers[server_id]
                    if current_customer["Remaining"] == 0:
                        current_customer["End"] = self.time
                        current_customer["TAT"] = current_customer["End"] - current_customer["Arrival"]
                        current_customer["Wait"] = current_customer["TAT"] - current_customer["Service"]
                        current_customer["Response"] = current_customer["Start"] - current_customer["Arrival"]
                        self.results.append(current_customer)
                        server_customers[server_id] = None

                if not server_customers[server_id] and self.queue:
                    next_customer = self.queue.popleft()
                    next_customer["Start"] = self.time if next_customer["Start"] is None else next_customer["Start"]
                    server_customers[server_id] = next_customer

                elif server_customers[server_id]:
                    for higher_priority_customer in self.queue:
                        if higher_priority_customer["Priority"] < server_customers[server_id]["Priority"]:
                            self.queue.append(server_customers[server_id])
                            server_customers[server_id] = self.queue.popleft()
                            server_customers[server_id]["Start"] = self.time if server_customers[server_id]["Start"] is None else server_customers[server_id]["Start"]
                            break

                if server_customers[server_id]:
                    server_customers[server_id]["Remaining"] -= 1
                    server_busy_times[server_id] += 1

            self.time += 1

        return server_busy_times

    def calculate_priority_wise_measures(self):
        priority_groups = {}

        for customer in self.results:
            priority = customer["Priority"]
            if priority not in priority_groups:
                priority_groups[priority] = {
                    "TAT": [], "Wait": [], "Response": [], "Interarrival": []
                }

            priority_groups[priority]["TAT"].append(customer["TAT"])
            priority_groups[priority]["Wait"].append(customer["Wait"])
            priority_groups[priority]["Response"].append(customer["Response"])
            priority_groups[priority]["Interarrival"].append(customer["Interarrival"])

        priority_measures = {}
        for priority, metrics in priority_groups.items():
            priority_measures[priority] = {
                "Average TAT": sum(metrics["TAT"]) / len(metrics["TAT"]),
                "Average Wait": sum(metrics["Wait"]) / len(metrics["Wait"]),
                "Average Response": sum(metrics["Response"]) / len(metrics["Response"]),
                "Average Interarrival": sum(metrics["Interarrival"]) / len(metrics["Interarrival"]),
            }

        return priority_measures

    def display_results(self, server_busy_times):
        total_simulation_time = max(c["End"] for c in self.results)

        table = PrettyTable()
        table.field_names = [
            "C.No", "Arrival", "Interarrival", "Priority",
            "Service", "Start", "End", "TAT", "Wait", "Response"
        ]

        for customer in sorted(self.results, key=lambda x: x["C.No"]):
            table.add_row([
                customer["C.No"], customer["Arrival"], customer["Interarrival"],
                customer["Priority"], customer["Service"], customer["Start"],
                customer["End"], customer["TAT"], customer["Wait"], customer["Response"]
            ])

        print(table)

        avg_tat = sum(c["TAT"] for c in self.results) / len(self.results)
        avg_wait = sum(c["Wait"] for c in self.results) / len(self.results)
        avg_response = sum(c["Response"] for c in self.results) / len(self.results)
        avg_interarrival = sum(c["Interarrival"] for c in self.results) / len(self.results)
        avg_service_time = sum(c["Service"] for c in self.results) / len(self.results)

        print("\nPerformance Measures:")
        print(f"Average Interarrival Time: {avg_interarrival:.2f} min")
        print(f"Average Service Time: {avg_service_time:.2f} min")
        print(f"Average Turnaround Time (TAT): {avg_tat:.2f} min")
        print(f"Average Wait Time: {avg_wait:.2f} min")
        print(f"Average Response Time: {avg_response:.2f} min")

        for i, utilization in enumerate([(busy / total_simulation_time) * 100 for busy in server_busy_times]):
            print(f"Server {i + 1} Utilization: {utilization:.2f}%")

        priority_measures = self.calculate_priority_wise_measures()
        print("\nPriority-wise Performance Measures:")
        for priority, measures in sorted(priority_measures.items()):
            print(f"Priority {priority}:")
            print(f"  Average TAT: {measures['Average TAT']:.2f} min")
            print(f"  Average Wait: {measures['Average Wait']:.2f} min")
            print(f"  Average Response: {measures['Average Response']:.2f} min")
            print(f"  Average Interarrival: {measures['Average Interarrival']:.2f} min")

"""if __name__ == "__main__":
    arrival_mean = float(input("Enter mean arrival time: "))
    service_mean = float(input("Enter mean service time: "))
    num_servers = int(input("Enter number of servers: "))

    priority_params = {
        "A": 55,
        "M": 1994,
        "Z": 10112166,
        "C": 9,
        "a": 1,
        "b": 3,
    }

    simulator = PrioritySimulator(arrival_mean, service_mean, num_servers, priority_params)
    server_busy_times = simulator.process_customers()
    simulator.display_results(server_busy_times)"""
