from datetime import datetime
from database.db_manager import DatabaseManager

class Donation (DatabaseManager) :
    id : str; church_id : str; amount : float; sunday_id : int; is_prediction : int;
    
    def __init__(self, id = None, church_id = None, amount = None, sunday_id = None, date = None, is_prediction = None) -> None:
        super().__init__()
        self.id = id
        self.church_id = church_id
        self.amount = amount
        self.sunday_id = sunday_id
        self.date = date
        self.is_prediction = is_prediction
        
    @property
    def date (self) :
        return self.date
    
    @date.setter 
    def date (self, value) :
        self.date = datetime.strptime(value, "%Y-%m-%d")