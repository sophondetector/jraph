import json
import simplekml
from flask import Flask, request

import dbc

app = Flask("jraph")


@app.route("/", methods=["GET"])
def main():
    # for ids, 1=nate, 2=jon, 3=MIIS
    with dbc.get_conn().cursor() as cur:
        cur.execute("SELECT * FROM node WHERE node_id=?;",
                    request.args.get("node_id"))

        row = cur.fetchone()

        kml = simplekml.Kml()

        raw = json.loads(row[1])

        pnt = kml.newpoint(
            name=raw['name'],
            description=raw['type'],
            coords=[(raw['lat'], raw['long'])]
        )

        return kml.kml()

        # print(kml.kml())

        # kml.save("output.kml")
        # print("saved to output.kml")

        # print("finito")


if __name__ == '__main__':
    with dbc.init_jraph_conn():
        app.run(debug=True)
