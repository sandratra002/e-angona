from database.db_manager import DatabaseManager
from utils.utils import calculate_proportion 
from models.donation import Donation
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
                return cursor.fetchmany(1)[0][0]
        except Exception as e :
            raise e 
        
    def calculate_percentage(self, year : int, sunday_id) :
        past_year_fund = self.get_fund(year=year-1, sunday_id=sunday_id)
        current_year_fund = self.get_fund(year=year, sunday_id=sunday_id)
        percentage = calculate_proportion(current_year_fund, past_year_fund)
        return percentage
    
    def get_donations (self, year : int) :
        donations = []
        try :
            with self._connection.cursor() as cursor:
                query = f"SELECT * FROM Donation WHERE church_id = \'{self.id}\' AND YEAR(date) = {year}"
                cursor.execute(query)  
                donations = [Donation().__class__(*row) for row in cursor.fetchall()]
                return donations
        except Exception as e :
            raise e
    
    