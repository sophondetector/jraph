/*
Query Creation Date: 4/29/2024
POC for this example usage of SQL to produce anx files is:
--Jonathan Miller
--Crime Data Analyst
--Portland Police Bureau, Strategic Services Division
--Contact via LinkedIn: https://www.linkedin.com/in/jonathanmiller3/

To use 
--1.Run query
--2.Copy and past output into .txt file
--3.Change extention to .anx
--4.Open in Analyst's Notebook
*/

/*Source tables: This is the data to be displayed in i2*/
SET ANSI_NULLS ON;
SET NOCOUNT ON;
SET QUOTED_IDENTIFIER ON;
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

DECLARE @CASE TABLE (case_id NVARCHAR(30),case_number NVARCHAR(30),occ_date NVARCHAR(30),occ_time NVARCHAR(30),offense NVARCHAR(MAX));
	INSERT INTO @CASE VALUES 
		('1', '24-0001', '2024-01-21', '12:04', 'Offense: Assault Offenses'),
		('2', '24-0002', '2024-01-22', '11:04', 'Offense: Liquor Law Violations'),
		('3', '24-0003', '2024-01-23', '10:04', 'Offense: Arson'),
		('4', '24-0004', '2024-01-24', '09:04', 'Offense: Motor Vehicle Theft');
		
DECLARE @PERS TABLE (pers_id NVARCHAR(30), pers_name NVARCHAR(30),sex NVARCHAR(30));
	INSERT INTO @PERS VALUES
		('1', 'Jack', 'MALE'),
		('2', 'Jill', 'FEMALE'),
		('3', 'Jesse', 'UNKNOWN'),
		('4', 'Jamie', 'X');

DECLARE @CASE_PERS_LINK TABLE (case_id NVARCHAR(30), pers_id NVARCHAR(30)); 
	INSERT INTO @CASE_PERS_LINK VALUES 
		('1', '1'),
		('2', '1'),
		('2', '2'),
		('3', '1'),
		('3', '2'),
		('3', '3'),
		('4', '1'),
		('4', '2'),
		('4', '3'),
		('4', '4');

/*File supporting data*/
DECLARE @OUTPUT TABLE (
	category NVARCHAR(30),
	name NVARCHAR(30), 
	content XML,
	id_type VARCHAR(50),
	id VARCHAR(34), 
	color_name NVARCHAR(MAX),
	color_val NVARCHAR(10)
);

--(i)COLOR_TABLE_GENERATION --https://convertingcolors.com/rgb-color-0_255_255.html is a good converter.
						     --Use converter to get to decimal from RGB. However, anx requires RGB to be flipped to BGR when doing the conversion.
						     --(e.g. If RGB= (255,179,202), enter (202,179,255) into the converter)
DECLARE @COLR_REFR TABLE (color_name NVARCHAR(MAX), color_val NVARCHAR(10));
INSERT INTO @COLR_REFR VALUES
 ('Amethyst', '13395609'),
 ('Beige', '14480885'),
 ('Black', '0'),
 ('Blue', '16711680'),
 ('Bronze', '3309517'),
 ('Brown', '2763429'),
 ('Camouflage', '16777215'),
 ('Chrome', '7697781'),
 ('Copper', '3371960'),
 ('Cream/Ivory', '15794175'),
 ('Dark Blue', '9109504'),
 ('Dark Green', '25600'),
 ('Gold', '55295'),
 ('Gray', '8421504'),
 ('Green', '32768'),
 ('Lavender', '16443110'),
 ('Light Blue', '15128749'),
 ('Light Green', '9498256'),
 ('Marron/Burgundy', '2097280'),
 ('Mauve', '16756960'),
 ('Multiple Colors', '16777215'),
 ('Orange', '42495'),
 ('Pink', '13353215'),
 ('Purple', '8388736'),
 ('Red', '255'),
 ('Silver/aluminum', '12632256'),
 ('Tan', '9221330'),
 ('Taupe', '7179187'),
 ('Teal', '8421376'),
 ('Turquoise', '13688896'),
 ('White', '16777215'),
 ('Yellow', '65535');

--ENTITYTYPECOLLECTION
	--CHOOSE ICONS FROM C:\Program Files (x86)\Common Files\i2 Shared\Images 8.5\Basic\Icons
		--@ICONFILE = Icon File Name without extension
		--@NAME		= Whatever you want to reference it as in later code.
		--		      Use text selected in earlier queries to apply icons based upon defined criteria
		--            Example: see (6b)PERSONS
		--			           Person icon styles are defined by values in the person_gender column from
		--                     the person entity query. Unique icons are defined below based upon all possible
		--                     values in that column. Selecting person_gender = @TYPE within ICONSTYLE assigns
		--                     appropriate icons based upon values unique to each person.
	
