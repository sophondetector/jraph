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

        node_id, properties_raw = cur.fetchone()

        properties = json.loads(properties_raw)

        kml = simplekml.Kml()

        kml.newpoint(
            name=properties.get("name"),
            description=properties.get('type'),
            coords=[(properties.get("lat"), properties.get("long"))]
        )

        return kml.kml()


if __name__ == '__main__':
    with dbc.init_jraph_conn():
        app.run(debug=True)
