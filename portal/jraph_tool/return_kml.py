from dbc import init_jraph_conn
import simplekml

with init_jraph_conn() as conn:
    cur = conn.cursor()
    # 3 is the MIIS id
    cur.execute("SELECT * FROM node WHERE node_id=3;")
    row = cur.fetchone()
    kml = simplekml.Kml()
    pnt = kml.newpoint(**row)
    print(kml.kml())
