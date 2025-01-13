# Simulator
The Python-based simulator models and analyzes queueing systems where both arrival times and service times follow a Poisson distribution.
Features Simulates customer arrivals and service times using Poisson-distributed intervals.
Supports multiple servers, dynamically assigning customers to the least utilized server.
Tracks and calculates key performance metrics:
Server Utilization
Average Queue Length
Average System Length
Average Waiting Time in the Queue
Average Waiting Time in the System
Visualizes system states and customer assignments for better understanding and analysis.
Includes statistical validation (e.g., Chi-square test) to ensure data adheres to the Poisson process.
Applications:
Useful for performance analysis of real-world queueing systems, such as:
=> Call centers
=> Traffic management
=> Network servers
=> Customer service counters
Can aid in optimizing resource allocation and minimizing wait times in multi-server environments.
Technologies Used
Python (Core implementation)
NumPy and SciPy for statistical computations
Matplotlib/Seaborn for visualizations (optional for enhanced analysis)
Getting Started
Clone the repository and run the simulator with custom parameters, such as:
Arrival rate
Service rate
Number of servers
