SET IDENTITY_INSERT node ON;

INSERT node (node_id, properties) 
VALUES 
	(1, '{"name": "Nate Taylor", "type": "person", "age": 38}'),
	(2, '{"name": "Jon Miller", "type": "person", "age": 40}'),
	(3, '{"name": "MIIS", "type": "place", "address": {"city": "Montery", "state": "CA"}, "lat": 36.59948, "long": -121.89673}');

