INSERT INTO edge(source_id, target_id, properties)
VALUES(
	(SELECT node_id FROM node WHERE json_value(properties, '$.Name')='Jon'),
  (SELECT node_id FROM node WHERE json_value(properties, '$.Name')='MIIS'), 
	'{"Label":"Associated with"}'
);

