import matplotlib.pyplot as plt
from SimulatorPriority import PrioritySimulator

class Task:
    def __init__(self, customer_id, start_time, end_time, server):
        self.customer_id = customer_id
        self.start_time = start_time
        self.end_time = end_time
        self.server = server
        self.service_time = self.end_time - self.start_time

class GanttChartView:
    def __init__(self, customers, number_of_servers):
        self.customers = customers
        self.number_of_servers = number_of_servers
        self.tasks = self.create_tasks()

    def create_tasks(self):
        tasks = []
        for customer in self.customers:
            if customer["Start"] is not None and customer["End"] is not None:
                task = Task(
                    customer_id=customer["C.No"],
                    start_time=customer["Start"],
                    end_time=customer["End"],
                    server=customer["Server"]  # Ensure each customer has an assigned server
                )
                tasks.append(task)
        return tasks

    def display_gantt_chart(self):
        fig, ax = plt.subplots(figsize=(12, 6))
        bar_height = 0.4

        for task in self.tasks:
            ax.barh(
                task.server - 1,  # Adjust for zero-based indexing
                task.service_time,
                left=task.start_time,
                height=bar_height,
                color='skyblue',
                edgecolor='black'
            )
            # Add task labels
            ax.text(
                task.start_time + task.service_time / 2,
                task.server - 1,
                f"C{task.customer_id}",
                ha='center',
                va='center',
                color='black',
                fontsize=9
            )

        # Configure chart appearance
        ax.set_yticks(range(self.number_of_servers))
        ax.set_yticklabels([f"Server {i + 1}" for i in range(self.number_of_servers)])
        ax.set_xlabel("Time")
        ax.set_ylabel("Servers")
        ax.set_title("Gantt Chart - Priority Scheduling")
        ax.grid(axis='x', linestyle='--', alpha=0.7)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # Input parameters for the priority simulator
    arrival_mean = float(input("Enter the mean arrival time: "))
    service_mean = float(input("Enter the mean service time: "))
    number_of_servers = int(input("Enter the number of servers: "))

    priority_params = {
        "A": 55,
        "M": 1994,
        "Z": 10112166,
        "C": 9,
        "a": 1,
        "b": 3,
    }

    # Run the priority simulator
    priority_simulator = PrioritySimulator(arrival_mean, service_mean, number_of_servers, priority_params)

    # Ensure customers are assigned to specific servers
    server_busy_times = priority_simulator.process_customers()

    # Assign servers to customers (this must be handled in the simulator logic)
    for server_id, customer in enumerate(priority_simulator.results):
        customer["Server"] = (server_id % number_of_servers) + 1

    # Display simulation results
    priority_simulator.display_results(server_busy_times)

    # Generate and display the Gantt chart for the priority simulator
    gantt_chart = GanttChartView(priority_simulator.results, number_of_servers)
    gantt_chart.display_gantt_chart()
