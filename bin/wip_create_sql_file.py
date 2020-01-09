from classes.file_transformer_lib import CsvToSQL, ConfParameter, LogControler
from classes.mascara_data import MascaraData
import os, re
import glob

def main(file):      

    table_name = file.split('.')[0]
    table_name = re.sub('[^A-Za-z0-9_]+', '', table_name).lower() + '_tmp'
    table_name = table_name.replace("__","_")
    
    c = CsvToSQL(file)
    
    headers, headers_minus_last, last_header = c.get_headers(file)
    lines_to_write_table = c.create_table_lines(table_name, headers_minus_last, last_header)
    lines_to_write_data_load = c.create_data_lines(file, table_name, headers)
    
    lines_to_write_log = lc.get_stage_load(table_name, file)
    
    c.write_lines_to_file(file, table_name, lines_to_write_table, lines_to_write_data_load, lines_to_write_log)


if __name__ == '__main__':

    t = MascaraData()
   
    lc = LogControler()
    pc = ConfParameter()
    path_conf = pc.get_py_configger('Path')
    
    dest = path_conf['temp'] + t.get_today() + '\\csv'
    os.chdir(dest)
    
    for g in glob.glob("*.csv"):
        os.chdir(dest)
        main(g)