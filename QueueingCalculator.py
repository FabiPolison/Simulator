import random

class MGNMetrics:
    def __init__(self, arrival_mean, min_service, max_service, number_of_servers):
        self.arrival_mean = arrival_mean
        self.min_service = min_service
        self.max_service = max_service
        self.number_of_servers = number_of_servers

        self.service_mean = (self.min_service + self.max_service) / 2
        self.service_variance = self.calculate_service_variance()
        self.utilization = self.calculate_utilization()
        self.avg_queue_length = self.calculate_avg_queue_length()
        self.avg_system_length = self.calculate_avg_system_length()
        self.avg_wait_time_in_system = self.calculate_avg_wait_time_in_system()
        self.avg_wait_time_in_queue = self.calculate_avg_wait_time_in_queue()

        self.display_results()

    def calculate_service_variance(self):
        mean = self.service_mean
        return ((self.max_service - mean) ** 2 + (self.min_service - mean) ** 2) / 2

    def calculate_utilization(self):
        return self.arrival_mean / (self.number_of_servers * self.service_mean)

    def calculate_avg_queue_length(self):
        p = self.utilization
        if p >= 1:
            return float('inf')  # System is unstable if utilization >= 1
        c2s = self.service_variance / (self.service_mean ** 2)  # Coefficient of variation squared
        numerator = (p ** 2) * (1 + c2s)
        denominator = 2 * (1 - p)
        return numerator / denominator

    def calculate_avg_system_length(self):
        return self.avg_queue_length + self.utilization

    def calculate_avg_wait_time_in_system(self):
        return self.avg_system_length / self.arrival_mean

    def calculate_avg_wait_time_in_queue(self):
        return self.avg_queue_length / self.arrival_mean

    def display_results(self):
        print("\nM/G/N Simulation Results")
        print("----------------------------")
        print(f"Utilization (ρ): {self.utilization:.2f}")
        print(f"Average System Length (L): {self.avg_system_length:.2f}")
        print(f"Average Queue Length (Lq): {self.avg_queue_length:.2f}")
        print(f"Average Wait Time in System (W): {self.avg_wait_time_in_system:.2f}")
        print(f"Average Wait Time in Queue (Wq): {self.avg_wait_time_in_queue:.2f}")


class MMNSimulation:
    def __init__(self, arrival_mean, service_mean, number_of_servers):
        self.arrival_mean = arrival_mean
        self.service_mean = service_mean
        self.number_of_servers = number_of_servers

        self.utilization = 0.0
        self.avg_system_length = 0.0
        self.avg_queue_length = 0.0
        self.avg_wait_time_in_system = 0.0
        self.avg_wait_time_in_queue = 0.0

        self.calculate_mmn_metrics()
        self.display_results()

    def calculate_mmn_metrics(self):
        lambda_ = self.arrival_mean
        mu = self.service_mean
        N = self.number_of_servers

        # Utilization (ρ)
        self.utilization = lambda_ / (N * mu)
        if self.utilization >= 1.0:
            print("System is unstable. Utilization must be less than 1.")
            return

        # Calculate P0 (Probability of zero customers in the system)
        sum_ = sum((lambda_ / mu) ** k / self.factorial(k) for k in range(N))
        last_term = (lambda_ / mu) ** N / (self.factorial(N) * (1 - self.utilization))
        P0 = 1 / (sum_ + last_term)

        # Average Queue Length (Lq)
        numerator = P0 * (lambda_ / mu) ** N * self.utilization
        denominator = self.factorial(N) * (1 - self.utilization) ** 2
        self.avg_queue_length = numerator / denominator

        # Average System Length (L)
        self.avg_system_length = self.avg_queue_length + (lambda_ / mu)

        # Average Wait Time in Queue (Wq)
        self.avg_wait_time_in_queue = self.avg_queue_length / lambda_

        # Average Wait Time in System (W)
        self.avg_wait_time_in_system = self.avg_system_length / lambda_

    def display_results(self):
        print("\nM/M/N Simulation Results")
        print("----------------------------")
        print(f"Utilization (ρ): {self.utilization:.2f} min")
        print(f"Average System Length (L): {self.avg_system_length:.2f} min")
        print(f"Average Queue Length (Lq): {self.avg_queue_length:.2f} min")
        print(f"Average Wait Time in System (W): {self.avg_wait_time_in_system:.2f} min")
        print(f"Average Wait Time in Queue (Wq): {self.avg_wait_time_in_queue:.2f} min")

    @staticmethod
    def factorial(n):
        if n == 0:
            return 1
        return 1 if n == 1 else n * MMNSimulation.factorial(n - 1)


