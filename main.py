import numpy as np
import pandas as pd
from scipy.stats import lognorm, poisson, truncnorm
from tqdm import tqdm

# Constants
days_per_year = 365
mu, sigma = 3, 0.75  # Log-normal parameters for hotel occupancy
breakfast_start, breakfast_end = 450, 600  # 7:30 to 10:00 in minutes (from midnight)
breakfast_duration = breakfast_end - breakfast_start
service_rate = 2  # One customer served every 2 minutes
eating_area_capacity = 40  # Max number of people in eating area

# Truncated normal for eating time (5-60 min, mean=30, std=15)
def truncated_normal(mean, std, low, high, size):
    if size <= 0:
        return []
    a, b = (low - mean) / std, (high - mean) / std
    return int(truncnorm.rvs(a, b, loc=mean, scale=std, size=size)[0])

# Store results
minute_data = []
daily_summary = []

for day in tqdm(range(days_per_year), desc="Simulating Days"):
    # Generate daily hotel occupancy
    num_guests = np.clip(int(lognorm.rvs(sigma, scale=np.exp(mu))), 0, 123)


    # Poisson process for breakfast arrivals
    lambda_per_minute = num_guests / breakfast_duration
    arrivals_per_minute = poisson.rvs(lambda_per_minute, size=breakfast_duration)

    queue, processed_customers = 0, 0
    eating_area = {}
    num_served = 0
    queue_stats, eating_stats = [], []

    for minute in range(breakfast_duration):
        current_minute = breakfast_start + minute
        arrivals = arrivals_per_minute[minute]
        queue += arrivals

        # Process customers if queue exists and there is space in eating area
        if queue > 0 and len(eating_area) < eating_area_capacity:
            queue -= 1

            # Add the customer to the eating area with random eating durations
            eating_durations = truncated_normal(30, 15, 5, 60, 1)
            for key in range(eating_area_capacity):
              if key not in eating_area or eating_area[key] <= 0:
                  eating_area[key] = eating_durations  # Assign eating duration to this spot
                  break

        # Decrement the eating times for all people currently in the eating area
        processed_this_minute = 0
        for customer in list(eating_area.keys()):
            eating_area[customer] -= 1
            if eating_area[customer] <= 0:
                del eating_area[customer]
                processed_this_minute += 1


        processed_customers += processed_this_minute
        eating_area_count = len(eating_area)

        # Record the queue and eating area stats
        minute_data.append([day + 1, current_minute, num_guests, arrivals, queue, eating_area_count, processed_customers])
        queue_stats.append(queue)
        eating_stats.append(eating_area_count)

    # Compute daily statistics
    daily_summary.append([
        day + 1, processed_customers,
        max(eating_stats), np.mean(eating_stats), np.median(eating_stats), np.std(eating_stats),
        max(queue_stats), np.mean(queue_stats), np.median(queue_stats), np.std(queue_stats),
    ])

# Save to CSV
minute_df = pd.DataFrame(minute_data, columns=["Day", "Minute", "ExpectedForTheDay", "Arrivals", "Queue", "Eating_Area", "CustomerFedSoFar"])
daily_df = pd.DataFrame(daily_summary, columns=[
    "Day", "Clients_Served",
    "Max_Eating_Area", "Mean_Eating_Area", "Median_Eating_Area", "Std_Eating_Area",
    "Max_Queue", "Mean_Queue", "Median_Queue", "Std_Queue"
])

minute_df.to_csv("minute_by_minute_data.csv", index=False)
daily_df.to_csv("daily_summary.csv", index=False)

print("Simulation complete. CSV files generated.")
