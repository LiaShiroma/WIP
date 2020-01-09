from classes.file_transformer_lib import ExecSQL, ConfParameter
from classes.data_transform_lib import DataTransform
from classes.mascara_data import MascaraData
import os, glob
import MySQLdb

def exec_sql_data(dir):

    os.chdir(dir)

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
            
        #os.remove(g)
        
def data_transform_prep():

    prep_ex = dt.set_wrk_prep_executive("TB_WRK_PREP_EXECUTIVE", "STG_BASE_WIP_TMP")
    prep_ext = dt.set_wrk_prep_ext("TB_WRK_PREP_EXT", "STG_BASE_WIP_TMP")
    prep_sq = dt.set_wrk_prep_squad("TB_WRK_PREP_SQUAD", "STG_BASE_FATURAMENTOITAU_TMP")
    prep_un = dt.set_wrk_prep_un("TB_WRK_PREP_UN", "STG_BASE_WIP_TMP")

    dt.transform_prep_to_file(prep_dir, "TB_WRK_PREP_EXECUTIVE", prep_ex)
    dt.transform_prep_to_file(prep_dir, "TB_WRK_PREP_EXT", prep_ext)
    dt.transform_prep_to_file(prep_dir, "TB_WRK_PREP_SQUAD", prep_sq)
    dt.transform_prep_to_file(prep_dir, "TB_WRK_PREP_UN", prep_un)

# Gerar estrutua para executar alt
def data_transform_alt():

    prep_ex = dt.set_wrk_prep_executive("TB_WRK_PREP_EXECUTIVE", "STG_BASE_WIP_TMP")
    prep_ext = dt.set_wrk_prep_ext("TB_WRK_PREP_EXT", "STG_BASE_WIP_TMP")
    prep_sq = dt.set_wrk_prep_squad("TB_WRK_PREP_SQUAD", "STG_BASE_FATURAMENTOITAU_TMP")
    prep_un = dt.set_wrk_prep_un("TB_WRK_PREP_UN", "STG_BASE_WIP_TMP")

    dt.transform_prep_to_file(prep_dir, "TB_WRK_PREP_EXECUTIVE", prep_ex)
    dt.transform_prep_to_file(prep_dir, "TB_WRK_PREP_EXT", prep_ext)
    dt.transform_prep_to_file(prep_dir, "TB_WRK_PREP_SQUAD", prep_sq)
    dt.transform_prep_to_file(prep_dir, "TB_WRK_PREP_UN", prep_un)
        
if __name__ == '__main__':

    t = MascaraData()
    today = t.get_today()
 
    dt = DataTransform()
    ps = ExecSQL()
    pc = ConfParameter()

    path_conf = pc.get_py_configger('Path')
    path_mysql_conn = pc.get_py_configger('MySql Connector')
    prep_dir = path_conf['temp'] + today
    
    data_transform_prep()
    exec_sql_data(prep_dir)