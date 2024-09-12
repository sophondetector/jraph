/*
Query Creation Date: 5/02/2024
Allows one to generate a simple kml map of points based upon a table of data.
POC is:
--Jonathan Miller
--Crime Data Analyst
--Portland Police Bureau, Strategic Services Division
--Contact via LinkedIn: https://www.linkedin.com/in/jonathanmiller3/ 

Description:	Creates a kml file for use in google earth. Save the output in a .txt file and then change the extension to .kml. 
              It requires use of the rapid_map userdefined table type, which consists of the following columms:
									Field Name			Field Type				Entry Format				Field Description
								    point_name			NVARCHAR(MAX)			TEXT						Name of the location
								    point_description	NVARCHAR(MAX)			TEXT						Descrition of the location
								    str_datetime		DATETIME				DATETIME					when the point starts
								    end_datetime		DATETIME				DATETIME					when the point ends 
								    lat					FLOAT					0.0							Latitude
								    lon					FLOAT					0.0							Longitude
								    elevation_meters	FLOAT					0.0							Elevation in meters.
								    radius_meters		FLOAT					0.0							accuracy radius in meters. The map will draw this around the point
									speed				FLOAT					0.0							Speed. Will change colors blue to red when speed is >=3.
																											3 miles an hour is the average walking speed of a human. The color change
																											makes it easier to distinguish between stationairy and moving entities.
*/
/*Create data table*/
SET ANSI_NULLS ON;
SET NOCOUNT ON;
SET QUOTED_IDENTIFIER ON;
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
DECLARE @rapid_map TABLE (point_name NVARCHAR(MAX),point_description NVARCHAR(MAX),str_datetime DATETIME,end_datetime DATETIME,lat FLOAT,lon FLOAT, elevation_meters FLOAT,radius_meters FLOAT,speed FLOAT);
INSERT INTO @rapid_map VALUES
	('Point 01','Description 01','2024-04-30 10:00:00.000','2024-04-30 10:00:59.000','45.52213258356169','-122.6844328257541','0','10','0'),
	('Point 02','Description 02','2024-04-30 10:01:00.000','2024-04-30 10:01:59.000','45.52186383547212','-122.6834574922921','0','10','1'),
	('Point 03','Description 03','2024-04-30 10:02:00.000','2024-04-30 10:02:59.000','45.5211952017553' ,'-122.6837785882264','0','10','2'),
	('Point 04','Description 04','2024-04-30 10:03:00.000','2024-04-30 10:03:59.000','45.52091841401852','-122.6827729246763','0','10','3'),
	('Point 05','Description 05','2024-04-30 10:04:00.000','2024-04-30 10:04:59.000','45.52031245525673','-122.6830552559341','0','10','4'),
	('Point 06','Description 06','2024-04-30 10:05:00.000','2024-04-30 10:05:59.000','45.52004748547911','-122.682068022142' ,'0','10','2'),
	('Point 07','Description 07','2024-04-30 10:06:00.000','2024-04-30 10:06:59.000','45.51934098492055','-122.6824690445624','0','10','3');
		
/*create styles and file data*/
	DECLARE @STYLE1 XML =  (SELECT 'IconStyle01'  AS '@id' , 'ff0000ff' AS 'IconStyle/color', '1' AS 'IconStyle/scale','http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png' AS 'IconStyle/Icon/href',
	                                                         '7f0000ff' AS 'PolyStyle/color',
															 '0' AS 'LabelStyle/scale' FOR XML PATH ('Style'),TYPE);
	DECLARE @STYLE2 XML =  (SELECT 'IconStyle02'  AS '@id' , 'ffff0000' AS 'IconStyle/color', '1' AS 'IconStyle/scale','http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png' AS 'IconStyle/Icon/href',
	                                                         '7fff0000' AS 'PolyStyle/color',
															 '0' AS 'LabelStyle/scale'  FOR XML PATH ('Style'),TYPE);
	DECLARE @FILENAME XML = (SELECT CONCAT('Rapid Map : ',FORMAT(GETDATE(),'yyyy-MM-dd HH:mm:ss')) FOR XML PATH('name'),TYPE);

