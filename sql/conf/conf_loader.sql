DROP TABLE IF EXISTS tb_load_stage;
CREATE TABLE tb_load_stage
( 
	id_exec MEDIUMINT NOT NULL AUTO_INCREMENT,
	anomesdia varchar(8),
	stg_name varchar(100),
	dt_load TIMESTAMP,
	nm_file varchar(100),
	PRIMARY KEY (id_exec)
);

DROP TABLE IF EXISTS tb_load_prep;
CREATE TABLE tb_load_prep
(
	id_exec MEDIUMINT NOT NULL AUTO_INCREMENT,
    anomesdia varchar(8),
    dp_table_name varchar(100),
    dt_load TIMESTAMP,
	process_name varchar(100),
    PRIMARY KEY (id_exec)

);

DROP TABLE IF EXISTS tb_load_alt;
CREATE TABLE tb_load_alt
(
	id_exec MEDIUMINT NOT NULL AUTO_INCREMENT,
    anomesdia varchar(8),
    dp_table_name varchar(100),
    dt_load TIMESTAMP,
	process_name varchar(100),
    PRIMARY KEY (id_exec)

);

DROP TABLE IF EXISTS tb_load_dim;
CREATE TABLE tb_load_dim
(
	id_exec MEDIUMINT NOT NULL AUTO_INCREMENT,
    anomesdia varchar(8),
    dp_table_name varchar(100),
    dt_load TIMESTAMP,
    process_name varchar(100),
    PRIMARY KEY (id_exec)
);