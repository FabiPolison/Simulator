import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from Simulator import Simulator
from matplotlib import rcParams


class QueueSimulation:
    def __init__(self, simulator):
        self.simulator = simulator
    
    def plot_arrival_times(self):
        plt.scatter(self.simulator.customer_ids, self.simulator.arrival_times)
        plt.xlabel('Customer IDs')
        plt.ylabel('Arrival times')
        plt.title('Arrival Times Distribution')
        plt.show()

    def plot_service_times_distribution(self):
        plt.hist(self.simulator.service_times, bins=10, color='skyblue', edgecolor='black')
        plt.xlabel('Service Time')
        plt.ylabel('Frequency')
        plt.title('Service Times Distribution')
        plt.show()

    def plot_server_utilization(self):
        total_simulation_time = max(self.simulator.assignment.customer_end_times)
        server_busy_times = self.simulator.assignment.server_busy_times
        server_utilizations = [(busy_time / total_simulation_time) * 100 for busy_time in server_busy_times]

        server_ids = range(1, self.simulator.number_of_servers + 1) 
        plt.bar(server_ids, server_utilizations, color='skyblue', edgecolor='black')
        plt.xlabel('Server ID')
        plt.ylabel('Utilization (%)')
        plt.title('Server Utilization')
        plt.show()

    def plot_waiting_times(self):
        sns.lineplot(x=self.simulator.customer_ids, y=self.simulator.assignment.waiting_times)
        plt.xlabel('Customer ID')
        plt.ylabel('Waiting Time')
        plt.title('Waiting Times')
        plt.show()

    def plot_turnaround_times(self):
        sns.lineplot(x=self.simulator.customer_ids, y=self.simulator.assignment.turnaround_times)
        plt.xlabel('customer ids')
        plt.ylabel('turn around times')
        plt.title('turnaround Times Distribution')
        plt.show()

    def plot_response_times(self):
        sns.lineplot(x=self.simulator.customer_ids, y=self.simulator.assignment.response_times)
        plt.xlabel('cust ids')
        plt.ylabel('Response times')
        plt.title('Response Times Distribution')
        plt.show()

    def plot_inter_arrival_times(self):
        sns.displot(self.simulator.inter_arrivals, kde=False, color='b', bins=20)
        plt.title('Time between Arrivals')
        plt.xlabel('Minutes')
        plt.ylabel('Frequency')
        sns.despine()
        plt.show()

if __name__ == "__main__":
    arrival_mean = float(input("Enter mean arrival time: "))
    service_mean = float(input("Enter mean service time: "))
    number_of_servers = int(input("Enter number of servers: "))

    # Initialize Simulator object and run simulation outside QueueSimulation class
    simulator = Simulator(arrival_mean, service_mean, number_of_servers)
    simulator.run_simulation()
    simulator.display_results()

    # Pass the simulator object to QueueSimulation
    simulation = QueueSimulation(simulator)
    simulation.plot_arrival_times()
    simulation.plot_service_times_distribution()
    simulation.plot_server_utilization()
    simulation.plot_waiting_times()
    simulation.plot_turnaround_times()
    simulation.plot_response_times()
    simulation.plot_inter_arrival_times()
