import json
from dbc import init_jraph_conn
import simplekml

with init_jraph_conn() as conn:
    cur = conn.cursor()

    # 3 is the MIIS id
    cur.execute("SELECT * FROM node WHERE node_id=3;")

    row = cur.fetchone()

    kml = simplekml.Kml()

    raw = json.loads(row[1])

    pnt = kml.newpoint(
        name=raw['name'],
        description=raw['type'],
        coords=[(raw['lat'], raw['long'])]
    )

    print(kml.kml())

    # kml.save("output.kml")
    # print("saved to output.kml")

    print("finito")
