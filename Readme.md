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
</details>


Run redis-cli

Run main.py

![](./docs/HLD-1.png)
Figure 1: High Level Diagram

Verify
------
Program simulates the motion of multiple vehicles.
Occasional nearby queries list the delivery agents within the given radius.


How to connect to Redis by redis-cli?
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
</verbatim>
</details>

How to connect to Redis by Redis Insights?
- 
Redis Insights : http://localhost:6379

References
----------
https://crashedmind.github.io/PlantUMLHitchhikersGuide/layout/layout.html
