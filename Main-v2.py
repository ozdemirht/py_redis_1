
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
    print("ID of process running task 2: {}".format(os.getpid()))

    # Simulate for 1 hour (3600 seconds), update every 10 seconds
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)

    current_time = start_time
    step = 0

    while current_time < end_time:
        # Random small movement (lat ~111km per degree, lon ~85km near SF)
        lat += random.uniform(-0.0002, 0.0002)  # ≈ ±20m north/south
        lon += random.uniform(-0.00025, 0.00025)  # ≈ ±20m east/west

        # Update driver location in Redis
        myRedis.geoadd(myKey, (lon, lat, driver_id))

        #print(f"[{current_time.strftime('%H:%M:%S')}] Step {step} → Pos=({lat:.5f},{lon:.5f}) Nearby={nearby}")
        #print(f"[{current_time.strftime('%H:%M:%S')}] Step {step} → Pos=({lat:.5f},{lon:.5f}) ")
        logging.debug(f"[{current_time.strftime('%H:%M:%S')}] Step {step} of {driver_id} → Pos=({lat:.5f},{lon:.5f}) ")

        # Wait 10s
        time.sleep(10)
        current_time += timedelta(seconds=10)
        step += 1

def run_test():
    # Connect to Redis
    r = redis.Redis(host="localhost", port=6379, db=0)
    #r = redis.Redis(host="172.17.0.2", port=6379, db=0)

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

    for i, x in enumerate(sims):
        logging.debug(f"Starting Sim-{i}!")
        x.start()

    for i, x in enumerate(sims):
        x.join()
        logging.debug(f"Sim-{i} has joined!")

    logging.debug(f"Done! "+__name__)


def run_test2():
    # Connect to Redis
    r = redis.Redis(host="localhost", port=6379, db=0)
    #r = redis.Redis(host="172.17.0.2", port=6379, db=0)

    KEY = "drivers"

    # Clear old data
    r.delete(KEY)

    # Driver initial position (Union Square SF)
    lat, lon = 37.7879, -122.4074
    driver_id = "DriverA"

    # Simulate for 1 hour (3600 seconds), update every 10 seconds
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)

    current_time = start_time
    step = 0

    while current_time < end_time:
        # Random small movement (lat ~111km per degree, lon ~85km near SF)
        lat += random.uniform(-0.0002, 0.0002)  # ≈ ±20m north/south
        lon += random.uniform(-0.00025, 0.00025)  # ≈ ±20m east/west

        # Update driver location in Redis
        r.geoadd(KEY, (lon, lat, driver_id))

        # Query for nearby drivers within 500m
        nearby = r.geosearch(
            KEY,
            longitude=lon,
            latitude=lat,
            radius=50000,
            unit="km",
            sort="ASC"
        )

        print(f"[{current_time.strftime('%H:%M:%S')}] Step {step} → Pos=({lat:.5f},{lon:.5f}) Nearby={nearby}")

        # Wait 10s
        time.sleep(10)
        current_time += timedelta(seconds=10)
        step += 1


if __name__ == "__main__":
    run_test()