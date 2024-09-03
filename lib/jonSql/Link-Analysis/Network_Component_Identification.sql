/*
Query Creation Date: 4/30/2024
Allows one to assign referencable ID's to indidvidual network components containing two or more
network components. Useful when it is desirable to confine analysis to nodes within a specific
network componet rather than an entire network. 
POC is:
--Jonathan Miller
--Crime Data Analyst
--Portland Police Bureau, Strategic Services Division
--Contact via LinkedIn: https://www.linkedin.com/in/jonathanmiller3/
*/

--(1) Establish Edge List and Distinct Llist of Nodes
SET ANSI_NULLS ON;
SET NOCOUNT ON;
SET QUOTED_IDENTIFIER ON;
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
	DECLARE @EDGES TABLE (node_a NVARCHAR(100),node_b NVARCHAR(100));
		INSERT INTO @EDGES VALUES (1,2),(1,3),(2,3),(3,4)
								 ,(5,6),(5,7)
								 ,(8,9);
	DECLARE @NODES TABLE (node NVARCHAR(100));
		INSERT INTO @NODES 
			SELECT DISTINCT a.* 
			FROM (SELECT node_a FROM @EDGES UNION SELECT node_b FROM @EDGES) a;

--(2) Identify network components (NC) with loop	
	DECLARE @NC_TABLE TABLE(nc_id INT,node NVARCHAR(100));
	DECLARE @NC_ID INT = 0;
	DECLARE @node NVARCHAR(100) = (SELECT node FROM @NODES WHERE CAST(node AS BIGINT) = (SELECT MIN(CAST(node AS BIGINT)) FROM @NODES));
	
	/*First loop id's nodes directly connected to @Node, subsequent loops identifes nodes connected to those, etc etc.
		Removal of edges at end of loop provides a trigger to move on to the next set of nodes in the component. Once nothing in the edge table 
		connects to nodes already inserted into @NC_Table, found nodes are removed from the @NODES reference, the @NC_ID iterates +1 and the
		process starts again with the node with the new lowest identifier. */
	WHILE (CAST(@node AS BIGINT) <= (SELECT MAX(CAST(node AS BIGINT)) FROM @NODES))
	BEGIN
		SELECT @NC_ID = @NC_ID + 1;	
		INSERT INTO @NC_TABLE SELECT @NC_ID,@node;
		WHILE (SELECT COUNT(node_a) FROM @EDGES WHERE node_a IN (SELECT node FROM @NC_TABLE) OR node_b IN (SELECT node FROM @NC_TABLE)) <> 0
			BEGIN
				/*Add any nodes to the current network component (@NC_ID) when it is connected to something already in @NC_TABLE and has not been added previously*/
				INSERT INTO @NC_TABLE 
					SELECT DISTINCT @NC_ID AS 'nc_id', aa.node FROM (					
					SELECT DISTINCT node_a AS 'node' FROM @EDGES WHERE node_b IN (SELECT node FROM @NC_TABLE) AND node_a NOT IN (SELECT node FROM @NC_TABLE)
					UNION
					SELECT DISTINCT node_b AS 'node' FROM @EDGES WHERE node_a IN (SELECT node FROM @NC_TABLE) AND node_b NOT IN (SELECT node FROM @NC_TABLE)
					) aa;
				/*Once complete, remove all connections that include a node identified by the loop from the @EDGES.*/
				DELETE FROM @EDGES WHERE node_a IN (SELECT node FROM @NC_TABLE) AND node_b IN (SELECT node FROM @NC_TABLE);
			END
		/*Remove nodes already found from node reference before re-establishing new target node*/
		DELETE FROM @NODES WHERE node IN (SELECT node FROM @NC_TABLE);
		SELECT @node = (SELECT node FROM @NODES WHERE CAST(node AS BIGINT) = (SELECT MIN(CAST(node AS BIGINT)) FROM @NODES));
	END	

--(3) SELECT OUTPUT
	SELECT * FROM @NC_TABLE;

--(4) Additional Example: Identify Nodes in Largest Network Component (LNC)	
	DECLARE @MAXCNT INT = (SELECT MAX(n_count)
							FROM (SELECT nc_id, COUNT(node) AS 'n_count' 
								  FROM @NC_TABLE
								  GROUP BY nc_id
								 ) s
							);
	DECLARE @LNC INT = (SELECT s.nc_id
					    FROM(SELECT nc_id, COUNT(node) AS 'n_count' 
							 FROM @NC_TABLE
							 GROUP BY nc_id
							 ) s
						WHERE n_count = @MAXCNT
						);
	SELECT * 
	FROM @NC_TABLE a 
	WHERE a.nc_id = @LNC;
