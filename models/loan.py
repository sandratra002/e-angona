from database.db_manager import DatabaseManager
from datetime import datetime 

class Loan (DatabaseManager) :
    id : str; believer_id : str; amount : float

    def __init__(self, id = None, believer_id = None, amount = None, 
                 request_date = None, delivery_date = None, repay_date = None) -> None:
        super().__init__()
        self.id = id
        self.believer_id = believer_id
        self.amount = amount
        self.request_date = request_date
        self.delivery_date = delivery_date
        self.repay_date = repay_date
        
    # Getters and setters
    # @property
    # def request_date (self) :
    #     return self.request_date
    
    # @request_date.setter 
    # def request_date (self, value) :
    #     self.request_date = datetime.strptime(value, "%Y-%m-%d")
    
    # @property
    # def delivery_date (self) :
    #     return self.delivery_date
    
    # @delivery_date.setter 
    # def delivery_date (self, value) :
    #     self.delivery_date = datetime.strptime(value, "%Y-%m-%d")
        
    # @property
    # def repay_date (self) :
    #     return self.repay_date
    
    # @repay_date.setter 
    # def repay_date (self, value) :
    #     self.repay_date = datetime.strptime(value, "%Y-%m-%d")
    