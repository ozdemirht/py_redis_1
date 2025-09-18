import redis
import random
import time
from datetime import datetime, timedelta


def run_test():
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