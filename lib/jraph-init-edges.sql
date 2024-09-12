SET IDENTITY_INSERT edge ON;

INSERT edge (edge_id, source_id, target_id, properties) 
VALUES 
	(1, 1, 3, '{"type": "attended", "focus": "nonproliferation"}'),
	(2, 1, 2, '{"type": "friends with"}'),
	(3, 2, 1, '{"type": "friends with"}'),
	(4, 2, 3, '{"type": "attended", "focus": "terrorism"}');

