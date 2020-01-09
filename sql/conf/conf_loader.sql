CREATE TABLE tb_load_stage
( 
	id_exec MEDIUMINT NOT NULL AUTO_INCREMENT,
	anomesdia varchar(8),
	stg_name varchar(100),
	dt_load TIMESTAMP,
	nm_file varchar(100),
	PRIMARY KEY (id_exec)
);

CREATE TABLE AUX_EMPLOYEE
(
	itau_employee_name varchar(300),
	id_sap varchar(6),
	id_func varchar(6),
	everis_employee_name varchar(300),
	dt_init date,
	dt_end date
);