DECLARE @entity_type_col_prep TABLE(Id NVARCHAR(20), name NVARCHAR(MAX), PreferredRepresentation NVARCHAR(MAX),IconFile NVARCHAR(MAX),IconShadingColour NVARCHAR(MAX));
	INSERT INTO @entity_type_col_prep VALUES 
	--Case_Icon_Styles
		('ENT01', 'Offense: All Other Offenses', 'RepresentAsIcon', 'Incident', NULL),
		('ENT02', 'Offense: Animal Cruelty Offenses', 'RepresentAsIcon', 'Dog', NULL),
		('ENT03', 'Offense: Arson', 'RepresentAsIcon', 'Arson', NULL),
		('ENT04', 'Offense: Assault Offenses', 'RepresentAsIcon', 'Assault', NULL),
		('ENT05', 'Offense: Bad Checks', 'RepresentAsIcon', 'Cheque', 'red'),
		('ENT06', 'Offense: Bribery', 'RepresentAsIcon', 'Mnytrans', NULL),
		('ENT07', 'Offense: Burglary', 'RepresentAsIcon', 'Burglary', NULL),
		('ENT08', 'Offense: Counterfeiting/Forgery', 'RepresentAsIcon', 'cntrfeit', NULL),
		('ENT09', 'Offense: Curfew/Loitering/Vagrancy Violations', 'RepresentAsIcon', 'Clock', NULL),
		('ENT10', 'Offense: Disorderly Conduct', 'RepresentAsIcon', 'Crime', NULL),
		('ENT11', 'Offense: Driving Under the Influence', 'RepresentAsIcon', 'Tiretred', NULL),
		('ENT12', 'Offense: Drug/Narcotic Offenses', 'RepresentAsIcon', 'Drugs', NULL),
		('ENT13', 'Offense: Embezzlement', 'RepresentAsIcon', 'Account', NULL),
		('ENT14', 'Offense: Extortion/Blackmail', 'RepresentAsIcon', 'Contaminated Letter', NULL),
		('ENT15', 'Offense: Family Offenses, Nonviolent', 'RepresentAsIcon', 'Family', 'red'),
		('ENT16', 'Offense: Fraud Offenses', 'RepresentAsIcon', 'Fraud', NULL),
		('ENT17', 'Offense: Gambling Offenses', 'RepresentAsIcon', 'Jester', NULL),
		('ENT18', 'Offense: Homicide Offenses', 'RepresentAsIcon', 'Body', NULL),
		('ENT19', 'Offense: Human Trafficking Offenses', 'RepresentAsIcon', 'Passport', NULL),
		('ENT20', 'Offense: Kidnapping/Abduction', 'RepresentAsIcon', 'Kidnapping', NULL),
		('ENT21', 'Offense: Larceny Offenses', 'RepresentAsIcon', 'Counterfeit Goods', NULL),
		('ENT22', 'Offense: Liquor Law Violations', 'RepresentAsIcon', 'Alcohol', NULL),
		('ENT23', 'Offense: Motor Vehicle Theft', 'RepresentAsIcon', 'Car (Rental)', NULL),
		('ENT24', 'Offense: Not an Offense', 'RepresentAsIcon', 'Spreadsheetdoc', NULL),
		('ENT25', 'Offense: Peeping Tom', 'RepresentAsIcon', 'Srvlanc0', NULL),
		('ENT26', 'Offense: Pornography/Obscene Material', 'RepresentAsIcon', 'Picturedoc', NULL),
		('ENT27', 'Offense: Prostitution Offenses', 'RepresentAsIcon', 'Perfume', NULL),
		('ENT28', 'Offense: Robbery', 'RepresentAsIcon', 'Robbery', NULL),
		('ENT29', 'Offense: Sex Offenses', 'RepresentAsIcon', 'interview', 'red'),
		('ENT30', 'Offense: Sex Offenses, Nonforcible', 'RepresentAsIcon', 'interview', 'blue'),
		('ENT31', 'Offense: Stolen Property Offenses', 'RepresentAsIcon', 'Package', NULL),
		('ENT32', 'Offense: Traffic Offenses', 'RepresentAsIcon', 'Speed Camera', NULL),
		('ENT33', 'Offense: Trespass of Real Property', 'RepresentAsIcon', 'Footprnt', NULL),
		('ENT34', 'Offense: Vandalism', 'RepresentAsIcon', 'Window (Broken)', NULL),
		('ENT35', 'Offense: Violation of Orders', 'RepresentAsIcon', 'Fugitive', NULL),
		('ENT36', 'Offense: Warrants', 'RepresentAsIcon', 'Sentence', NULL),
		('ENT37', 'Offense: Weapon Law Violations', 'RepresentAsIcon', 'Weapons Cache', NULL),
	--person_icon_styles
		('ENT38', 'UNKNOWN', 'RepresentAsIcon', 'Person (Faceless)', NULL),
		('ENT39', 'X', 'RepresentAsIcon', 'Adult', NULL),
		('ENT40', 'MALE', 'RepresentAsIcon', 'Person', NULL),
		('ENT41', 'FEMALE', 'RepresentAsIcon', 'Woman', NULL),
	--vehicle_icon_styles
		('ENT42', 'Vehicle: AIRCRAFT', 'RepresentAsIcon', 'Airplane', NULL),
		('ENT44', 'Vehicle: ALL TERRAIN  VEHICLE', 'RepresentAsIcon', 'Patrol Vehicle', NULL),
		('ENT45', 'Vehicle: ASSEMBLED VEHICLES', 'RepresentAsIcon', 'Patrol Vehicle', NULL),
		('ENT46', 'Vehicle: BICYCLE', 'RepresentAsIcon', 'Cycle', NULL),
		('ENT47', 'Vehicle: BOX TRUCK/CARGO VAN', 'RepresentAsIcon', 'Vanluton', NULL),
		('ENT48', 'Vehicle: Bus', 'RepresentAsIcon', 'Coach', NULL),
		('ENT49', 'Vehicle: CONSTRUCTION EQUIPMENT', 'RepresentAsIcon', 'Dump Truck', NULL),
		('ENT50', 'Vehicle: DUNE BUGGY', 'RepresentAsIcon', 'Patrol Vehicle', NULL),
		('ENT51', 'Vehicle: FARM AND GARDEN', 'RepresentAsIcon', 'Patrol Vehicle', NULL),
		('ENT52', 'Vehicle: GOLF CART', 'RepresentAsIcon', 'Patrol Vehicle', NULL),
		('ENT53', 'Vehicle: MINI-VAN/PASSENGER VAN', 'RepresentAsIcon', 'Van', NULL),
		('ENT54', 'Vehicle: MOTORCYCLE', 'RepresentAsIcon', 'Mcycle', NULL),
		('ENT55', 'Vehicle: MOTORHOME, RV', 'RepresentAsIcon', 'Motorhome', NULL),
		('ENT56', 'Vehicle: MOTORIZED SCOOTER', 'RepresentAsIcon', 'Patrol Vehicle', NULL),
		('ENT57', 'Vehicle: OTHER VEHICLE', 'RepresentAsIcon', 'Patrol Vehicle', NULL),
		('ENT58', 'Vehicle: PASSENGER CAR', 'RepresentAsIcon', 'Car', NULL),				
		('ENT59', 'Vehicle: PICK-UP TRUCK', 'RepresentAsIcon', 'Pickup', NULL),
		('ENT60', 'Vehicle: POLICE VEHICLE', 'RepresentAsIcon', 'Policcar', NULL),
		('ENT61', 'Vehicle: SEMI, TRACTOR TRAILER', 'RepresentAsIcon', 'Articab', NULL),
		('ENT62', 'Vehicle: SNOW MOBILE', 'RepresentAsIcon', 'Patrol Vehicle', NULL),
		('ENT63', 'Vehicle: SUV/LL/JEEP', 'RepresentAsIcon', '4x4', NULL),				
		('ENT64', 'Vehicle: TANKER TRUCK', 'RepresentAsIcon', 'Hgv', NULL),
		('ENT65', 'Vehicle: TRAILER', 'RepresentAsIcon', 'Trailer', NULL),
		('ENT66', 'Vehicle: WATERCRAFT', 'RepresentAsIcon', 'Cruiser', NULL),
		('ENT67', 'Vehicle: ', 'RepresentAsIcon', 'Patrol Vehicle', NULL),
	--cad_icon_styles				
		('ENT68', 'cad', 'RepresentAsIcon', 'Voice Chat', NULL),
	--business_icon_stules
		('ENT69', 'business', 'RepresentAsIcon', 'Shopping Mall', NULL),
	--msisdn_icon_styles
		('ENT70', 'phone', 'RepresentAsIcon', 'Phone', NULL),
		('ENT71', 'External Case', 'RepresentAsIcon', 'Digital Evidence Analysis', NULL),
	--WEAPON_ICON_STYLES
		('ENT72', 'Weapon: Rifle', 'RepresentAsIcon', 'Rifle', NULL),
		('ENT73', 'Weapon: Pistol', 'RepresentAsIcon', 'Gun', NULL),
		('ENT74', 'Weapon: Shotgun', 'RepresentAsIcon', 'Shotgun', NULL),
		('ENT75', 'Weapon: Airsoft', 'RepresentAsIcon', 'Air Rifle', NULL),
		('ENT76', 'Weapon: Revolver', 'RepresentAsIcon', 'Revolver', NULL),
		('ENT77', 'Weapon: Other', 'RepresentAsIcon', 'Gun', 'white'),
	--EVIDENCE_ICON_STYLES
		('ENT78', 'Evidence: DNA', 'RepresentAsIcon', 'Dna', NULL),
		('ENT79', 'Evidence: Video', 'RepresentAsIcon', 'VidCass', NULL),
		('ENT80', 'Evidence: Clothing', 'RepresentAsIcon', 'Clothing', NULL),
		('ENT81', 'Evidence: Bullet Fragments', 'RepresentAsIcon', 'Bullet', NULL),
		('ENT82', 'Evidence: Casings', 'RepresentAsIcon', 'Bulcases', NULL),
	--NIBIN
		('ENT83', 'NIBIN', 'RepresentAsIcon', 'Forensic',NULL),
	--Additional Icons
		('ENT84', 'Multiple: Cases', 'RepresentAsIcon', 'Case',NULL),
		('ENT85', 'Multiple: People', 'RepresentAsIcon', 'Group of People',NULL),
		('ENT86', 'Multiple: Other', 'RepresentAsIcon', 'General group',NULL),
		('ENT87', 'General', 'RepresentAsIcon', 'General',NULL),
		('ENT88', 'Offense: None Specified', 'RepresentAsIcon', 'Query',NULL);

	DECLARE @ET_COL XML;
	SELECT  @ET_COL = (
		SELECT		  
		  (SELECT a.id AS '@Id', a.name AS '@Name', a.PreferredRepresentation AS '@PreferredRepresentation', a.IconFile AS '@IconFile', (SELECT col.color_val FROM @COLR_REFR col WHERE col.color_name = a.IconShadingColour) AS '@IconShadingColour' FROM @entity_type_col_prep a WHERE a.IconShadingColour IS NOT NULL ORDER BY a.id FOR XML PATH('EntityType'),type),
		  (SELECT a.id AS '@Id', a.name AS '@Name', a.PreferredRepresentation AS '@PreferredRepresentation', a.IconFile AS '@IconFile'
			 FROM @entity_type_col_prep a WHERE a.IconShadingColour IS NULL ORDER BY a.id FOR XML PATH('EntityType'),type)
		  	FOR XML PATH('EntityTypeCollection')
		);

