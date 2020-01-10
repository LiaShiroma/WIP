DROP TABLE IF EXISTS AUX_EMPLOYEE;
CREATE TABLE AUX_EMPLOYEE
(
	itau_employee_name TEXT,
	id_sap TEXT,
	id_func TEXT,
	everis_employee_name TEXT,
	dt_init TEXT,
	dt_end TEXT
) DEFAULT CHARSET=utf8; 

LOAD DATA INFILE "C:\\PROD\\conf\\carga_nomes\\stg_base_nomes.csv"
INTO TABLE AUX_EMPLOYEE
CHARACTER SET UTF8
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(
	itau_employee_name,
	id_sap,
	id_func,
	everis_employee_name,
	dt_init,
	dt_end
);

DELETE FROM AUX_EMPLOYEE WHERE dt_init = '';