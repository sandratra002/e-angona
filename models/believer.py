from datetime import datetime
from database.db_manager import DatabaseManager
from models.loan import Loan

class Believer(DatabaseManager) :
    id : str; name : str; church_id : str; first_name : str; password : str
    
    def __init__(self, id = None, name = None, church_id = None,first_name = None, password = None, integration_date = None) :
        super().__init__()
        self.id = id
        self.name = name
        self.church_id = church_id
        self.first_name = first_name
        self.password = password
        self.integration_date = integration_date
        pass
    
    # Class methods
    def request_loan (self, date, amount) :
        return Loan(request_date=date, amount=amount, believer_id=self.id)
    
    # Getters and setters
    # @property
    # def integration_date (self) :
    #     return self.integration_date
    
    # @integration_date.setter 
    # def integration_date (self, value) :
    #     self.integration_date = datetime.strptime(value, "%Y-%m-%d")