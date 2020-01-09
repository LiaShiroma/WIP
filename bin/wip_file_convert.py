from classes.file_transformer_lib import ExcelToCsv, ConfParameter
from classes.mascara_data import MascaraData
import os, glob

def read_glob(file):
    exc = ExcelToCsv()
    for g in glob.glob(file):
        exc.excel_to_csv(g, dest_csv, path_conf['sheet'])
        exc.excel_to_csv(g, dest_csv, "Analises")

def create_dir(dir):
    if not os.path.exists(dir) :
        os.mkdir(dir)

def main():  
    for file in ("*.xls", "*.xlsx", "*.xlsb"):
        read_glob(file)     

if __name__ == '__main__':
    t = MascaraData()
    today = t.get_today()
    
    pc = ConfParameter()
    path_conf = pc.get_py_configger('Path')

    source = path_conf['dir'] + today
    dest = path_conf['temp'] + today 
    dest_csv = path_conf['temp'] + today + '\\csv\\'
    
    create_dir(dest)
    create_dir(dest_csv)
    
    os.chdir(source)
    
    main()