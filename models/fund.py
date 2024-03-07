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
        
    def get_last_fund (self) :
        try:
            with self._connection.cursor() as cursor:
                table_name = self.get_table_name() 
                sql = f"SELECT TOP 1 * FROM {table_name} ORDER BY date"
                cursor.execute(sql)

                data = [self.__class__(*row) for row in cursor.fetchall()]
            if len(data) > 0 : return data[0] 
        except Exception as e:
            raise e
    # Getters and setter
        