--STRENGTHCOLLECTION
DECLARE @ST_COL XML;
SELECT  @ST_COL = (
	SELECT (SELECT 'STID1' AS '@Id', 'Confirmed'   AS '@Name', 'DotStyleSolid'  AS '@DotStyle' FOR XML PATH('Strength'),type),
			(SELECT 'STID2' AS '@Id', 'Unconfirmed' AS '@Name', 'DotStyleDashed' AS '@DotStyle' FOR XML PATH('Strength'),type),
			(SELECT 'STID3' AS '@Id', 'Tentative'   AS '@Name', 'DotStyleDotted' AS '@DotStyle' FOR XML PATH('Strength'),type)
			FOR XML PATH('StrengthCollection')
);

--LINKTYPECOLLECTION
DECLARE @link_type_col_prep TABLE(Id NVARCHAR(20),Name NVARCHAR(MAX), Colour NVARCHAR(MAX));
INSERT INTO @link_type_col_prep VALUES 
		('LNK01', 'Case_to_Pers'	,'Black'),
		('LNK02', 'Case_to_Vehi'	,'Blue'),
		('LNK03', 'Pers_to_Pers'	,'Copper'),
		('LNK04', 'Case_to_Case'	,'Brown'),
		('LNK05', 'Case_to_Busn'	,'Gold'),
		('LNK06', 'Case_to_Call'	,'Taupe'),
		('LNK07', 'Nibin_Link'	,'Red');
								
DECLARE @LT_COL XML;
SELECT  @LT_COL = (
	SELECT (
		SELECT a.id AS '@Id', a.name AS '@Name', (
			SELECT col.color_val FROM @COLR_REFR col WHERE col.color_name = a.Colour
		) AS '@Colour' 
			FROM @link_type_col_prep a ORDER BY a.id FOR XML PATH('LinkType'),type)
			FOR XML PATH('LinkTypeCollection')
	);
--CURRENTSTYLECOLLECTION

DECLARE @CS_COL XML;
SELECT  @CS_COL = (
	SELECT(
		SELECT 'MultiplicitySingle' AS '@Multiplicity' FOR XML PATH('ConnectionStyle'),type) FOR XML PATH('CurrentStyleCollection')
);

--(!)ATTRIBUTECLASSCOLLECTION !!!This section dictates the order in which attributes appear on entities.
--Group like items for sake of concision	
	--general attributes	
