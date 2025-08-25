# SQL

## DDL

Refere-se à criação das tabelas, inserções e atualizações.

### CREATE TABLE

Used for creating and connecting relational tables

Exemple:

	CREATE TABLE vendor
	(
	vendorid 	CHAR(2)	  	NOT NULL,
	vendorname 	VARCHAR(25) 	NOT NULL,
	PRIMARY KEY (vendorid)
	);

	CREATE TABLE salestransaction
	( 
	tid VARCHAR(8) NOT NULL,
	customerid CHAR(7) NOT NULL,
	storeid VARCHAR(3) NOT NULL,
	tdate DATE NOT NULL,
	PRIMARY KEY (tid),
	FOREIGN KEY (customerid) REFERENCES customer(customerid),
	FOREIGN KEY (storeid) REFERENCES store(storeid) 
	);

### DROP TABLE

Used to remove a table from the database

Exemple:
	
	DROP TABLE <tableName>

Precisa estar na sequência inversa da criação.


### INSERT INTO
Used to pouplate the created relations with data
	INSERT INTO product VALUES ('1X1','Zzz Bag',100,'PG','CP');
	INSERT INTO product VALUES ('2X2','Easy Boot',70,'MK','FW');
	INSERT INTO product VALUES ('3X3','Cosy Sock',15,'MK','FW');
	INSERT INTO product VALUES ('4X4','Dura Boot',90,'PG','FW');
	INSERT INTO product VALUES ('5X5','Tiny Tent',150,'MK','CP');
	INSERT INTO product VALUES ('6X6','Biggy Tent',250,'MK','CP');	
