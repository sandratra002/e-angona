from database.db_manager import DatabaseManager
from datetime import datetime, date

class Loan (DatabaseManager) :
    id : str; believer_id : str; amount : float

    def __init__(self, id = None, believer_id = None, request_date = None, delivery_date = None, repay_date = None, amount = None, ) -> None:
        super().__init__()  
        self.id = id
        self.believer_id = believer_id
        self.amount = amount
        self.request_date = request_date
        self.delivery_date = delivery_date
        self.repay_date = repay_date
        
    def get_loan(self, church_id : str, before : bool = None, after : bool = None):
        loan = []
        try :
            with self._connection.cursor() as cursor:
                if before : query = f"SELECT id, believer_id, request_date, delivery_date, repay_date, amount FROM v_loan_church WHERE church_id = \'{church_id}\' AND request_date < \'{self.request_date.strftime("%Y-%m-%d %H:%M:%S")}\'"
                
                elif after : query = f"SELECT id, believer_id, request_date, delivery_date, repay_date, amount FROM v_loan_church WHERE church_id = \'{church_id}\' AND request_date > \'{self.request_date.strftime("%Y-%m-%d %H:%M:%S")}\'"
                
                else : raise Exception("Missing argument in get_loan(before, after)")
                
                cursor.execute(query)  
                loan = [Loan().__class__(*row) for row in cursor.fetchall()]
                assert all(isinstance(obj, Loan) for obj in loan), "Unexpected object in loan list"
                return loan
        except Exception as e :
            raise e
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
    