DECLARE @CONC_ATTR TABLE( attrgroup NVARCHAR(MAX),name NVARCHAR(MAX),id NVARCHAR(20)); INSERT INTO @CONC_ATTR VALUES 
	/*Selection Sets*/ ('SelSet', 'Selection Set 0', 'SL0'),('SelSet', 'Selection Set 1', 'SL1'),('SelSet', 'Selection Set 2', 'SL2'),('SelSet', 'Selection Set 3', 'SL3'),('SelSet', 'Selection Set 4', 'SL4'), ('SelSet', 'Selection Set 5', 'SL5'),('SelSet', 'Selection Set 6', 'SL6'),('SelSet', 'Selection Set 7', 'SL7'), ('SelSet', 'Selection Set 8', 'SL8'),('SelSet', 'Selection Set 9', 'SL9'),
	/*Vehicles______*/ ('vic_unique1', 'License Number', 'ID33'),('Vehicles', 'License State', 'ID34'),('Vehicles', 'License Year', 'ID35'),('Vehicles', 'License Type', 'ID36'),('Vehicles', 'VIN', 'ID37'),('Vehicles', 'Vehicle Type', 'ID38'),('Vehicles', 'Vehicle Style', 'ID39'),('Vehicles', 'Vehicle Year', 'ID40'),('Vehicles', 'Vehicle Make', 'ID41'),('Vehicles', 'Vehicle Model', 'ID42'),('Vehicles', 'Vehicle Color', 'ID43'),('Vehicles', 'Vehicle Role', 'ID44'),
	/*Persons_______*/ ('Pers_Unique4', 'Race', 'ID01'),('Pers_Unique1', 'dob', 'ID02'),('Pers_Unique5', 'Sex', 'ID03'),('Pers_Unique2', 'Height', 'ID04'),('Pers_Unique3', 'Weight', 'ID05'),('Pers_Text', 'Complexion', 'ID06'),('Pers_Text', 'Build', 'ID07'),('Pers_Text', 'Hair Color', 'ID08'),('Pers_Text', 'Hair Style', 'ID09'),('Pers_Text', 'Eye Color', 'ID10'),('Pers_Text', 'Lens Type', 'ID11'),('Pers_Text', 'Facial Hair Color', 'ID12'),('Pers_Text', 'Facial Hair Style', 'ID13'),('Pers_Text', 'Caution Flag', 'ID14'),
	/*GO_TO_PER_LINK*/ ('Link_go_per', 'Role', 'ID15'),
	/*GOs___________*/ ('Case_Unique1', 'Occur DateTime', 'ID16'),('Case_Unique2', 'Report Date', 'ID17'),('Case_Text', 'Municipality', 'ID18'),('Case_Text', 'Jurisdiction', 'ID19'),('Case_Text', 'Neighborhood', 'ID20'),('Case_Text', 'Precinct', 'ID21'),('Case_Text', 'District', 'ID22'),('Case_Text', 'Grid', 'ID23'),('Case_Unique4', 'Location', 'ID24'),('Case_Text', 'Place Name', 'ID25'),('Case_Unique3', 'Latitude', 'ID26'),('Case_Unique3', 'Longitude', 'ID27'),('Case_Text', 'Offense Category', 'ID28'),('Case_Text', 'Offense Type', 'ID29'),('Case_Text', 'Offense Description', 'ID30'),('Case_Text', 'Case Title', 'ID31'),('Case_Text', 'Case Status', 'ID32'),('Case_Unique5', 'Privatized', 'ID49'),
	/*CAD___________*/ ('CAD', 'Final Case Type', 'ID45'),('CAD', 'Cleared By', 'ID46'),
	/*Businesses____*/ ('Business', 'Business Name', 'ID47'),('Business', 'Business Type', 'ID48'),
	/*Officer_______*/ ('Officer', 'Lead Investigator', 'ID50');

	DECLARE @AC_COL XML;
	SELECT  @AC_COL = (
	SELECT
		--has cards/clash
		  (SELECT 'Has Cards' AS '@Name', 'HC1' AS '@Id', 'AttMergeOR'        AS '@PasteBehaviour', 'AttMergeOR'         AS '@MergeBehaviour', 'true'  AS '@ShowIfSet', 'false' AS '@Visible', '2'  AS '@DecimalPlaces', 'false' AS '@ShowSeconds', 'true'  AS '@ShowTime', 'true' AS '@ShowDate', 'true'  AS '@ShowValue', 'false' AS '@ShowSuffix', 'false' AS '@ShowPrefix', 'true'  AS '@ShowSymbol', ''     AS '@Suffix', '' AS '@Prefix', 'ac-cards' AS '@IconFile', 'false' AS '@UserCanRemove', 'false' AS '@UserCanAdd', 'false' AS '@IsUser', 'AttFlag'   AS '@Type'  FOR XML PATH('AttributeClass'),type),
		  (SELECT 'Clash'     AS '@Name', 'CL1' AS '@Id', 'AttMergeOR'        AS '@PasteBehaviour', 'AttMergeOR'         AS '@MergeBehaviour', 'false' AS '@ShowIfSet', 'true'  AS '@Visible', '2'  AS '@DecimalPlaces', 'false' AS '@ShowSeconds', 'true'  AS '@ShowTime', 'true' AS '@ShowDate', 'true'  AS '@ShowValue', 'false' AS '@ShowSuffix', 'false' AS '@ShowPrefix', 'true'  AS '@ShowSymbol', ''     AS '@Suffix', '' AS '@Prefix', 'ac-clash' AS '@IconFile', 'true'  AS '@UserCanRemove', 'false' AS '@UserCanAdd', 'false' AS '@IsUser', 'AttFlag'   AS '@Type'  FOR XML PATH('AttributeClass'),type),	  
		--Selection Sets
		  (SELECT a.name      AS '@Name', a.id AS '@Id', 'AttMergeOR'         AS '@PasteBehaviour', 'AttMergeOR'         AS '@MergeBehaviour', 'false'  AS '@ShowIfSet', 'false'  AS '@Visible', '2'  AS '@DecimalPlaces', 'false' AS '@ShowSeconds', 'true'  AS '@ShowTime', 'true' AS '@ShowDate', 'false' AS '@ShowValue', 'false' AS '@ShowSuffix', 'false' AS '@ShowPrefix', 'false'  AS '@ShowSymbol', ''     AS '@Suffix', '' AS '@Prefix', 'i2sel0'   AS '@IconFile', 'true'  AS '@UserCanRemove', 'true'  AS '@UserCanAdd', 'false' AS '@IsUser', 'AttFlag'   AS '@Type' FROM @CONC_ATTR a WHERE a.attrgroup = 'SelSet' ORDER BY a.id FOR XML PATH('AttributeClass'),type),
		--Persons & some general text. see end of these code lines to right
		  (SELECT a.name      AS '@Name', a.id AS '@Id', 'AttMergeMin'        AS '@PasteBehaviour', 'AttMergeMin'        AS '@MergeBehaviour', 'true'  AS '@ShowIfSet', 'false' AS '@Visible', '2'  AS '@DecimalPlaces', 'false' AS '@ShowSeconds', 'false' AS '@ShowTime', 'true' AS '@ShowDate', 'true'  AS '@ShowValue', 'false' AS '@ShowSuffix', 'false' AS '@ShowPrefix', 'false' AS '@ShowSymbol', ''     AS '@Suffix', '' AS '@Prefix', 'i2Sel0'   AS '@IconFile', 'true'  AS '@UserCanRemove', 'true'  AS '@UserCanAdd', 'false' AS '@IsUser', 'AttTime'   AS '@Type' FROM @CONC_ATTR a WHERE a.attrgroup = 'Pers_Unique1' ORDER BY a.id  FOR XML PATH('AttributeClass'),type),
		  (SELECT a.name      AS '@Name', a.id AS '@Id', 'AttMergeAddIfNotIn' AS '@PasteBehaviour', 'AttMergeAddIfNotIn' AS '@MergeBehaviour', 'true'  AS '@ShowIfSet', 'false' AS '@Visible', '0'  AS '@DecimalPlaces', 'false' AS '@ShowSeconds', 'true'  AS '@ShowTime', 'true' AS '@ShowDate', 'true'  AS '@ShowValue', 'false' AS '@ShowSuffix', 'false' AS '@ShowPrefix', 'false' AS '@ShowSymbol', ''     AS '@Suffix', '' AS '@Prefix', 'i2Sel0'   AS '@IconFile', 'true'  AS '@UserCanRemove', 'true'  AS '@UserCanAdd', 'false' AS '@IsUser', 'AttText'   AS '@Type' FROM @CONC_ATTR a WHERE a.attrgroup IN ('Pers_Text', 'link_go_per', 'Vehicles', 'CAD', 'Business') ORDER BY a.id FOR XML PATH('AttributeClass'),type),
		  (SELECT a.name      AS '@Name', a.id AS '@Id', 'AttMergeAddIfNotIn' AS '@PasteBehaviour', 'AttMergeAddIfNotIn' AS '@MergeBehaviour', 'true'  AS '@ShowIfSet', 'true' AS '@Visible', '0'  AS '@DecimalPlaces', 'false' AS '@ShowSeconds', 'true'  AS '@ShowTime', 'true' AS '@ShowDate', 'true'  AS '@ShowValue', 'false' AS '@ShowSuffix', 'false' AS '@ShowPrefix', 'false' AS '@ShowSymbol', ''     AS '@Suffix', '' AS '@Prefix', 'i2Sel0'   AS '@IconFile', 'true'  AS '@UserCanRemove', 'true'  AS '@UserCanAdd', 'false' AS '@IsUser', 'AttText'   AS '@Type' FROM @CONC_ATTR a WHERE a.attrgroup = 'vic_unique1' ORDER BY a.id FOR XML PATH('AttributeClass'),type),
		  (SELECT a.name      AS '@Name', a.id AS '@Id', 'AttMergeMin'        AS '@PasteBehaviour', 'AttMergeMin'        AS '@MergeBehaviour', 'true'  AS '@ShowIfSet', 'false' AS '@Visible', '0'  AS '@DecimalPlaces', 'false' AS '@ShowSeconds', 'true'  AS '@ShowTime', 'true' AS '@ShowDate', 'true'  AS '@ShowValue', 'false' AS '@ShowSuffix', 'false' AS '@ShowPrefix', 'false' AS '@ShowSymbol', ''     AS '@Suffix', '' AS '@Prefix', 'i2Sel0'   AS '@IconFile', 'true'  AS '@UserCanRemove', 'true'  AS '@UserCanAdd', 'false' AS '@IsUser', 'AttNumber' AS '@Type' FROM @CONC_ATTR a WHERE a.attrgroup = 'Pers_Unique2' ORDER BY a.id  FOR XML PATH('AttributeClass'),type),
		  (SELECT a.name      AS '@Name', a.id AS '@Id', 'AttMergeMin'        AS '@PasteBehaviour', 'AttMergeMin'        AS '@MergeBehaviour', 'true'  AS '@ShowIfSet', 'false' AS '@Visible', '0'  AS '@DecimalPlaces', 'false' AS '@ShowSeconds', 'true'  AS '@ShowTime', 'true' AS '@ShowDate', 'true'  AS '@ShowValue', 'true'  AS '@ShowSuffix', 'false' AS '@ShowPrefix', 'false' AS '@ShowSymbol', ' lbs' AS '@Suffix', '' AS '@Prefix', 'i2Sel0'   AS '@IconFile', 'true'  AS '@UserCanRemove', 'true'  AS '@UserCanAdd', 'false' AS '@IsUser', 'AttNumber' AS '@Type' FROM @CONC_ATTR a WHERE a.attrgroup = 'Pers_Unique3' ORDER BY a.id  FOR XML PATH('AttributeClass'),type),
		  (SELECT a.name      AS '@Name', a.id AS '@Id', 'AttMergeAddIfNotIn' AS '@PasteBehaviour', 'AttMergeAddIfNotIn' AS '@MergeBehaviour', 'true'  AS '@ShowIfSet', 'false' AS '@Visible', '0'  AS '@DecimalPlaces', 'false' AS '@ShowSeconds', 'true'  AS '@ShowTime', 'true' AS '@ShowDate', 'true'  AS '@ShowValue', 'false' AS '@ShowSuffix', 'false' AS '@ShowPrefix', 'false' AS '@ShowSymbol', ''     AS '@Suffix', '' AS '@Prefix', 'i2Sel0'   AS '@IconFile', 'true'  AS '@UserCanRemove', 'true'  AS '@UserCanAdd', 'false' AS '@IsUser', 'AttText'   AS '@Type' FROM @CONC_ATTR a WHERE a.attrgroup = 'Pers_Unique4' ORDER BY a.id FOR XML PATH('AttributeClass'),type),
		  (SELECT a.name      AS '@Name', a.id AS '@Id', 'AttMergeAddIfNotIn' AS '@PasteBehaviour', 'AttMergeAddIfNotIn' AS '@MergeBehaviour', 'true'  AS '@ShowIfSet', 'false' AS '@Visible', '0'  AS '@DecimalPlaces', 'false' AS '@ShowSeconds', 'true'  AS '@ShowTime', 'true' AS '@ShowDate', 'true'  AS '@ShowValue', 'false' AS '@ShowSuffix', 'false' AS '@ShowPrefix', 'false' AS '@ShowSymbol', ''     AS '@Suffix', '' AS '@Prefix', 'i2Sel0'   AS '@IconFile', 'true'  AS '@UserCanRemove', 'true'  AS '@UserCanAdd', 'false' AS '@IsUser', 'AttText'   AS '@Type' FROM @CONC_ATTR a WHERE a.attrgroup = 'Pers_Unique5' ORDER BY a.id FOR XML PATH('AttributeClass'),type),
		--GOs
		  (SELECT a.name      AS '@Name', a.id AS '@Id', 'AttMergeMin'        AS '@PasteBehaviour', 'AttMergeMin'        AS '@MergeBehaviour', 'true'  AS '@ShowIfSet', 'true' AS '@Visible', '2'  AS '@DecimalPlaces', 'false' AS '@ShowSeconds', 'true'  AS '@ShowTime', 'true' AS '@ShowDate', 'true'  AS '@ShowValue', 'false' AS '@ShowSuffix', 'false' AS '@ShowPrefix', 'false' AS '@ShowSymbol', ''     AS '@Suffix', '' AS '@Prefix', 'i2Sel0'   AS '@IconFile', 'true'  AS '@UserCanRemove', 'true'  AS '@UserCanAdd', 'false' AS '@IsUser', 'AttTime'   AS '@Type' FROM @CONC_ATTR a WHERE a.attrgroup = 'Case_Unique1' ORDER BY a.id FOR XML PATH('AttributeClass'),type),
		  (SELECT a.name      AS '@Name', a.id AS '@Id', 'AttMergeMin'        AS '@PasteBehaviour', 'AttMergeMin'        AS '@MergeBehaviour', 'true'  AS '@ShowIfSet', 'false' AS '@Visible', '2'  AS '@DecimalPlaces', 'false' AS '@ShowSeconds', 'false' AS '@ShowTime', 'true' AS '@ShowDate', 'true'  AS '@ShowValue', 'false' AS '@ShowSuffix', 'false' AS '@ShowPrefix', 'false' AS '@ShowSymbol', ''     AS '@Suffix', '' AS '@Prefix', 'i2Sel0'   AS '@IconFile', 'true'  AS '@UserCanRemove', 'true'  AS '@UserCanAdd', 'false' AS '@IsUser', 'AttTime'   AS '@Type' FROM @CONC_ATTR a WHERE a.attrgroup = 'Case_Unique2' ORDER BY a.id FOR XML PATH('AttributeClass'),type),
		  (SELECT a.name      AS '@Name', a.id AS '@Id', 'AttMergeAddIfNotIn' AS '@PasteBehaviour', 'AttMergeAddIfNotIn' AS '@MergeBehaviour', 'true'  AS '@ShowIfSet', 'false' AS '@Visible', '0'  AS '@DecimalPlaces', 'false' AS '@ShowSeconds', 'true'  AS '@ShowTime', 'true' AS '@ShowDate', 'true'  AS '@ShowValue', 'false' AS '@ShowSuffix', 'false' AS '@ShowPrefix', 'false' AS '@ShowSymbol', ''     AS '@Suffix', '' AS '@Prefix', 'i2Sel0'   AS '@IconFile', 'true'  AS '@UserCanRemove', 'true'  AS '@UserCanAdd', 'false' AS '@IsUser', 'AttText'   AS '@Type' FROM @CONC_ATTR a WHERE a.attrgroup = 'Case_Text'    ORDER BY a.id FOR XML PATH('AttributeClass'),type),
		  (SELECT a.name      AS '@Name', a.id AS '@Id', 'AttMergeMin'        AS '@PasteBehaviour', 'AttMergeMin'        AS '@MergeBehaviour', 'true'  AS '@ShowIfSet', 'false' AS '@Visible', '15' AS '@DecimalPlaces', 'false' AS '@ShowSeconds', 'true'  AS '@ShowTime', 'true' AS '@ShowDate', 'true'  AS '@ShowValue', 'false' AS '@ShowSuffix', 'false' AS '@ShowPrefix', 'false' AS '@ShowSymbol', ''     AS '@Suffix', '' AS '@Prefix', 'i2Sel0'   AS '@IconFile', 'true'  AS '@UserCanRemove', 'true'  AS '@UserCanAdd', 'false' AS '@IsUser', 'AttNumber' AS '@Type' FROM @CONC_ATTR a WHERE a.attrgroup = 'Case_Unique3' ORDER BY a.id FOR XML PATH('AttributeClass'),type),
		  (SELECT a.name      AS '@Name', a.id AS '@Id', 'AttMergeAddIfNotIn' AS '@PasteBehaviour', 'AttMergeAddIfNotIn' AS '@MergeBehaviour', 'true'  AS '@ShowIfSet', 'true' AS '@Visible', '0'  AS '@DecimalPlaces', 'false' AS '@ShowSeconds', 'true'  AS '@ShowTime', 'true' AS '@ShowDate', 'true'  AS '@ShowValue', 'false' AS '@ShowSuffix', 'false' AS '@ShowPrefix', 'false' AS '@ShowSymbol', ''     AS '@Suffix', '' AS '@Prefix', 'i2Sel0'   AS '@IconFile', 'true'  AS '@UserCanRemove', 'true'  AS '@UserCanAdd', 'false' AS '@IsUser', 'AttText'   AS '@Type' FROM @CONC_ATTR a WHERE a.attrgroup = 'Case_Unique4'    ORDER BY a.id FOR XML PATH('AttributeClass'),type),
		  (SELECT a.name      AS '@Name', a.id AS '@Id', 'AttMergeAddIfNotIn' AS '@PasteBehaviour', 'AttMergeAddIfNotIn' AS '@MergeBehaviour', 'true'  AS '@ShowIfSet', 'true' AS '@Visible', '0'  AS '@DecimalPlaces', 'false' AS '@ShowSeconds', 'true'  AS '@ShowTime', 'true' AS '@ShowDate', 'true'  AS '@ShowValue', 'false' AS '@ShowSuffix', 'false' AS '@ShowPrefix', 'false' AS '@ShowSymbol', ''     AS '@Suffix', '' AS '@Prefix', 'i2Sel0'   AS '@IconFile', 'true'  AS '@UserCanRemove', 'true'  AS '@UserCanAdd', 'false' AS '@IsUser', 'AttText'   AS '@Type',(SELECT '0' AS '@BackColour', '255' AS '@FontColour' FOR XML PATH('Font'),type) FROM @CONC_ATTR a WHERE a.attrgroup = 'Case_Unique5' ORDER BY a.id FOR XML PATH('AttributeClass'),type),
		  (SELECT a.name      AS '@Name', a.id AS '@Id', 'AttMergeAddIfNotIn' AS '@PasteBehaviour', 'AttMergeAddIfNotIn' AS '@MergeBehaviour', 'true'  AS '@ShowIfSet', 'true' AS '@Visible', '0'  AS '@DecimalPlaces', 'false' AS '@ShowSeconds', 'true'  AS '@ShowTime', 'true' AS '@ShowDate', 'true'  AS '@ShowValue', 'false' AS '@ShowSuffix', 'false' AS '@ShowPrefix', 'false' AS '@ShowSymbol', ''     AS '@Suffix', '' AS '@Prefix', 'i2Sel0'   AS '@IconFile', 'true'  AS '@UserCanRemove', 'true'  AS '@UserCanAdd', 'false' AS '@IsUser', 'AttText'   AS '@Type',(SELECT '9109504' AS '@BackColour', '16777215' AS '@FontColour' FOR XML PATH('Font'),type) FROM @CONC_ATTR a WHERE a.attrgroup = 'Officer' ORDER BY a.id FOR XML PATH('AttributeClass'),type)
	FOR XML PATH('AttributeClassCollection')
	);

