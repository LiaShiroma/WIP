class DataTransform():

    def __init__ (self):  

        from classes.mascara_data import MascaraData
        import os
        
        self.os = os
        self.d = MascaraData()
        self.today = self.d.get_today()
        
    def set_wrk_prep_executive(self, tb_wrk_prep_name, stg_name):

        wrk_prep_executive = []
        wrk_prep_executive.append("DROP TABLE IF EXISTS {};".format(tb_wrk_prep_name))
        wrk_prep_executive.append("CREATE TABLE {} AS".format(tb_wrk_prep_name))
        wrk_prep_executive.append("	SELECT")
        wrk_prep_executive.append("		{} AS ANOMESDIA,".format(self.today))  
        wrk_prep_executive.append("		(@ROW_NUMBER:=@ROW_NUMBER + 1) AS ID_EXECUTIVE,") 
        wrk_prep_executive.append("		 E.PROJECT_MANAGER_NAME AS NM_EXECUTIVE,") 
        wrk_prep_executive.append("		 NULL AS ID_SAP,")
        wrk_prep_executive.append("		NULL AS DT_INIT,")
        wrk_prep_executive.append("STR_TO_DATE('31/12/2100', '%d/%m/%Y') AS DT_END")
        wrk_prep_executive.append("	FROM") 
        wrk_prep_executive.append("	(SELECT DISTINCT PROJECT_MANAGER_NAME FROM {}) AS E,".format(stg_name)) 
        wrk_prep_executive.append("	(SELECT @ROW_NUMBER:=(SELECT IFNULL(MAX(ID_EXECUTIVE), 0) FROM DIM_EXECUTIVE)) AS RN;")
        
        return wrk_prep_executive

    def set_wrk_prep_un(self, tb_wrk_prep_name, stg_name):
        
        wrk_prep_un = []
        wrk_prep_un.append("DROP TABLE IF EXISTS {};".format(tb_wrk_prep_name))
        wrk_prep_un.append("CREATE TABLE {} AS".format(tb_wrk_prep_name))
        wrk_prep_un.append("SELECT")
        wrk_prep_un.append("	{} AS ANOMESDIA,".format(self.today))
        wrk_prep_un.append("	(@ROW_NUMBER:=@ROW_NUMBER + 1) AS ID_UN,")
        wrk_prep_un.append("	 U.UN AS NM_UN,")
        wrk_prep_un.append("	NULL AS DT_INIT,")
        wrk_prep_un.append("	STR_TO_DATE('31/12/2100', '%d/%m/%Y') AS DT_END")
        wrk_prep_un.append("FROM")
        wrk_prep_un.append("(SELECT DISTINCT UN FROM {}) AS U,".format(stg_name))
        wrk_prep_un.append("(SELECT @ROW_NUMBER:=(SELECT IFNULL(MAX(ID_UN), 0) FROM DIM_UN)) AS RN;")

        return wrk_prep_un
        
    def set_wrk_prep_ext(self, tb_wrk_prep_name, stg_name):

        wrk_prep_ext = []
        wrk_prep_ext.append("DROP TABLE IF EXISTS {};".format(tb_wrk_prep_name))
        wrk_prep_ext.append("CREATE TABLE {} AS".format(tb_wrk_prep_name))
        wrk_prep_ext.append("SELECT")
        wrk_prep_ext.append("		{} AS ANOMESDIA,".format(self.today)) 
        wrk_prep_ext.append("		 E.project AS ID_EXT,")
        wrk_prep_ext.append("         NULL AS NM_EXT,")
        wrk_prep_ext.append("         NULL AS DT_INIT,")
        wrk_prep_ext.append("		 STR_TO_DATE('31/12/2100', '%d/%m/%Y') AS DT_END")
        wrk_prep_ext.append("	FROM")
        wrk_prep_ext.append("	(SELECT DISTINCT project FROM {}) AS E;".format(stg_name))
                
        return wrk_prep_ext

    def set_wrk_prep_squad(self, tb_wrk_prep_name, stg_name):

        wrk_prep_squad = []
        wrk_prep_squad.append("DROP TABLE IF EXISTS {};".format(tb_wrk_prep_name))
        wrk_prep_squad.append("CREATE TABLE {} AS".format(tb_wrk_prep_name))
        wrk_prep_squad.append("SELECT")
        wrk_prep_squad.append("	{} AS ANOMESDIA,".format(self.today))
        wrk_prep_squad.append("	S.ID_SQUAD,")
        wrk_prep_squad.append("    NULL AS NM_SQUAD,")
        wrk_prep_squad.append("	NULL AS DT_INIT,")
        wrk_prep_squad.append("	STR_TO_DATE('31/12/2100', '%d/%m/%Y') DT_END")
        wrk_prep_squad.append("FROM")
        wrk_prep_squad.append("(SELECT DISTINCT SUBSTR(agrupamento, 1, 5) AS ID_SQUAD")
        wrk_prep_squad.append("FROM {}) AS S;".format(stg_name))

        return wrk_prep_squad 
        
    def set_wrk_alt_executive(self, tb_wrk_alt_name, prep_name):

        wrk_alt_executive = []
        wrk_alt_executive.append("TRUNCATE TABLE {};".format(tb_wrk_alt_name))
        wrk_alt_executive.append("INSERT INTO {}".format(tb_wrk_alt_name))
        wrk_alt_executive.append("SELECT ")
        wrk_alt_executive.append("	prp.ANOMESDIA,")
        wrk_alt_executive.append("	prp.ID_EXECUTIVE,")
        wrk_alt_executive.append("	prp.NM_EXECUTIVE,")
        wrk_alt_executive.append("	prp.ID_SAP,")
        wrk_alt_executive.append("	prp.DT_INIT,")
        wrk_alt_executive.append("	prp.DT_END,")
        wrk_alt_executive.append("	IF(ISNULL(dim.NM_EXECUTIVE),'I', ")
        wrk_alt_executive.append("	IF((prp.DT_END <> dim.DT_END),'E', 'N')) AS COD_INDCD_ALT")
        wrk_alt_executive.append("FROM {} prp".format(prep_name))
        wrk_alt_executive.append("LEFT JOIN DIM_EXECUTIVE dim")
        wrk_alt_executive.append("ON prp.ID_EXECUTIVE = dim.ID_EXECUTIVE;")

        return wrk_alt_executive

    def set_wrk_alt_un(self, tb_wrk_alt_name, prep_name):

        wrk_alt_un = []
        wrk_alt_un.append("TRUNCATE TABLE {};".format(tb_wrk_alt_name))
        wrk_alt_un.append("INSERT INTO {}".format(tb_wrk_alt_name))
        wrk_alt_un.append("SELECT")
        wrk_alt_un.append("		prp.ANOMESDIA,")
        wrk_alt_un.append("		prp.ID_UN,")
        wrk_alt_un.append("		prp.NM_UN,")
        wrk_alt_un.append("		prp.DT_INIT,")
        wrk_alt_un.append("		prp.DT_END,")
        wrk_alt_un.append("IF(ISNULL(dim.NM_UN),'I', ")
        wrk_alt_un.append("IF((prp.DT_END <> dim.DT_END),'E', 'N')) AS COD_INDCD_ALT")
        wrk_alt_un.append("FROM {} prp".format(prep_name))
        wrk_alt_un.append("LEFT JOIN DIM_UN dim")
        wrk_alt_un.append("ON prp.ID_UN = dim.ID_UN;")

        return wrk_alt_un

    def set_wrk_alt_ext(self, tb_wrk_alt_name, prep_name):

        wrk_alt_ext = []
        wrk_alt_ext.append("TRUNCATE TABLE {};".format(tb_wrk_alt_name))
        wrk_alt_ext.append("INSERT INTO {}".format(tb_wrk_alt_name))
        wrk_alt_ext.append("SELECT ")
        wrk_alt_ext.append("		prp.ANOMESDIA,")
        wrk_alt_ext.append("		prp.ID_EXT,")
        wrk_alt_ext.append("		prp.NM_EXT,")
        wrk_alt_ext.append("		prp.DT_INIT,")
        wrk_alt_ext.append("		prp.DT_END,")
        wrk_alt_ext.append("IF(ISNULL(dim.ID_EXT),'I', ")
        wrk_alt_ext.append("IF((prp.NM_EXT <> dim.NM_EXT),'A', ")
        wrk_alt_ext.append("IF((prp.DT_END <> dim.DT_END),'E','N'))) AS COD_INDCD_ALT")
        wrk_alt_ext.append("FROM {} prp".format(prep_name))
        wrk_alt_ext.append("LEFT JOIN DIM_EXT dim")
        wrk_alt_ext.append("ON prp.ID_EXT = dim.ID_EXT;")
        
        return wrk_alt_ext

    def set_wrk_alt_squad(self, tb_wrk_alt_name, prep_name):

        wrk_alt_squad = []
        wrk_alt_squad.append("TRUNCATE TABLE {};".format(tb_wrk_alt_name))
        wrk_alt_squad.append("INSERT INTO {}".format(tb_wrk_alt_name))
        wrk_alt_squad.append("SELECT ")
        wrk_alt_squad.append("		prp.ANOMESDIA,")
        wrk_alt_squad.append("		prp.ID_SQUAD,")
        wrk_alt_squad.append("		prp.NM_SQUAD,")
        wrk_alt_squad.append("		prp.DT_INIT,")
        wrk_alt_squad.append("		prp.DT_END,")
        wrk_alt_squad.append("IF(ISNULL(dim.ID_SQUAD),'I', ")
        wrk_alt_squad.append("IF((prp.NM_SQUAD <> dim.NM_SQUAD),'A', ")
        wrk_alt_squad.append("IF((prp.DT_END <> dim.DT_END),'E','N'))) AS COD_INDCD_ALT")
        wrk_alt_squad.append("FROM {} prp".format(prep_name))
        wrk_alt_squad.append("LEFT JOIN DIM_SQUAD dim")
        wrk_alt_squad.append("ON prp.ID_SQUAD = dim.ID_SQUAD;")
        
        return wrk_alt_squad
        
    def set_dim_executive(self, tb_dim_name, alt_name):

        prep_dim_executive = []
        prep_dim_executive.append("INSERT INTO {}".format(tb_dim_name))
        prep_dim_executive.append("SELECT DISTINCT ANOMESDIA,")
        prep_dim_executive.append("ID_EXECUTIVE,")
        prep_dim_executive.append("NM_EXECUTIVE,")
        prep_dim_executive.append("ID_SAP,")
        prep_dim_executive.append("DT_INIT,")
        prep_dim_executive.append("DT_END")
        prep_dim_executive.append("FROM {}".format(alt_name))
        prep_dim_executive.append("WHERE COD_INDCD_ALT IN('I','A');")

        return prep_dim_executive

    def set_dim_squad(self, tb_dim_name, alt_name):

        prep_dim_squad = []
        prep_dim_squad.append("INSERT INTO {}".format(tb_dim_name))
        prep_dim_squad.append("SELECT DISTINCT ANOMESDIA,")
        prep_dim_squad.append("ID_SQUAD,")
        prep_dim_squad.append("NM_SQUAD,")
        prep_dim_squad.append("DT_INIT,")
        prep_dim_squad.append("DT_END")
        prep_dim_squad.append("FROM {}".format(alt_name))
        prep_dim_squad.append("WHERE COD_INDCD_ALT IN('I','A');")

        return prep_dim_squad

    def set_dim_ext(self, tb_dim_name, alt_name):

        prep_dim_ext = []
        prep_dim_ext.append("INSERT INTO {}".format(tb_dim_name))
        prep_dim_ext.append("SELECT DISTINCT ANOMESDIA,")
        prep_dim_ext.append("ID_EXT,")
        prep_dim_ext.append("NM_EXT,")
        prep_dim_ext.append("DT_INIT,")
        prep_dim_ext.append("DT_END")
        prep_dim_ext.append("FROM {}".format(alt_name))
        prep_dim_ext.append("WHERE COD_INDCD_ALT IN('I','A');")

        return prep_dim_ext

    def set_dim_un(self, tb_dim_name, alt_name):

        prep_dim_un = []
        prep_dim_un.append("INSERT INTO {}".format(tb_dim_name))
        prep_dim_un.append("SELECT DISTINCT ANOMESDIA,")
        prep_dim_un.append("ID_UN,")
        prep_dim_un.append("NM_UN,")
        prep_dim_un.append("DT_INIT,")
        prep_dim_un.append("DT_END")
        prep_dim_un.append("FROM {}".format(alt_name))
        prep_dim_un.append("WHERE COD_INDCD_ALT ='I';")

        return prep_dim_un

    def set_dim_user(self, tb_dim_name, alt_name):

        prep_dim_user = []
        prep_dim_user.append("INSERT INTO {}".format(tb_dim_name))
        prep_dim_user.append("SELECT DISTINCT ANOMESDIA,")
        prep_dim_user.append("ITAU_EMPLOYEE_NAME,")
        prep_dim_user.append("ID_SAP ,")
        prep_dim_user.append("ID_FUNC ,")
        prep_dim_user.append("EVERIS_EMPLOYEE_NAME,")
        prep_dim_user.append("DT_INIT")
        prep_dim_user.append("FROM {}".format(alt_name))
        prep_dim_user.append("WHERE COD_INDCD_ALT IN('I','A');")

        return prep_dim_user

    def transform_prep_to_file(self, source_sql, tbl_nm, tbl_wrk_prep): 
    
        sq = source_sql
        
        if not self.os.path.exists(sq):
            self.os.mkdir(sq)
        
        self.os.chdir(sq)
        
        with open (tbl_nm.lower() + '.sql', 'w') as f:
            for i in tbl_wrk_prep:
                f.write(i + '\n')