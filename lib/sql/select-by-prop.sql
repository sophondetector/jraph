SELECT node_id FROM node WHERE json_value(properties, '$.address') LIKE 'Lotus%';
