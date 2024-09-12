SELECT properties FROM node WHERE node_id = 1;

SELECT properties FROM node WHERE json_value(properties, '$.Name')='Jon';

SELECT properties FROM node WHERE json_value(properties, '$.Label')='Person';
