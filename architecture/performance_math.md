Little’s Law:

L = λ × W
Where:

L = Average # of items in system

λ = Arrival rate (posts/sec)

W = Average time in system (sec)

Example (assume):

λ = 1000 posts/hour = 0.28 posts/sec

W = ~60 sec (Airflow batch lag)

→ L = 0.28 × 60 = 16.8 posts in system at any time

Also calculate:

Airflow batch size

Optimal worker count (assume 1 CPU can clean 50 posts/sec)