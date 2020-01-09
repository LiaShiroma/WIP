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

    dt.transform_prep_to_file(data_prep_dir, "TB_WRK_PREP_EXECUTIVE", prep_ex)
    dt.transform_prep_to_file(data_prep_dir, "TB_WRK_PREP_EXT", prep_ext)
    dt.transform_prep_to_file(data_prep_dir, "TB_WRK_PREP_SQUAD", prep_sq)
    dt.transform_prep_to_file(data_prep_dir, "TB_WRK_PREP_UN", prep_un)

def data_transform_alt():

    alt_ex = dt.set_wrk_alt_executive("TB_WRK_ALT_EXECUTIVE", "TB_WRK_PREP_EXECUTIVE")
    alt_ext = dt.set_wrk_alt_ext("TB_WRK_ALT_EXT", "TB_WRK_PREP_EXT")
    alt_sq = dt.set_wrk_alt_squad("TB_WRK_ALT_SQUAD", "TB_WRK_PREP_SQUAD")
    alt_un = dt.set_wrk_alt_un("TB_WRK_ALT_UN", "TB_WRK_PREP_UN")

    dt.transform_prep_to_file(data_prep_dir, "TB_WRK_ALT_EXECUTIVE", alt_ex)
    dt.transform_prep_to_file(data_prep_dir, "TB_WRK_ALT_EXT", alt_ext)
    dt.transform_prep_to_file(data_prep_dir, "TB_WRK_ALT_SQUAD", alt_sq)
    dt.transform_prep_to_file(data_prep_dir, "TB_WRK_ALT_UN", alt_un)

def data_transform_dim():
    
    dim_ex = dt.set_dim_executive("DIM_EXECUTIVE", "TB_WRK_ALT_EXECUTIVE")
    dim_ext = dt.set_dim_ext("DIM_EXT", "TB_WRK_ALT_EXT")
    dim_sq = dt.set_dim_squad("DIM_SQUAD", "TB_WRK_ALT_SQUAD")
    dim_un = dt.set_dim_un("DIM_UN", "TB_WRK_ALT_UN")

    dt.transform_prep_to_file(data_prep_dir, "DIM_EXECUTIVE", dim_ex)
    dt.transform_prep_to_file(data_prep_dir, "DIM_EXT", dim_ext)
    dt.transform_prep_to_file(data_prep_dir, "DIM_SQUAD", dim_sq)
    dt.transform_prep_to_file(data_prep_dir, "DIM_UN", dim_un)
        
if __name__ == '__main__':

    t = MascaraData()
    today = t.get_today()
 
    dt = DataTransform()
    ps = ExecSQL()
    pc = ConfParameter()

    path_conf = pc.get_py_configger('Path')
    path_mysql_conn = pc.get_py_configger('MySql Connector')
    data_prep_dir = path_conf['temp'] + today + "\\sql"
    
    data_transform_prep()
    data_transform_alt()
    data_transform_dim()
    
    exec_sql_data(data_prep_dir)