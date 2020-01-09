from classes.file_transformer_lib import ExecSQL, ConfParameter
from classes.mascara_data import MascaraData
import os, glob
import MySQLdb

def main():

    mydb = MySQLdb.connect(host=path_mysql_conn['host'],
        user=path_mysql_conn['user'],
        passwd=path_mysql_conn['passwd'],
        db=path_mysql_conn['db'])
    

    for g in glob.glob("*.sql"):
        
        stmts = ps.get_stmts(g)

        with mydb.cursor() as cursor:
            for stmt in stmts:
                cursor.execute(stmt)
            mydb.commit()
            
        os.remove(g)

if __name__ == '__main__':

    t = MascaraData()
    today = t.get_today()
    
    ps = ExecSQL()
    pc = ConfParameter()
    
    path_conf = pc.get_py_configger('Path')
    path_mysql_conn = pc.get_py_configger('MySql Connector') 

    dest_sql = path_conf['temp'] + today + '\\sql\\'
    os.chdir(dest_sql)
    
    main()