import math
import random
from prettytable import PrettyTable


class Simulator:
    def __init__(self, arrival_mean, service_mean, number_of_servers):
        self.arrival_mean = arrival_mean
        self.service_mean = service_mean
        self.number_of_servers = number_of_servers

        self.cumulative_probabilities = self.get_arrival_times(arrival_mean)
        self.cp_lookup = self.calculate_cp_lookup(self.cumulative_probabilities)
        self.inter_arrivals = self.calculate_inter_arrivals(self.cumulative_probabilities)
        self.arrival_times = self.calculate_arrival_times(self.inter_arrivals)
        self.service_times = self.get_service_times(len(self.arrival_times), service_mean)
        self.customer_ids = self.generate_customer_ids(len(self.arrival_times))

        # Initialize server assignment
        self.assignment = ServerAssign(
            arrivals=self.arrival_times,
            service_times=self.service_times,
            number_of_servers=self.number_of_servers,
            customer_ids=self.customer_ids,
            inter_arrivals=self.inter_arrivals
        )

    def get_arrival_times(self, mean_arrival_number):
        cumulative_probability = 0
        cumulative_probabilities = []
        x = 0

        while round(cumulative_probability, 4) < 1:
            new_value = (math.exp(-mean_arrival_number) * (mean_arrival_number ** x)) / math.factorial(x)
            cumulative_probability += new_value
            cumulative_probabilities.append(round(cumulative_probability, 4))
            x += 1

        return cumulative_probabilities

    def calculate_cp_lookup(self, cumulative_probabilities):
        if not cumulative_probabilities:
            return []
        cp_lookup = [0]  # Start with 0
        cp_lookup.extend(cumulative_probabilities[:-1])
        return cp_lookup

    def calculate_inter_arrivals(self, cumulative_probabilities):
        inter_arrivals = []
        for _ in range(len(cumulative_probabilities)):
            random_number = random.random()
            for j, value in enumerate(cumulative_probabilities):
                if random_number < value:
                    inter_arrivals.append(j)
                    break
        return inter_arrivals

    def calculate_arrival_times(self, inter_arrivals):
        arrival_times = [inter_arrivals[0]]
        for i in range(1, len(inter_arrivals)):
            arrival_times.append(arrival_times[i - 1] + inter_arrivals[i])
        return arrival_times

    def get_service_times(self, length, mean_service_number):
        service_times = []
        for _ in range(length):
            service_time = -mean_service_number * math.log(random.random())
            clamped_service_time = max(5, min(8, math.ceil(service_time)))
            service_times.append(clamped_service_time)
        return service_times

    def generate_customer_ids(self, count):
        return list(range(1, count + 1))

    def run_simulation(self):
        self.assignment.simulate_customer_assignment()

    def display_results(self):
        table = PrettyTable()
        table.field_names = [
            "Customer ID", "Arrival Time", "Inter Arrival Time",
            "Start Time", "End Time", "Turnaround Time",
            "Wait Time", "Response Time", "Service Time"
        ]

        for i in range(len(self.customer_ids)):
            table.add_row([
                self.customer_ids[i],
                self.arrival_times[i],
                self.inter_arrivals[i],
                self.assignment.start_times[i],
                self.assignment.customer_end_times[i],
                self.assignment.turnaround_times[i],
                self.assignment.waiting_times[i],
                self.assignment.response_times[i],
                self.service_times[i]
            ])

        print(table)

        # Performance measures
        avg_arrival_time = sum(self.arrival_times) / len(self.arrival_times)
        avg_interarrival_time = sum(self.inter_arrivals) / len(self.inter_arrivals)
        avg_turnaround_time = sum(self.assignment.turnaround_times) / len(self.assignment.turnaround_times)
        avg_waiting_time = sum(self.assignment.waiting_times) / len(self.assignment.waiting_times)
        avg_response_time = sum(self.assignment.response_times) / len(self.assignment.response_times)

        total_simulation_time = max(self.assignment.customer_end_times)
        server_busy_times = self.assignment.server_busy_times
        server_utilizations = [(busy_time / total_simulation_time) * 100 for busy_time in server_busy_times]

        print("\nPerformance Measures:")
        print(f"Average Arrival Time: {avg_arrival_time:.2f} min")
        print(f"Average Interarrival Time: {avg_interarrival_time:.2f} min")
        print(f"Average Turnaround Time: {avg_turnaround_time:.2f} min")
        print(f"Average Waiting Time: {avg_waiting_time:.2f} min")
        print(f"Average Response Time: {avg_response_time:.2f} min")

        for i, utilization in enumerate(server_utilizations):
            print(f"Server {i + 1} Utilization: {utilization:.2f}%")


class ServerAssign:
    def __init__(self, arrivals, service_times, number_of_servers, customer_ids, inter_arrivals):
        self.arrivals = arrivals
        self.service_times = service_times
        self.number_of_servers = number_of_servers
        self.customer_ids = customer_ids
        self.inter_arrivals = inter_arrivals

        # Initialize tracking variables
        self.server_assignments = [[] for _ in range(number_of_servers)]
        self.start_times = [0] * len(arrivals)
        self.end_times = [0] * number_of_servers
        self.customer_end_times = [0] * len(arrivals)
        self.waiting_times = [0] * len(arrivals)
        self.turnaround_times = [0] * len(arrivals)
        self.response_times = [0] * len(arrivals)
        self.server_busy_times = [0] * number_of_servers

    def simulate_customer_assignment(self):
        for i in range(len(self.arrivals)):
            assigned_server = None

            # Find the earliest free server
            for server in range(self.number_of_servers):
                if self.arrivals[i] >= self.end_times[server]:
                    assigned_server = server
                    break

            # If no free server is found, wait for the earliest free one
            if assigned_server is None:
                assigned_server = self.end_times.index(min(self.end_times))

            # Assign customer to the chosen server
            server = assigned_server
            self.server_assignments[server].append(self.customer_ids[i])

            # Calculate the start time correctly:
            self.start_times[i] = max(self.arrivals[i], self.end_times[server])

            # Update the end time of the assigned server
            self.end_times[server] = self.start_times[i] + self.service_times[i]

            # Calculate and store the customer's end time
            self.customer_end_times[i] = self.end_times[server]

            # Update server busy time
            self.server_busy_times[server] += self.service_times[i]

            # Calculate Waiting Time
            self.waiting_times[i] = self.start_times[i] - self.arrivals[i]

            # Calculate Turnaround Time
            self.turnaround_times[i] = self.customer_end_times[i] - self.arrivals[i]

            # Calculate Response Time
            self.response_times[i] = self.start_times[i] - self.arrivals[i]



"""if __name__ == "__main__":
    arrival_mean = float(input("Enter mean arrival time: "))
    service_mean = float(input("Enter mean service time: "))
    number_of_servers = int(input("Enter number of servers: "))

    simulator = Simulator(arrival_mean, service_mean, number_of_servers)
    simulator.run_simulation()
    simulator.display_results()"""