class GGNSimulation:
    def __init__(self, arrival_mean, service_mean, arrival_variance, service_variance, number_of_servers):
        self.arrival_mean = arrival_mean
        self.service_mean = service_mean
        self.arrival_variance = arrival_variance
        self.service_variance = service_variance
        self.number_of_servers = number_of_servers

        # Calculated metrics
        self.utilization = self.calculate_utilization()
        self.avg_queue_length = self.calculate_avg_queue_length()
        self.avg_system_length = self.calculate_avg_system_length()
        self.avg_wait_time_in_queue = self.calculate_avg_wait_time_in_queue()
        self.avg_wait_time_in_system = self.calculate_avg_wait_time_in_system()

        self.display_results()

    def calculate_utilization(self):
        rho = self.arrival_mean / (self.number_of_servers * self.service_mean)
        return min(rho, 1.0)  # Utilization cannot exceed 1.0

    def calculate_avg_queue_length(self):
        if self.utilization >= 1.0:
            return float('inf')  # System is unstable
        variance_factor = (self.arrival_variance + self.service_variance) / 2.0
        return (self.utilization ** 2 * (1 + variance_factor)) / (1 - self.utilization)

    def calculate_avg_system_length(self):
        return self.avg_queue_length + (self.arrival_mean / self.service_mean)

    def calculate_avg_wait_time_in_queue(self):
        return self.avg_queue_length / self.arrival_mean

    def calculate_avg_wait_time_in_system(self):
        return self.avg_wait_time_in_queue + (1 / self.service_mean)

    def display_results(self):
        print("\nG/G/N Metrics Simulation Results")
        print("-----------------------------------")
        print(f"Utilization (ρ): {self.utilization:.2f}")
        print(f"Average System Length (L): {self.avg_system_length:.2f}")
        print(f"Average Queue Length (Lq): {self.avg_queue_length:.2f}")
        print(f"Average Wait Time in System (W): {self.avg_wait_time_in_system:.2f}")
        print(f"Average Wait Time in Queue (Wq): {self.avg_wait_time_in_queue:.2f}")


if __name__ == "__main__":
    print("Select the Queueing Model:")
    print("1. M/M/N")
    print("2. M/G/N")
    print("3. G/G/N")
    model_choice = int(input("Enter your choice (1/2/3): "))

    if model_choice == 1:
        arrival_mean = float(input("Enter mean arrival time: "))
        service_mean = float(input("Enter mean service time: "))
        number_of_servers = int(input("Enter number of servers: "))
        MMNSimulation(arrival_mean, service_mean, number_of_servers)
    elif model_choice == 2:
        min_service = float(input("Enter min service: "))
        max_service = float(input("Enter max service: "))
        arrival_mean = float(input("Enter mean arrival time: "))
        number_of_servers = int(input("Enter number of servers: "))
        MGNMetrics(arrival_mean, min_service, max_service, number_of_servers)
    elif model_choice == 3:
        arrival_mean = float(input("Enter mean arrival time: "))
        service_mean = float(input("Enter mean service time: "))
        number_of_servers = int(input("Enter number of servers: "))
        arrival_variance = float(input("Enter arrival variance: "))
        service_variance = float(input("Enter service variance: "))
        GGNSimulation(arrival_mean, service_mean, arrival_variance, service_variance, number_of_servers)
    else:
        print("Invalid choice!")
