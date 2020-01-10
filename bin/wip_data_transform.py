from classes.file_transformer_lib import ExecSQL, ConfParameter, LogControler
from classes.data_transform_lib import DataTransform
from classes.mascara_data import MascaraData
import sys, os, glob
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
    prep_user = dt.set_wrk_prep_user("TB_WRK_PREP_USER", "AUX_EMPLOYEE")
    
    log_ex = lc.get_data_prep_load("tb_load_prep", "TB_WRK_PREP_EXECUTIVE", sys.argv[0])
    log_ext = lc.get_data_prep_load("tb_load_prep", "TB_WRK_PREP_EXT", sys.argv[0])
    log_sq = lc.get_data_prep_load("tb_load_prep", "TB_WRK_PREP_SQUAD", sys.argv[0])
    log_un = lc.get_data_prep_load("tb_load_prep", "TB_WRK_PREP_UN", sys.argv[0])
    log_user = lc.get_data_prep_load("tb_load_prep", "TB_WRK_PREP_USER", sys.argv[0])

    dt.transform_prep_to_file(dp_prep, "TB_WRK_PREP_EXECUTIVE", prep_ex, log_ex)
    dt.transform_prep_to_file(dp_prep, "TB_WRK_PREP_EXT", prep_ext, log_ext)
    dt.transform_prep_to_file(dp_prep, "TB_WRK_PREP_SQUAD", prep_sq, log_sq)
    dt.transform_prep_to_file(dp_prep, "TB_WRK_PREP_UN", prep_un, log_un)
    dt.transform_prep_to_file(dp_prep, "TB_WRK_PREP_USER", prep_user, log_user)

def data_transform_alt():

    alt_ex = dt.set_wrk_alt_executive("TB_WRK_ALT_EXECUTIVE", "TB_WRK_PREP_EXECUTIVE")
    alt_ext = dt.set_wrk_alt_ext("TB_WRK_ALT_EXT", "TB_WRK_PREP_EXT")
    alt_sq = dt.set_wrk_alt_squad("TB_WRK_ALT_SQUAD", "TB_WRK_PREP_SQUAD")
    alt_un = dt.set_wrk_alt_un("TB_WRK_ALT_UN", "TB_WRK_PREP_UN")
    alt_user = dt.set_wrk_alt_user("TB_WRK_ALT_USER", "TB_WRK_PREP_USER")
    
    log_ex = lc.get_data_prep_load("tb_load_alt", "TB_WRK_ALT_EXECUTIVE", sys.argv[0])
    log_ext = lc.get_data_prep_load("tb_load_alt", "TB_WRK_ALT_EXT", sys.argv[0])
    log_sq = lc.get_data_prep_load("tb_load_alt", "TB_WRK_ALT_SQUAD", sys.argv[0])
    log_un = lc.get_data_prep_load("tb_load_alt", "TB_WRK_ALT_UN", sys.argv[0])
    log_user = lc.get_data_prep_load("tb_load_alt", "TB_WRK_ALT_USER", sys.argv[0])

    dt.transform_prep_to_file(dp_alt, "TB_WRK_ALT_EXECUTIVE", alt_ex, log_ex)
    dt.transform_prep_to_file(dp_alt, "TB_WRK_ALT_EXT", alt_ext, log_ext)
    dt.transform_prep_to_file(dp_alt, "TB_WRK_ALT_SQUAD", alt_sq, log_sq)
    dt.transform_prep_to_file(dp_alt, "TB_WRK_ALT_UN", alt_un, log_un)
    dt.transform_prep_to_file(dp_alt, "TB_WRK_ALT_USER", alt_user, log_user)

def data_transform_dim():

    dim_ex = dt.set_dim_executive("DIM_EXECUTIVE", "TB_WRK_ALT_EXECUTIVE")
    dim_ext = dt.set_dim_ext("DIM_EXT", "TB_WRK_ALT_EXT")
    dim_sq = dt.set_dim_squad("DIM_SQUAD", "TB_WRK_ALT_SQUAD")
    dim_un = dt.set_dim_un("DIM_UN", "TB_WRK_ALT_UN")
    dim_user = dt.set_dim_user("DIM_USER", "TB_WRK_ALT_USER")
    
    log_ex = lc.get_data_prep_load("tb_load_dim", "DIM_EXECUTIVE", sys.argv[0])
    log_ext = lc.get_data_prep_load("tb_load_dim", "DIM_EXT", sys.argv[0])
    log_sq = lc.get_data_prep_load("tb_load_dim", "DIM_SQUAD", sys.argv[0])
    log_un = lc.get_data_prep_load("tb_load_dim", "DIM_UN", sys.argv[0])
    log_user = lc.get_data_prep_load("tb_load_dim", "DIM_USER", sys.argv[0])

    dt.transform_prep_to_file(dp_dim, "DIM_EXECUTIVE", dim_ex, log_ex)
    dt.transform_prep_to_file(dp_dim, "DIM_EXT", dim_ext, log_ext)
    dt.transform_prep_to_file(dp_dim, "DIM_SQUAD", dim_sq, log_sq)
    dt.transform_prep_to_file(dp_dim, "DIM_UN", dim_un, log_un)
    dt.transform_prep_to_file(dp_dim, "DIM_USER", dim_user, log_user)
        
if __name__ == '__main__':

    t = MascaraData()
    today = t.get_today()
 
    lc = LogControler()
    dt = DataTransform()
    ps = ExecSQL()
    pc = ConfParameter()

    path_conf = pc.get_py_configger('Path')
    path_mysql_conn = pc.get_py_configger('MySql Connector')
    data_prep_dir = path_conf['temp'] + today + "\\sql"
    
    dp_prep = data_prep_dir + "\\prep"
    dp_alt = data_prep_dir + "\\alt"
    dp_dim = data_prep_dir + "\\dim"
    
    data_transform_prep()
    data_transform_alt()
    data_transform_dim()
    
    exec_sql_data(dp_prep)
    exec_sql_data(dp_alt)
    exec_sql_data(dp_dim)