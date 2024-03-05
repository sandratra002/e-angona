from datetime import datetime
from database.db_manager import DatabaseManager

class Fund (DatabaseManager) :
    id : str; church_id : str; amount : float
    
    def __init__(self, id = None, church_id = None, date = None, amount = None) -> None:
        super().__init__()
        
        self.id = id
        self.church_id = church_id
        self.date = date
        self.amount = amount
        
    # Getters and setters
    # @property
    # def date (self) :
    #     return self.date
    
    # @date.setter 
    # def date (self, value) :
    #     self.date = datetime.strptime(value, "%Y-%m-%d")
        