-- not sure what this does; yanked from SO
SELECT  d.plan_handle ,
        d.sql_handle ,
        e.text
FROM    sys.dm_exec_query_stats d
        CROSS APPLY sys.dm_exec_sql_text(d.plan_handle) AS e
WHERE e.text like '%something%';

--selects from current default trace file
SELECT * FROM ::fn_trace_getinfo(default);

--selects from some specific trace file
SELECT * FROM fn_trace_gettable('/var/opt/mssql/log/log_5.trc', default);

-- https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-readerrorlog-transact-sql?view=sql-server-ver16
-- ^^^ more t sql functions

-- t sql doesn't use limit
SELECT SalesOrderID, OrderDate
FROM Sales.SalesOrderHeader 
ORDER BY SalesOrderID
    OFFSET 10 ROWS
    FETCH NEXT 10 ROWS ONLY;

-- t sql doesn't use limit
SELECT TOP 10 * FROM node;

