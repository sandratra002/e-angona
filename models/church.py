from database.db_manager import DatabaseManager

class Church (DatabaseManager):
    id : str; name : str; church_group_id : str;
    
    def __init__(self, id = None, name = None, church_group_id = None) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.church_group_id = church_group_id
        pass
        
    def get_fund(self, year : int, sunday_id : int) -> float:
        try :
            with self._connection.cursor() as cursor:
                query = f"SELECT SUM(amount) FROM Donation WHERE church_id = \'{self.id}\' AND YEAR(date) = {year} AND sunday_id < {sunday_id}"
                cursor.execute(query)  
                return cursor.fetchmany(1)
        except Exception as e :
            raise e 
    