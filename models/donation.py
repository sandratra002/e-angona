from datetime import datetime, date
from database.db_manager import DatabaseManager

class Donation (DatabaseManager) :
    id : str; church_id : str; amount : float; sunday_id : int; is_prediction : int = 1;
    
    def __init__(self, id = None, church_id = None, amount = None, date = None, sunday_id = None, is_prediction = None) -> None:
        super().__init__()
        self.id = id
        self.church_id = church_id
        self.amount = amount
        self.sunday_id = sunday_id
        self.date = date
        self.is_prediction = is_prediction
        
    def __copy__ (self) :
        return Donation(self.id, church_id=self.church_id, amount=self.amount, date=self.date, sunday_id=self.sunday_id, is_prediction=self.is_prediction)
    # @property
    # def date (self) :
    #     return self.date
    
    # @date.setter 
    # def date (self, value) :
    #     if (not value == None) :
    #         if (isinstance(value, str)) :
    #             self.date = datetime.strptime(value, "%Y-%m-%d")
    #         if (isinstance(value, date)) :
    #             self.date = value
        