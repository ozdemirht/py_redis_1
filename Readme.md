Introduction
------------

```geojson
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": 1,
      "properties": {
        "ID": 0
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
              [-74.3,40.55],
              [-74.3,40.15],
              [-74.8,40.15],
              [-74.8,40.55],
              [-74.3,40.55]
          ]
        ]
      }
    }
  ]
}
```

Setup
-----
Run redis

<details>
<summary>docker-compose.yml</summary>
<verbatim>
version: '3.8'
services:
  redis:
    image: redis
    ports:
      - "6379:6379"
    command: redis-server --protected-mode no
</verbatim>
</details>


Run redis-cli

Run main.py

**SimDeliveryAgent**: Simulates movements of a delivery agent who updates its location via updateLocationMS/Redis. 
Because class **SimDeliveryAgent** extends from threading.Thread, each instance has its own thread. 

**SimUser**: Simulates movements of a rider who also checks for nearby delivery agents (queryNearbyMS). 
Because class **SimUser** extends from threading.Thread, each instance has its own thread. 

![](./docs/HLD-1.png)
Figure 1: High Level Diagram

[Redis GEOSEARCH](https://redis.io/docs/latest/commands/geosearch/) comes with two flavours that impact how the system handle location of entities.
GEOSEARCH can use given location (longitude,latitude) and radius. Beyond the given coordinates, there is nothing shared with Redis. 
GEOSEARCH can use member identifier and radius. Because Redis stores the location of given member, it can translate the request to the above GEOSEARCH. 
In this case, system needs to share the location of user entities. This increases the number of update location requests. 
This implementation decision also requires verification with legal department due to data protection regulations and laws.

[Redis GEOADD](https://redis.io/docs/latest/commands/geoadd/) adds/updates the **last location** of an entity, (lon,lat,member_id). 
For the details of Redis geohashing implementation (52 bits) see [Redis GEOADD](https://redis.io/docs/latest/commands/geoadd/) 
and [Sorted Set](https://redis.io/docs/latest/develop/data-types/sorted-sets/).

Verify
------
Program simulates the motion of multiple vehicles.
Occasional nearby queries list the delivery agents within the given radius.


How to connect to Redis by redis-cli?
--
```bash
  redis-cli -h 127.0.0.1 -p 6379
```

<details>
<summary>Helpful redis-cli commands</summary>
<verbatim>
> KEYS d* <br>
> ZRANGE drivers 0 -1 <br>
> GEOPOS drivers deliveryAgent-0 <br>
> GEOPOS drivers deliveryAgent-1 <br>
> GEOPOS drivers deliveryAgent-2 <br>
> GEOHASH drivers deliveryAgent-0 <br>
> GEOHASH drivers deliveryAgent-1 <br>
> GEOHASH drivers deliveryAgent-2 <br>
> GEOSEARCH drivers FROM LONLAT -122.4 37.8 BYRADIUS 5000 M
> GEOSEARCH drivers FROM LONLAT -122.4 37.8 BYRADIUS 5000 M WITHDIST WITHHASH WITHCOORD
> GEOSEARCH drivers FROMMEMBER User-1 BYRADIUS 5000 M WITHDIST WITHHASH WITHCOORD
</verbatim>
</details>

How to connect to Redis by Redis Insight?
- 
RedisInsight : http://localhost:5540

References
----------
1. [Redis GEOSEARCH](https://redis.io/docs/latest/commands/geosearch/)
1. [Redis Sorted Set](https://redis.io/docs/latest/develop/data-types/sorted-sets/)
1. [Redis GEOADD](https://redis.io/docs/latest/commands/geoadd/)
1. https://crashedmind.github.io/PlantUMLHitchhikersGuide/layout/layout.html