--(@@)PaletteCollection
	DECLARE @PC_COL XML;
	SELECT  @PC_COL = (
	SELECT(SELECT 'RMS_Palette' AS '@Name',
	               (SELECT
		                  (SELECT a.id AS '@AttributeClassReference', a.name AS '@AttributeClass'
							 FROM @CONC_ATTR a 
						    WHERE a.attrgroup IN ('SelSet', 'Case_Text', 'Case_Unique1', 'Case_Unique2', 'Case_Unique3', 'Case_Unique4', 'CaseUnique5', 'Pers_Text', 'Pers_Unique1', 'Pers_Unique2', 'Pers_Unique3', 'Pers_Unique4', 'Pers_Unique5', 'Link_go_per', 'Vehicles', 'CAD', 'Business', 'Officer') 
							ORDER BY a.id ASC FOR XML PATH('AttributeClassEntry'),type)					
				    FOR XML PATH('AttributeClassEntryCollection'),type),
	               (SELECT
		                  (SELECT a.id AS '@EntityTypeReference', a.name AS '@Entity'
							 FROM @entity_type_col_prep a 
							ORDER BY a.id ASC FOR XML PATH('EntityTypeEntry'),type)					
				    FOR XML PATH('EntityTypeEntryCollection'),type),
	               (SELECT
		                  (SELECT a.id AS '@LinkTypeReference', a.name AS '@LinkType'
							 FROM @link_type_col_prep a 
							ORDER BY a.id ASC FOR XML PATH('LinkTypeEntry'),type)					
				    FOR XML PATH('LinkTypeEntryCollection'),type)
		   FOR XML PATH('Palette'),type)
	FOR XML PATH('PaletteCollection')
	);
