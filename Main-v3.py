#from django.db.models.functions import NullIf
#from encodings.punycode import selective_find

import redis
import os
import random
import time
from datetime import datetime, timedelta
import threading
import logging
import logging.config


class updateLocationMS:
    def updateMyLocation(self):
        pass

class queryNearByMS():
    def queryNearByEntities(self):
        pass

class updateLocationRedis(updateLocationMS):
    def __init__(self,myKey, myRedis):
        #super.__init__(self)
        self.myKey = myKey
        self.myRedis = myRedis

    def updateMyLocation(self,my_lon, my_lat, my_id):
        """ Encapsulates details of Redis I/F """
        try:
            self.myRedis.geoadd(self.myKey,(my_lon,my_lat,my_id))
        except:
            print(f"Error updating location: redis.geoadd({self.myKey},{my_lon},{my_lat},{my_id})")

class queryNearByRedis(queryNearByMS):
    def __init__(self,myKey, myRedis):
        self.myKey = myKey
        self.myRedis = myRedis

    def queryNearByEntities(self,lon,lat,radius):
        return self.myRedis.geosearch(
            self.myKey,
            longitude=lon,
            latitude=lat,
            radius=radius,
            unit="m",
            sort="ASC"
        )


class SimDeliveryAgent(threading.Thread):
    def __init__(self,my_lat, my_lon, my_id, locationUpdater):
        threading.Thread.__init__(self, target=self.run, daemon=False)
        self.lat = my_lat
        self.lon = my_lon
        self.driver_id = my_id
        #self.myKey = myKey
        #self.myRedis = myRedis
        self.locationUpdater = locationUpdater

    def getName(self):
        return self.driver_id

    def run(self):
        print("Starting SimDeliveryAgent")
        self.emulate()
        print("Completed SimDeliveryAgent")
        return

    def emulate(self):
        lat = self.lat
        lon = self.lon
        driver_id = self.driver_id

        print("Task 2 assigned to thread: {}".format(threading.current_thread().name))
        # print("ID of process running task 2: {}".format(os.getpid()))

        # Simulate for 1 hour (3600 seconds), update every 10 seconds
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=1)

        current_time = start_time
        step = 0

        while current_time < end_time and (step < 10):
            # Random small movement (lat ~111km per degree, lon ~85km near )
            lat += random.uniform(-0.0002, 0.0002)  # ≈ ±20m north/south
            lon += random.uniform(-0.00025, 0.00025)  # ≈ ±20m east/west

            rsleep_seconds = random.uniform(1, 4)
            time.sleep(rsleep_seconds)

            # Update driver's location
            self.locationUpdater.updateMyLocation(lon, lat, driver_id)

            # print(f"[{current_time.strftime('%H:%M:%S')}] Step {step} → Pos=({lat:.5f},{lon:.5f}) Nearby={nearby}")
            print(f"[{current_time.strftime('%H:%M:%S')}] Step {step} of {driver_id} → Pos=({lat:.5f},{lon:.5f}) ")
            logging.debug(
                f"[{current_time.strftime('%H:%M:%S')}] Step {step} of {driver_id} → Pos=({lat:.5f},{lon:.5f}) ")

            # Wait 10s
            time.sleep(10 - rsleep_seconds)
            current_time += timedelta(seconds=10)
            step += 1

class SimUser(threading.Thread):
    def __init__(self,my_lat, my_lon, my_id, findNearBy):
        threading.Thread.__init__(self, target=self.run, daemon=False)
        self.lat = my_lat
        self.lon = my_lon
        self.user_id = my_id
        self.findNearBy = findNearBy

    def getName(self):
        return self.user_id

    def run(self):
        print(f"Starting SimUser-{self.getName()}")
        self.emulate()
        print(f"Completed SimUser-{self.getName()}")
        return

    def emulate(self):
        user_id = self.user_id
        lat = self.lat
        lon = self.lon

        # Simulate for 1 hour (3600 seconds), update every 10 seconds
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=1)

        current_time = start_time
        step = 0

        while current_time < end_time and (step < 5):
            # Random small movement (lat ~111km per degree, lon ~85km near SF)
            lat += random.uniform(-0.00002, 0.00002)  # ≈ ±2m north/south
            lon += random.uniform(-0.000025, 0.000025)  # ≈ ±2m east/west

            # Query for nearby drivers within 500m
            radius = random.uniform(50, 500)
            nearby = self.findNearBy.queryNearByEntities(lon, lat, radius)
            print(
                f"[{current_time.strftime('%H:%M:%S')}] Step {step} of {user_id} → Pos=({lat:.5f},{lon:.5f},{radius:.2f}) Nearby={nearby}")

            # Wait 30s
            time.sleep(20)
            current_time += timedelta(seconds=20)
            step += 1


def run_test(k = 3, usrn = 2):
    # Connect to Redis
    r = redis.Redis(host="localhost", port=6379, db=0)
    #r = redis.Redis(host="172.17.0.3", port=6379, db=0)

    KEY = "drivers"

    # Clear old data
    r.delete(KEY)

    # Driver initial position (... New York, New York)
    lat, lon = 37.7879, -122.4074

    sims = list()
    # Initiate K deliveryAgents
    for i in range(k):
        nlat = lat + random.uniform(-0.0002, 0.0002)  # ≈ ±20m north/south
        nlon = lon + random.uniform(-0.00025, 0.00025)  # ≈ ±20m east/west
        sims.append(SimDeliveryAgent( nlat,nlon
                                     , "deliveryAgent-{}".format(i)  ## Name
                                     , updateLocationRedis(KEY, r))) ## Location Update I/F

    ##
    usr  = list()
    # Initiate USRN Users/Walkers
    for i in range(usrn):
        nlat = lat + random.uniform(-0.00002, 0.00002)  # ≈ ±2m north/south
        nlon = lon + random.uniform(-0.00025, 0.00025)  # ≈ ±20m east/west
        usr.append(SimUser(nlat, nlon, "user-{}".format(i), queryNearByRedis(KEY, r)))

    print("Let's run delivery agents!")
    for sa in sims:
        logging.debug(f"Starting {sa.getName()}!")
        print(f"Starting {sa.getName()}!")
        sa.start()

    print("Let's run users!")
    for user in usr:
        logging.debug(f"Starting User-Sim-{user.getName()}!")
        print(f"Starting User-Sim-{user.getName()}!")
        user.start()

    print("Let's wait delivery agents to finish!")
    for sa in sims:
        sa.join()
        logging.debug(f"Sim-{sa.getName()} has joined!")
        print(f"Sim-{sa.getName()} has joined!")

    print("Let's wait users to finish!")
    for user in usr:
        user.join()
        logging.debug(f"User-Sim-{user.getName()} has joined!")
        print(f"User-Sim-{user.getName()} has joined!")

    logging.debug(f"Done! "+__name__)
    print(f"Done! "+__name__)
    return 0


if __name__ == "__main__":
    run_test()
