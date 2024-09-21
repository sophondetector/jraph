DELETE FROM node WHERE node_id = 1;

DELETE FROM node WHERE json_value(properties, '$.Name') = 'Jon';

DELETE FROM node
WHERE json_value(properties, '$.Name') = 'Jon'
AND json_value(properties, '$.Label') = 'Person';
