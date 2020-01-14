class ConfParameter():

    def __init__ (self):  
    
        import configparser
        
        self.config = configparser.RawConfigParser()

        self.config.read('C:\\PROD\\conf\\init.conf')

    def get_py_configger(self,path):
        return dict(self.config.items(path))

class CsvToSQL():

    def __init__ (self, file):  

        from classes.mascara_data import MascaraData
        from classes.init_logger import InitLogger
        from unicodedata import normalize
        
        import os, csv, re
        
        self.os = os
        self.csv = csv
        self.re = re
        self.normalize = normalize
        
        self.l = InitLogger(__name__)      
        self.logger = self.l.build_logger()   
        
        self.d = MascaraData()
        self.today = self.d.get_today()
        
        self.logger.info("Inicializando Conversão | Arquivo: " + file)
        
    def get_headers(self, csv_file):

        with open (csv_file, newline='', encoding="utf8") as f:
            reader = self.csv.reader(f)
            header_row = next(reader)
            headers = []
            for i in header_row:
                i = self.normalize('NFKD', i).encode('ASCII', 'ignore').decode('ASCII')
                i = self.re.sub("\s+", "_", i)
                i = self.re.sub('[^A-Za-z0-9_]+', '', i).lower()
                headers.append(i)
            headers_minus_last = headers[:-1]
            last_header = headers[-1]
        return headers, headers_minus_last, last_header


    def create_table_lines(self, tbl_nm, headers_minus_last, last_header):

        column_type = 'TEXT'

        lines_to_write_table = []
        lines_to_write_table.append('DROP TABLE IF EXISTS {};\n'.format(tbl_nm))
        lines_to_write_table.append('CREATE TABLE {}\n('.format(tbl_nm))

        for i in headers_minus_last:
            lines_to_write_table.append(i + ' {},'.format(column_type))
        lines_to_write_table.append(last_header + ' {}'.format(column_type) + '\n) DEFAULT CHARSET=utf8; \n')
        return lines_to_write_table


    def create_data_lines(self, csv_file, tbl_nm, hdrs):

        field_terminator = "','"
        line_terminator = "'\\r\\n'"
        enclosed_by = "'\"'"
        ignore_lines = '1'
        lines_to_write_data_load = []
        lines_to_write_data_load.append('LOAD DATA INFILE "C:\\\\PROD\\\\tmp\\\\' + self.today +'\\\\csv\\\\{}"'.format(csv_file))
        lines_to_write_data_load.append('INTO TABLE {}'.format(tbl_nm))
        lines_to_write_data_load.append('CHARACTER SET UTF8')
        lines_to_write_data_load.append('FIELDS TERMINATED BY {}'.format(field_terminator))
        lines_to_write_data_load.append('ENCLOSED BY {}'.format(enclosed_by))
        lines_to_write_data_load.append('LINES TERMINATED BY {}'.format(line_terminator))
        lines_to_write_data_load.append('IGNORE {} LINES'.format(ignore_lines))
        lines_to_write_data_load.append('(')
        for i in hdrs[:-1]:
            lines_to_write_data_load.append(i + ',')
        lines_to_write_data_load.append(hdrs[-1] + '\n);')
        return lines_to_write_data_load


    def write_lines_to_file(self, csv_file, tbl_nm, tbl_lines, data_lines, log_lines): 
        
        source_sql = 'C:\\PROD\\tmp\\' + self.today + '\\sql'
        source_stage = 'C:\\PROD\\tmp\\' + self.today + '\\sql\\stage'
        
        if not self.os.path.exists(source_sql):
            self.os.mkdir(source_sql)
        
        if not self.os.path.exists(source_stage):
            self.os.mkdir(source_stage)
            
        self.os.chdir(source_stage)
        
        with open (tbl_nm + '.sql', 'w') as f:
            for i in tbl_lines:
                f.write(i + '\n')
            for i in data_lines:
                f.write(i + '\n')
            f.write('\n')    
            for i in log_lines:
                f.write(i + '\n')
                
        self.logger.info('Conversão Concluída! Arquivo SQL gerado: {}.sql'.format(tbl_nm))
 
