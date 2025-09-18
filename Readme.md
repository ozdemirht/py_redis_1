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
              [-90,35],
              [-90,30],
              [-85,30],
              [-85,35],
              [-90,35]
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
@include "./setup/docker-compose.yml"

<div>
{% capture p1 %}{% include ./setup/docker-compose.yml %}{% endcapture %}
{{ p1 | markdownify }}
</div>
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
