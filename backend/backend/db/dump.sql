PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version VALUES('371303aa3c2f');
CREATE TABLE admin (
	id INTEGER NOT NULL, 
	"key" TEXT NOT NULL, 
	value TEXT NOT NULL, 
	format TEXT NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE ("key")
);
INSERT INTO admin VALUES(1,'main_lazy_loading','true','text');
INSERT INTO admin VALUES(2,'side_lazy_loading','true','text');
INSERT INTO admin VALUES(3,'main_num_notes_to_render','10','int');
INSERT INTO admin VALUES(4,'side_num_notes_to_render','5','int');
INSERT INTO admin VALUES(5,'main_default_depth','3','int');
INSERT INTO admin VALUES(6,'side_default_depth','0','int');
INSERT INTO admin VALUES(7,'db_last_updated','1602887657.81662','float');
CREATE TABLE items (
	id TEXT NOT NULL, 
	date_created INTEGER NOT NULL, 
	date_updated INTEGER NOT NULL, 
	text TEXT NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO items VALUES('e83bcd2f',1602887657,1602887657,'This is some text.');
INSERT INTO items VALUES('568d26da',1602887657,1602887657,'Lorem ipsum and cats.');
INSERT INTO items VALUES('023adf31',1602887657,1602887657,'In the beginning...');
INSERT INTO items VALUES('a7cd35ae',1602887657,1602887657,'And the last, at last.');
COMMIT;
