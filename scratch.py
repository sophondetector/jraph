import simplekml as sk
from jtool import Node, dbc

kml = sk.Kml()
kml.newpoint(name="Kirstenbosch", coords=[(18.432314, -33.988862)])

n = dbc.query_node(169177)
