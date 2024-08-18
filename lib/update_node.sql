UPDATE node
SET properties = json_modify(properties, '$.Age', 100)
WHERE json_value(properties, '$.Name')='Jon';