/*Create linestring for accuracy radius*/
	DECLARE @TEMP1  TABLE (point_name NVARCHAR(MAX),point_description NVARCHAR(MAX), str_datetime DATETIME, end_datetime DATETIME,lat FLOAT, lon FLOAT, elevation_meters FLOAT, radius_meters FLOAT, speed FLOAT,BUFFERS_TEXT NVARCHAR(MAX),poly_string NVARCHAR(MAX));
	INSERT INTO @TEMP1 

	SELECT s.*,'poly_string' = REPLACE(REPLACE(REPLACE(REPLACE(s.Buffers_Text,'Polygon ((',''),' ',','),',,',',0 '),'))',',0')
	FROM(
		SELECT a.*,'Buffers_Text' = GEOGRAPHY::STPointFromText(CONCAT('POINT(',CONVERT(VARCHAR(MAX),CONVERT(DECIMAL(30,11),a.lon)),' ',CONVERT(VARCHAR(MAX),CONVERT(DECIMAL(30,11),a.lat)),')'),4326).STBuffer(a.radius_meters).STAsText()
		FROM @rapid_map a  
		) s;
	
/*assemble point and polygon kml strings*/
	DECLARE @TEMP2 TABLE (point_name NVARCHAR(MAX),point_description NVARCHAR(MAX), str_datetime DATETIME, end_datetime DATETIME,lat FLOAT, lon FLOAT, elevation_meters FLOAT, radius_meters FLOAT, speed FLOAT,BUFFERS_TEXT NVARCHAR(MAX),poly_string NVARCHAR(MAX),
			name XML,description XML,TimeSpan XML,point_data XML,poly_data XML);
	INSERT INTO @TEMP2
	SELECT a.*,
	       (SELECT CAST(a.point_name AS VARCHAR) FOR XML PATH('name'),       TYPE),
		   (SELECT a.point_description           FOR XML PATH('description'),TYPE),
		   (SELECT CONCAT(FORMAT(a.str_datetime,'yyyy-MM-dd'),'T',FORMAT(a.str_datetime,'HH:mm:ss'),'Z') AS 'begin',
	               CONCAT(FORMAT(a.end_datetime,'yyyy-MM-dd'),'T',FORMAT(a.end_datetime,'HH:mm:ss'),'Z') AS 'end'
	                                            FOR XML PATH('TimeSpan'),    TYPE),
			CAST((SELECT CONCAT(CONVERT(VARCHAR(MAX),CONVERT(DECIMAL(30,12),a.lon)),',',CONVERT(VARCHAR(MAX),CONVERT(DECIMAL(30,13),a.lat)),',',a.elevation_meters)
			                                    FOR XML PATH('coordinates'),Root('Point')) AS XML),
			CAST((SELECT a.poly_string AS 'LinearRing/coordinates'
												FOR XML PATH('outerBoundaryIs'),Root('Polygon')) AS XML)
	FROM @TEMP1 a;

/*Assemble multigeometry placemarks. Include caveat where speed > 2 change style*/
	DECLARE @TEMP3 TABLE (loc_output XML);
	INSERT INTO @TEMP3
	SELECT 
		(SELECT
			CAST(a.name AS XML),
	        CAST(a.description AS XML),
			(SELECT CAST(a.name AS XML),
				    CAST(a.TimeSpan AS XML),
				    CASE WHEN a.speed > 2 THEN'#IconStyle01' ELSE '#IconStyle02' END AS 'styleUrl',
				    CAST(a.point_data AS XML)
		    FOR XML PATH('Placemark'),TYPE), 
			(SELECT CAST(a.name AS XML),
				   CAST(a.TimeSpan AS XML),
				   CASE WHEN a.speed > 2 THEN'#IconStyle01' ELSE '#IconStyle02' END AS 'styleUrl',
				   CAST(a.poly_data AS XML)
		    FOR XML PATH('Placemark'),TYPE) FOR XML PATH('Folder'),TYPE) AS 'loc_output'
	FROM @TEMP2 a;

/*results*/
	DECLARE @QUERYRESULT XML = (SELECT 'Locations' AS 'name',(SELECT CAST(a.loc_output AS XML) FROM @TEMP3 a FOR XML PATH(''),TYPE) FOR XML PATH ('Folder'),TYPE);
/**/
	DECLARE @FINAL XML = (
	SELECT @FILENAME,
	       @STYLE1,
	       @STYLE2,
		   @QUERYRESULT
	FOR XML PATH('Document'),root('kml'));
	--Create final table
		SELECT @FINAL;
