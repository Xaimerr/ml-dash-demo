"Generates data from 5 different states with one of them being much better so that MAB finds it"
import MySQLdb
import time
import datetime
from scipy.stats import multivariate_normal
import numpy as np
from info import user, psswd, db_name

# Variables
K = 5             # Number of states
N_samples = 1000  # Amount of samples for simulation

# Multivariate normal variable
# NOTE: var.rvs(N) draws N random samples
mu = [-50, -54, -32, -48, -45]
s = [[5, 0, 0, 0, 0],
         [0, 5, 0, 0, 0],
         [0, 0, 5, 0, 0],
         [0, 0, 0, 5, 0],
         [0, 0, 0, 0, 5]]
norm_var = multivariate_normal(mean=mu, cov=s)

# Connect to the Database
db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user=user,         # your username
                     passwd=psswd, # your password
                     db=db_name)        # the database
cursor = db.cursor()

# Multi-arm bandit variables
mu_R = np.zeros((K, 1))  # Mean reward for each mode
n = np.zeros((K, 1))  # Times each mode has been selected

# Manual sweep of all states 4 times
for i in range(0, 4):
    for state in range(0, K):
        try:
            # Get RSSI
            rewards = norm_var.rvs()
            RSSI = rewards[state]
            n[state] += 1
            mu_R[state] = (mu_R[state] * (n[state] - 1) + RSSI) / (n[state])

            # Create timestamp
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            # Send
            cursor.execute("""INSERT into rala (timestampt,state,rssi) values(%s,%s,%s)""",
                           (timestamp, state, RSSI))
            db.commit()

        except:
           db.rollback()
           print("Problem writing to DB")


# Get N_samples
iter = 1
while iter < N_samples:
    # Get RSSI
    rewards = norm_var.rvs()

    # Choose the state based on MAB - UCB1
    state = np.argmax(mu_R + np.sqrt(2 * np.log(iter) / n))

    # Update the reward for that state
    RSSI = rewards[state]
    n[state] += 1
    mu_R[state] = (mu_R[state] * (n[state] - 1) + RSSI) / (n[state])

    # Create timestamp
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    try:
       cursor.execute("""INSERT into rala (timestampt,state,rssi) values(%s,%s,%s)""",
                      (timestamp,state,RSSI))
       db.commit()
       iter += 1

    except:
       db.rollback()
       print("Problem writing to DB")


db.close()
