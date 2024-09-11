/*
Query Creation Date: 4/30/2024
Example query for structuring data to identify when two entities are connected
by a common feature. In this case, persons connected by a location. Suitable for 
creating an edge table for generating a network diagram.

POC is:
--Jonathan Miller
--Crime Data Analyst
--Portland Police Bureau, Strategic Services Division
--Contact via LinkedIn: https://www.linkedin.com/in/jonathanmiller3/
*/

/*Presumed Table Formats*/
--place: [place_id, place_name]
--place_person: [place_id, person_id]
--person: [person_id, person_name]

/*Establish table to contain output*/
SET ANSI_NULLS ON;
SET NOCOUNT ON;
SET QUOTED_IDENTIFIER ON;
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

DECLARE @CONNECTION TABLE (p1 NVARCHAR(MAX), p2 NVARCHAR(MAX));

/*Create temp table that contains a list of relevant person and location data, brought together by the place_person connecting table.*/  
SELECT pl.place_id, pl.place_name, pr.person_id, pr.person_name
INTO #CUP
FROM place pl
LEFT JOIN place_person pp ON pl.place_id = pp.place_id
LEFT JOIN person pr ON pp.person_id = pr.person_id;

/*Join the temp table to itself to create rows that contain connected people. This dataset will contain non-duplicate rows that represent
the same relationship. For example:
[p1]  [p2]
 A     B
 B     A

To correct for this, the case statements are used to force the p1 to always contain the id with the greatest value, and p2 to always
contain the id with the lowest value, thereby forcing the rows to be duplicate. Using the example above, it forces that table to look
like:
[p1]  [p2]
 B     A
 B     A

The use of SELECT DISTINCT then eliminates duplicate rows, thereby ensuring the edge between connected entities is only included in
the table 1 time.

This transformation is only needed here because this is a non-directional network. In cases where the "from" and the "to" sides of the
relationship matter, you would not use these case statements so as to retain the different relationships. For example:
	
If you just want to visualize that Jack and Jill are friends generally, you would use the case statements as the statements "Jack is friends with Jill"
and "Jill is friends with Jack" are meaningfully identical. 
	
If you want to visualize Jack and Jill sending eachother messages, you would not use the case statements as the statments "Jack called Jill"
and "Jill called Jack" are meaningfully different.
*/
INSERT INTO @CONNECTION
SELECT DISTINCT CASE WHEN a.person_id >= b.person_id 
THEN a.person_id 
ELSE b.person_id 
END AS ‘p1’, 
CASE WHEN a.person_id >= b.person_id 
THEN b.person_id 
ELSE a.person_id 
END AS ‘p2’
FROM #CUP a
LEFT JOIN #CUP b ON a. place_id = b. place_id;

/*Select the output of the above table to view it*/
SELECT c.*
FROM @CONNECTION c;

/*Eliminae #CUP when it's no longer required*/
DROP TABLE #CUP;
