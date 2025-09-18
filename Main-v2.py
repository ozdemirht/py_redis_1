
import redis
import os
import random
import time
from datetime import datetime, timedelta
import threading
import logging
import logging.config

def emulate_aDeliveryAgent(my_lat, my_lon, my_id, myKey, myRedis):
    lat = my_lat
    lon = my_lon
    driver_id = my_id

    print("Task 2 assigned to thread: {}".format(threading.current_thread().name))
    #print("ID of process running task 2: {}".format(os.getpid()))

    # Simulate for 1 hour (3600 seconds), update every 10 seconds
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)

    current_time = start_time
    step = 0

    while current_time < end_time and (step<10):
        # Random small movement (lat ~111km per degree, lon ~85km near )
        lat += random.uniform(-0.0002, 0.0002)  # ≈ ±20m north/south
        lon += random.uniform(-0.00025, 0.00025)  # ≈ ±20m east/west

        rsleep_seconds = random.uniform(1, 4)
        time.sleep(rsleep_seconds)

        # Update driver location in Redis
        myRedis.geoadd(myKey, (lon, lat, driver_id))

        #print(f"[{current_time.strftime('%H:%M:%S')}] Step {step} → Pos=({lat:.5f},{lon:.5f}) Nearby={nearby}")
        print(f"[{current_time.strftime('%H:%M:%S')}] Step {step} of {driver_id} → Pos=({lat:.5f},{lon:.5f}) ")
        logging.debug(f"[{current_time.strftime('%H:%M:%S')}] Step {step} of {driver_id} → Pos=({lat:.5f},{lon:.5f}) ")

        # Wait 10s
        time.sleep(10-rsleep_seconds)
        current_time += timedelta(seconds=10)
        step += 1


def emulate_aUser(my_lat, my_lon, my_id, myKey, myRedis):

    user_id = my_id
    lat = my_lat
    lon = my_lon
    KEY = myKey


    # Simulate for 1 hour (3600 seconds), update every 10 seconds
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)

    current_time = start_time
    step = 0

    while current_time < end_time and (step<5):
        # Random small movement (lat ~111km per degree, lon ~85km near SF)
        lat += random.uniform(-0.00002, 0.00002)  # ≈ ±2m north/south
        lon += random.uniform(-0.000025, 0.000025)  # ≈ ±2m east/west

        # Query for nearby drivers within 500m
        nearby = myRedis.geosearch(
            KEY,
            longitude=lon,
            latitude=lat,
            radius=0.75,
            unit="km",
            sort="ASC"
        )

        print(f"[{current_time.strftime('%H:%M:%S')}] Step {step} of {user_id} → Pos=({lat:.5f},{lon:.5f}) Nearby={nearby}")

        # Wait 30s
        time.sleep(20)
        current_time += timedelta(seconds=20)
        step += 1

def run_test():
    # Connect to Redis
    r = redis.Redis(host="localhost", port=6379, db=0)
    #r = redis.Redis(host="172.17.0.3", port=6379, db=0)

    KEY = "drivers"

    # Clear old data
    r.delete(KEY)

    # Driver initial position (Union Square SF)
    lat, lon = 37.7879, -122.4074
    k = 3
    sims = list()
    # Initiate K deliveryAgents
    for i in range(k):
        id = "deliveryAgent-{}".format(i)
        x = threading.Thread(target=emulate_aDeliveryAgent, args=(lat, lon, id, KEY, r, ))
        sims.append(x)

    usrn = 2
    usr  = list()
    # Initiate USRN Users/Walkers
    for i in range(usrn):
        id = "user-{}".format(i)
        x = threading.Thread(target=emulate_aUser, args=(lat, lon, id, KEY, r, ))
        usr.append(x)

    print("Let's run sims!")
    for i in range(len(sims)):
        logging.debug(f"Starting Sim-{i}!")
        print(f"Starting Sim-{i}!")
        sims[i].start()

    print("Let's run usr!")
    for i in range(len(usr)):
        logging.debug(f"Starting User-Sim-{i}!")
        print(f"Starting User-Sim-{i}!")
        usr[i].start()

    print("Let's wait sims to finish!")
    for i in range(len(sims)):
        sims[i].join()
        logging.debug(f"Sim-{i} has joined!")
        print(f"Sim-{i} has joined!")

    print("Let's wait user-sims to finish!")
    for i in range(len(usr)):
        usr[i].join()
        logging.debug(f"User-Sim-{i} has joined!")
        print(f"User-Sim-{i} has joined!")

    logging.debug(f"Done! "+__name__)
    print(f"Done! "+__name__)
    return 0

if __name__ == "__main__":
    run_test()