--(@@)LegendDefinition
	DECLARE @LD_DEF XML;
	SELECT  @LD_DEF = (
	SELECT 'false' AS '@Shown', '0' AS '@Y', '0' AS '@X', 'LegendAlignmentRight' AS '@HorizontalAlignment', 'LegendAlignmentBottom' AS '@VerticalAlignment', 'LegendArrangementSquare' AS '@Arrange',
	             (SELECT '16777215' AS '@BackColour', 'false' AS '@Underline', 'false' AS '@Strikeout', '10' AS '@PointSize', 'false' AS '@Italic', '0' AS '@FontColour', 'Tahoma' AS '@FaceName', 'CharSetANSI' AS '@CharSet', 'false' AS '@Bold' FOR XML PATH('Font'),type)
	FOR XML PATH('LegendDefinition')
	);
--Print_settings_to_format_header_and_footer
	DECLARE @PRINTSET XML;
	SELECT  @PRINTSET = (
	SELECT
		(SELECT(SELECT 'HeaderFooterPositionCenter' AS '@Position', 'Classification' AS '@Property', 'false' AS '@Visible' FOR XML PATH ('Footer'),type),
			   (SELECT 'HeaderFooterPositionRight'  AS '@Position', 'Last Saved'	 AS '@Property', 'false' AS '@Visible' FOR XML PATH ('Footer'),type),
			   (SELECT 'HeaderFooterPositionLeft'   AS '@Position', 'Title'	         AS '@Property', 'false' AS '@Visible' FOR XML PATH ('Footer'),type)
			FOR XML PATH('FooterCollection'),type)
	FOR XML PATH ('PrintSettings')
	);
