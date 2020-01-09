DROP TABLE IF EXISTS DIM_SQUAD;
CREATE TABLE DIM_SQUAD
(
	anomesdia varchar(8),
    id_squad varchar(6) NOT NULL UNIQUE,
    nm_squad text,
    dt_init date,
    dt_end date
);

DROP TABLE IF EXISTS DIM_EXT;
CREATE TABLE DIM_EXT
(
	anomesdia varchar(8),
    id_ext varchar(20) NOT NULL UNIQUE,
    nm_ext text,
    dt_init date,
    dt_end date
);

DROP TABLE IF EXISTS DIM_UN;
CREATE TABLE DIM_UN
(
	anomesdia varchar(8),
	id_un MEDIUMINT NOT NULL,
    nm_un varchar(100) NOT NULL UNIQUE,
	dt_init date,
    dt_end date
);

DROP TABLE IF EXISTS DIM_EXECUTIVE;
CREATE TABLE DIM_EXECUTIVE
(
	anomesdia varchar(8),
	id_executive MEDIUMINT NOT NULL,
	nm_executive varchar(300) NOT NULL UNIQUE,
	id_sap varchar(6) UNIQUE,
	dt_init date,
	dt_end date
);

DROP TABLE IF EXISTS DIM_USER;
CREATE TABLE DIM_USER
(
	anomesdia varchar(8),
	itau_employee_name varchar(300),
	id_sap varchar(6),
	id_func varchar(6),
	everis_employee_name varchar(300),
	dt_init date,
	dt_end date
);

