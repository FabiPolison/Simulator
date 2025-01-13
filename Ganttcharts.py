import matplotlib.pyplot as plt
from Simulator import Simulator, ServerAssign

class Task:
    def __init__(self, customer_id, start_time, end_time, server):
        self.customer_id = customer_id
        self.start_time = start_time
        self.end_time = end_time
        self.server = server
        self.service_time = self.end_time - self.start_time

class GanttChartView:
    def __init__(self, customer_ids, start_times, end_times, server_assignments, number_of_servers):
        self.customer_ids = customer_ids
        self.start_times = start_times
        self.end_times = end_times
        self.server_assignments = server_assignments
        self.number_of_servers = number_of_servers
        self.tasks = self.create_tasks()

    def create_tasks(self):
        tasks = []
        for server_index, customer in enumerate(self.server_assignments):
            for customer_id in customer:
                index = self.customer_ids.index(customer_id)
                task = Task(
                    customer_id=self.customer_ids[index],
                    start_time=self.start_times[index],
                    end_time=self.end_times[index],
                    server=server_index
                )
                tasks.append(task)
        return tasks

    def display_gantt_chart(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        bar_height = 0.2

        for task in self.tasks:
            ax.barh(
                task.server,
                task.service_time,
                left=task.start_time,
                color='skyblue',
                edgecolor='black'
            )
            # Add labels to the bars
            ax.text(
                task.start_time + task.service_time / 2,
                task.server,
                f"C{task.customer_id}",
                ha='center',
                va='center',
                color='black',
                fontsize=10
            )

        # Configure the chart
        ax.set_yticks(range(self.number_of_servers))
        ax.set_yticklabels([f"Server {i + 1}" for i in range(self.number_of_servers)])
        ax.set_xlabel("Time")
        ax.set_title("Gantt Chart")
        ax.grid(axis='x', linestyle='--', alpha=0.7)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # Input parameters for the simulator
    arrival_mean = float(input("Enter the mean arrival time: "))
    service_mean = float(input("Enter the mean service time: "))
    number_of_servers = int(input("Enter the number of servers: "))

    # Run the simulator
    simulator = Simulator(arrival_mean, service_mean, number_of_servers)
    simulator_results = ServerAssign(
        arrivals=simulator.arrival_times,
        service_times=simulator.service_times,
        number_of_servers=number_of_servers,
        customer_ids=simulator.customer_ids,
        inter_arrivals=simulator.inter_arrivals
    )
    simulator_results.simulate_customer_assignment()

    simulator.run_simulation()
    simulator.display_results()

    # Extract data from the simulator results
    customer_ids = simulator_results.customer_ids
    start_times = simulator_results.start_times
    end_times = simulator_results.customer_end_times
    server_assignments = simulator_results.server_assignments

    # Generate and display the Gantt chart
    gantt_chart = GanttChartView(customer_ids, start_times, end_times, server_assignments, number_of_servers)
    gantt_chart.display_gantt_chart()





