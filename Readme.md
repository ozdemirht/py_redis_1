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

References
----------
https://crashedmind.github.io/PlantUMLHitchhikersGuide/layout/layout.html

How to connect to Redis by redis-cli?
redis-cli -h 127.0.0.1 -p 6379

How to connect to Redis by Redis Insights?
Redis Insights : http://localhost:6379
