DROP TABLE IF EXISTS TB_WRK_ALT_EXECUTIVE;
CREATE TABLE TB_WRK_ALT_EXECUTIVE
(
	anomesdia varchar(8),
	id_executive MEDIUMINT NOT NULL,
	nm_executive varchar(300) NOT NULL,
	id_sap varchar(6),
	dt_init date,
	dt_end date,
	cod_indcd_alt varchar(1)
);

DROP TABLE IF EXISTS TB_WRK_ALT_UN;
CREATE TABLE TB_WRK_ALT_UN
(
	anomesdia varchar(8),
	id_un MEDIUMINT NOT NULL,
    nm_un varchar(100) NOT NULL,
	dt_init date,
    dt_end date,
	cod_indcd_alt varchar(1)
);

DROP TABLE IF EXISTS TB_WRK_ALT_EXT;
CREATE TABLE TB_WRK_ALT_EXT
(
	anomesdia varchar(8),
    id_ext varchar(20) NOT NULL,
    nm_ext text,
    dt_init date,
    dt_end date,
	cod_indcd_alt varchar(1)
);

DROP TABLE IF EXISTS TB_WRK_ALT_SQUAD;
CREATE TABLE TB_WRK_ALT_SQUAD
(
	anomesdia varchar(8),
    id_squad varchar(6) NOT NULL,
    nm_squad text,
    dt_init date,
    dt_end date,
	cod_indcd_alt varchar(1)
);

DROP TABLE IF EXISTS TB_WRK_ALT_USER;
CREATE TABLE TB_WRK_ALT_USER
(
	anomesdia varchar(8),
	itau_employee_name varchar(300),
	id_sap varchar(10),
	id_func varchar(10),
	everis_employee_name varchar(300),
	dt_init date,
	dt_end date,
	cod_indcd_alt varchar(1)
);