--Establish final table
	INSERT INTO @OUTPUT VALUES  ('xmlcomp', 'ST_COL',@ST_COL,NULL,NULL,NULL,NULL)
							   ,('xmlcomp', 'AC_COL',@AC_COL,NULL,NULL,NULL,NULL)
							   ,('xmlcomp', 'ET_COL',@ET_COL,NULL,NULL,NULL,NULL)
							   ,('xmlcomp', 'CS_COL',@CS_COL,NULL,NULL,NULL,NULL)
							   ,('xmlcomp', 'LT_COL',@LT_COL,NULL,NULL,NULL,NULL)
							--chart item collection added in primary query
							   ,('xmlcomp', 'PC_COL',@PC_COL,NULL,NULL,NULL,NULL)
							   ,('xmlcomp', 'LD_DEF',@LD_DEF,NULL,NULL,NULL,NULL)
							--summary data added in primary query
							   ,('xmlcomp', 'PRINTSET',@PRINTSET,NULL,NULL,NULL,NULL);

	INSERT INTO @OUTPUT 
		SELECT 'color_refr',NULL,NULL,NULL,NULL,a.color_name,a.color_val
		FROM @COLR_REFR a;

/*File Assmbly*/
/*Acquire support information & Summary Data*/
	DECLARE @SUPPORT TABLE (category NVARCHAR(30),name NVARCHAR(30), content XML,id_type VARCHAR(50),id VARCHAR(34),color_name NVARCHAR(MAX),color_val NVARCHAR(10));
		INSERT INTO @SUPPORT SELECT a.* FROM @OUTPUT a;	
