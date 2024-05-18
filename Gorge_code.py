# -*- coding: utf-8 -*-
"""
Created on Tue May  7, 09:12:13, 2024

"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm       # Cool Progress Bar-Bar

np.random.seed(7052024)     # Allows reproducability

#          Arrival Times | Plot up to t=40 | Departure Times | Queue Length
exFlags = [1,              1,                1,                1];

# Set the number of packets
number_of_packets = 2000

# Set the parameters for the exponential distributions
lambda_param = 0.5  # Input rate
mu_param = 0.01     # Output rate

# Generate realizations
inter_arrival_times = np.random.exponential(scale=1/lambda_param, size=number_of_packets)
processing_times = np.random.exponential(scale=1/mu_param, size=number_of_packets)

# Calculate the input timeline
arrival_times = np.cumsum(inter_arrival_times)

if exFlags[0]:
    # Append 0 to the cumulative sum (for a nice presentation)
    cumulative_sum = np.concatenate(([0], arrival_times))
    print(f'Timeline head:{ cumulative_sum[:10] }')
    
    # Plot all points
    plt.plot(cumulative_sum, range(number_of_packets + 1), linestyle='-')
    plt.title('Poisson Process (All Points)')
    plt.xlabel('Time [sec?]')
    plt.ylabel('Value')
    plt.grid(True)
    plt.show()


if exFlags[1]:
    # Plot points up to t=40
    plt.plot(cumulative_sum, range(number_of_packets + 1), marker='o', linestyle='-')
    plt.title('Poisson Process (Up to t=40)')
    plt.xlabel('Time [sec?]')
    plt.ylabel('Value')
    plt.xlim(0, 40)
    plt.ylim(0, 25)
    plt.grid(True)
    plt.show()
    
    # Cut timeline to include all events up to t=40
    index_40 = np.argmax(cumulative_sum > 40)    # Find the first index when t > 40
    cumulative_sum = cumulative_sum[:index_40+1]
    plt.plot(cumulative_sum, range(index_40+1), marker='o', linestyle='-')
    plt.title('Poisson Process (Up to t=40, cut)')
    plt.xlabel('Time [sec?]')
    plt.ylabel('Value')
    plt.xlim(0, 40)
    plt.ylim(0, 25)
    plt.grid(True)
    plt.show()



if exFlags[2]:
    # Calculate departure times
    departure_times = [0]   # Initialize the departure time of the first packet
    for arrival_time, processing_time in zip(arrival_times, processing_times):
        
        # Calculate the departure time of the current packet
        departure_time = max(arrival_time, departure_times[-1]) + processing_time
        departure_times.append(departure_time)
        
    # Remove the auxiliarly element
    departure_times.pop(0)


if exFlags[3]:
    # Get queue length
    '''
        Main idea: Iterate over the event list of both arrivals and departures.
            Increase the Q size for each arrival and decrease it for each departure.
            Finally, save the result
    '''
    queue_length = 0
    event_times = np.sort(np.concatenate((arrival_times, departure_times))) # Combine and sort arrival and departure times
    queue_lengths = []
    
    # Iterate over event times
    for event_time in tqdm(event_times):
        # Update queue length
        for arrival_time in arrival_times:
            if event_time == arrival_time:
                queue_length += 1
        for departure_time in departure_times:
            if event_time == departure_time:
                queue_length -= 1
    
        queue_lengths.append(queue_length)
        
    # Plot all points
    plt.plot(event_times, queue_lengths, linestyle='-')
    plt.title('Queue Size (All Points)')
    plt.xlabel('Time [sec?]')
    plt.ylabel('Value')
    plt.grid(True)
    plt.show()