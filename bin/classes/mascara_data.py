from classes.init_logger import InitLogger
from datetime import date

class MascaraData():

    def __init__ (self):              
        self.l = InitLogger(__name__)      
        self.logger = self.l.build_logger()    
        self.logger.debug("Diretório Data = " + self.get_today())
        
    def get_today(self):    
        self.today = date.today().strftime("%Y%m%d")        
        return self.today