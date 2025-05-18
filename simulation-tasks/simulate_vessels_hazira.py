'''
simulate_vessels_hazira.py
Simulate 1 200 vessel calls/yr
(bulk carriers, container ships, tankers) 
via Poisson arrivals; service μ = 23h, σ = 4.5h; 
include 11 % delay events.

https://www.scribbr.com/statistics/poisson-distribution/
#:~:text=A%20Poisson%20distribution%20is%20a,the%20mean%20number%20of%20events.
A Poisson distribution is a discrete probability distribution.
It gives the probability of an event happening a certain number 
of times (k) within a given interval of time or space.

The Poisson distribution has only one parameter, λ (lambda), 
which is the mean number of events.

So, if there are a mean of 1200 vessel calls/year, we need to convert
those aggregate arrivals to the times at which each vessel arrives.

https://www.probabilitycourse.com/chapter11/11_1_2_
basic_concepts_of_the_poisson_process.php#:~:text=The%20
Poisson%20distribution%20can%20be%20viewed%20as%20the%20limit
%20of%20binomial%20distribution.&text=If%20N(t)%20is%20a%20
Poisson%20process%20with,%E2%8B%AF%20are%20independent%20an
d%20Xi%E2%88%BCExponential(%CE%BB)%2C%20for%20i=1%2C2%2C3%2C%E2%8B%AF.
If there are 1200 vessel calls/year, then the mean time between arrivals
is 1/1200 per year is modeled by an exponential process.
'''

import csv
import numpy as np
BERTHS = ['MP1', 'MP2', 'MP3', 'MP4', 'CT1', 'CT2']
ARRIVALS_PER_YEAR = 1200

# The number of vessels that will arrive this year
number_vessels = np.random.poisson(lam=ARRIVALS_PER_YEAR, size=1)[0]

# These arrivals times represent the time between consecutive arrivals of vessels
arrival_times = np.random.exponential(scale=1/ARRIVALS_PER_YEAR, size=number_vessels)
print(arrival_times)

data = []

with open('vessel_turnaround_hazira.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(data)