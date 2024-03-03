from database.db_manager import DatabaseManager

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
    