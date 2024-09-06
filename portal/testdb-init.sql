CREATE DATABASE testdb;
GO

USE testdb;
GO

CREATE TABLE dbo.Products(
	ProductID int PRIMARY KEY NOT NULL,
	ProductName varchar(25) NOT NULL,
	Price money NULL,
	ProductDescription varchar(max) NULL
);

-- Standard syntax
INSERT dbo.Products (ProductID, ProductName, Price, ProductDescription) 
VALUES 
	(1, 'Clamp', 12.48, 'Workbench clamp'),
	(2, 'Special Sauce', 100.00, 'Very Special Sauce'),
	(3, 'Golden Kissenger', 1000.48, 'A golden doll with the face of Henry Kissenger'),
	(4, 'Chainsaw', 50.00, 'A chainsaw for cutting down trees'),
	(5, 'Used Braces', 101.00, 'Braces for a small child, lightly used');

GO

SELECT * from dbo.Products;

GO