/*assemble file*/
	DECLARE @TITLETEXT NVARCHAR(MAX)= 'Example Chart';
	DECLARE @COMNTTEXT NVARCHAR(MAX) = 'Chart Comments';
--()Summary_Data
	DECLARE @CLASSIFICATION NVARCHAR(MAX) = 'Enter Classifcation';
	DECLARE @SUMMARY XML;
	SELECT @SUMMARY = (
	SELECT
		(SELECT(SELECT @TITLETEXT AS '@Field', 'SummaryFieldTitle'    AS '@Type'  FOR XML PATH ('Field'),type),
		       (SELECT @COMNTTEXT AS '@Field', 'SummaryFieldComments' AS '@Type'  FOR XML PATH ('Field'),type)
		FOR XML PATH('FieldCollection'),type),
		(SELECT(SELECT 'Classification' AS '@Name', 'String' AS '@Type',@CLASSIFICATION AS '@Value' FOR XML PATH ('CustomProperty'),type)
		FOR XML PATH ('CustomPropertyCollection'),type)
	FOR XML PATH('Summary')
	);
--CHARTITEMCOLLECTION
	DECLARE @CI_COL XML;
	SELECT  @CI_COL = (
	SELECT(
	--(10A)CASES
			SELECT 'Database' AS '@SourceType', 'RMS' AS '@SourceReference', a.case_number AS '@Label', 'true' AS '@DateSet', 'true' AS '@TimeSet',CONCAT(a.occ_date,'T',a.occ_time,':00') AS '@DateTime',
				(SELECT
					(SELECT CONCAT('GO_',a.case_id) AS '@Identity', CONCAT('GO_',a.case_id) AS '@EntityId',
							(SELECT(SELECT a.offense AS '@Type' FOR XML PATH('IconStyle'),type) FOR XML PATH('Icon'),type),
							(SELECT
								(SELECT a.case_number  AS '@Summary', '1:RMS'     AS '@SourceReference' 
								 FOR XML PATH('Card'),type)
							 FOR XML PATH('CardCollection'),type)
					 FOR XML PATH('Entity'),type)
				 FOR XML PATH('End'),type),
				(SELECT
					CASE WHEN LEN(a.offense) < 1 THEN '' ELSE (SELECT 'ID28' AS '@AttributeClassReference', a.offense AS '@Value' FOR XML PATH('Attribute'),type) END
				FOR XML PATH ('AttributeCollection'),type)
			FROM @CASE a FOR XML PATH ('ChartItem'),type),
	--(10B)PERSONS
			(SELECT 'Database' AS '@SourceType', 'RMS' AS '@SourceReference', a.pers_name AS '@Label',
				(SELECT
					(SELECT CONCAT('PERS_',a.pers_id) AS '@Identity', CONCAT('PERS_',a.pers_id) AS '@EntityId', 
							(SELECT(SELECT a.sex AS '@Type' FOR XML PATH('IconStyle'),type) FOR XML PATH('Icon'),type)
					FOR XML PATH('Entity'),type)
				FOR XML PATH('End'),type),
				(SELECT
					CASE WHEN a.sex IS NULL THEN '' ELSE (SELECT 'ID03'  AS '@AttributeClassReference', a.sex AS '@Value' FOR XML PATH('Attribute'),type) END
				FOR XML PATH ('AttributeCollection'),type)
			FROM @PERS a FOR XML PATH ('ChartItem'),type),
	--(10J)PERSON_TO_EVENT_LINKS
			(SELECT 'Database' AS '@SourceType', 'RMS' AS '@SourceReference',  'Related'  AS '@Label',
				(SELECT CONCAT('PERS_',a.pers_id) AS '@End2Id', CONCAT('GO_',a.case_id) AS '@End1Id', 
					(SELECT 'ArrowNone' AS '@ArrowStyle', '1' AS '@LineWidth', 'Confirmed' AS '@Strength', 'Case_to_Pers' AS '@Type' FOR XML PATH('LinkStyle'),type)
				FOR XML PATH('Link'),type)
			FROM  @CASE_PERS_LINK a FOR XML PATH ('ChartItem'),type)
	--CHART ITEM COLLECTION ENDCAP
			FOR XML PATH('ChartItemCollection')
			 );
--FINAL_ASSEMBLY
	DECLARE @FINAL XML;
	SELECT  @FINAL = 
		(SELECT 'false' AS '@Rigorous', 'false' AS '@IdReferenceLinking',(SELECT a.content FROM @SUPPORT a WHERE a.name = 'ST_COL'),
		(SELECT a.content FROM @SUPPORT a WHERE a.name = 'AC_COL'),
		(SELECT a.content FROM @SUPPORT a WHERE a.name = 'ET_COL'),
		(SELECT a.content FROM @SUPPORT a WHERE a.name = 'CS_COL'),
		(SELECT a.content FROM @SUPPORT a WHERE a.name = 'LT_COL'),
		@CI_COL
		(SELECT a.content FROM @SUPPORT a WHERE a.name = 'PC_COL'),
		(SELECT a.content FROM @SUPPORT a WHERE a.name = 'LD_DEF'),
		@SUMMARY
		(SELECT a.content FROM @SUPPORT a WHERE a.name = 'PRINTSET')
			FOR XML PATH ('Chart')
			);
	--Create final table
		SELECT @FINAL;