class ExcelToCsv():

    def __init__ (self):  
        from pyxlsb import open_workbook as open_xlsb
        from classes.mascara_data import MascaraData
        from unicodedata import normalize
        import pandas as pd
        import os, re, traceback, csv
        
        self.pc = ConfParameter()
        self.path_conf = self.pc.get_py_configger('Path')
        self.os = os
        self.csv = csv
        self.pd = pd
        self.open_xlsb = open_xlsb
        self.re = re
        self.d = MascaraData()
        self.today = self.d.get_today()
        self.normalize = normalize
        self.traceback = traceback
    
    def m_remove(self, txt, month):
        for m in month:
            txt = txt.replace(m,"")
        
        return txt
    
    #incluir parametro para receber o nome da guia e gravar o nome da guia no csvfile
    def excel_to_csv(self, excel_file, dest_csv, sheet_name):
        try:
            ext = self.os.path.splitext(excel_file)[1]
            
            if ext in (".xls", ".xlsx"):
                df = self.pd.DataFrame()
                xl = self.pd.ExcelFile(excel_file)
                 
                for sheet in xl.sheet_names:
                    if sheet == sheet_name:
                        df_tmp = xl.parse(sheet)
                        df = df.append(df_tmp, ignore_index=True)
                        
            
            elif ext == ".xlsb":
                df = []

                with self.open_xlsb(excel_file) as wb:
                    with wb.get_sheet(sheet_name) as sheet:
                            for row in sheet.rows():
                                df.append([item.v for item in row])

                df = self.pd.DataFrame(df[1:], columns=df[0])
                
            else:
                print("Formato não suportado")
                
            rm_month_abv = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
            rm_month = ["janeiro", "fevereiro", "março", "marco", "abril", "maio", 
                "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
                        
            csvfile = self.os.path.splitext(excel_file)[0]    
            csvfile = self.re.sub("\s+", "_", csvfile).lower()
            csvfile = self.normalize('NFKD', csvfile).encode('ASCII', 'ignore').decode('ASCII')
            
            csvfile = self.m_remove(csvfile,rm_month)
            csvfile = self.m_remove(csvfile,rm_month_abv)
            csvfile = csvfile.replace("_v","")   
            csvfile = csvfile.replace("sap","") 
            csvfile = csvfile.replace("scf","")           
            csvfile = csvfile.replace("consolidado","")   
            csvfile = csvfile.replace("final","")  
                      
            csvfile = self.re.sub('[^A-Za-z]+', '', csvfile).lower()
            csvfile = "stg_" + sheet_name.lower() + "_" + csvfile 
            
            arq_csv = dest_csv + csvfile + ".csv"
            
            df.to_csv(arq_csv, index=False, encoding='utf-8')
            
            file = open(arq_csv, newline='', encoding="utf8")
            numline = len(file.readlines())
            
            file.close()
            
            if (numline == 1):
                self.os.remove(arq_csv)
                    
        except Exception:
            pass
            

class ExecSQL():   

    def get_stmts(self, sql_file_path):
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            self.data = f.read().splitlines()
        self.stmt = ''
        self.stmts = []
        for line in self.data:
            if line:
                if line.startswith('--'):
                    continue
                self.stmt += line.strip() + ' '
                if ';' in self.stmt:
                    self.stmts.append(self.stmt.strip())
                    self.stmt = ''
        return self.stmts

class LogControler():   

    def __init__ (self):  
    
        from classes.mascara_data import MascaraData
        
        self.d = MascaraData()
        self.today = self.d.get_today()

    def get_stage_load(self, stg_name, csv_file):
    
        lines_stage_load = []
        lines_stage_load.append('')
        lines_stage_load.append('INSERT INTO tb_load_stage')
        lines_stage_load.append('(')
        lines_stage_load.append('anomesdia, stg_name, dt_load, nm_file')
        lines_stage_load.append(')')
        lines_stage_load.append('VALUES')
        lines_stage_load.append('(')
        lines_stage_load.append("'{}',".format(self.today))
        lines_stage_load.append("'{}',".format(stg_name))
        lines_stage_load.append("current_timestamp(),")
        lines_stage_load.append("'{}'".format(csv_file))
        lines_stage_load.append(");")
       
        return lines_stage_load           

    def get_data_prep_load(self, table_insert_name, dp_table_name ,process_name):
    
        lines_stage_load = []
        lines_stage_load.append('')
        lines_stage_load.append('INSERT INTO {}'.format(table_insert_name))
        lines_stage_load.append('(')
        lines_stage_load.append('anomesdia, dp_table_name, dt_load, process_name')
        lines_stage_load.append(')')
        lines_stage_load.append('VALUES')
        lines_stage_load.append('(')
        lines_stage_load.append("'{}',".format(self.today))
        lines_stage_load.append("'{}',".format(dp_table_name))
        lines_stage_load.append("current_timestamp(),")
        lines_stage_load.append("'{}'".format(process_name))
        lines_stage_load.append(");")
       
        return lines_stage_load        

