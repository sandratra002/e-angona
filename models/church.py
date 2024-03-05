from database.db_manager import DatabaseManager
from utils.utils import calculate_proportion, get_sunday_date
from models.donation import Donation
from models.loan import Loan
from models.fund import Fund
from copy import deepcopy

class Church (DatabaseManager):
    id : str; name : str; church_group_id : str;
    
    week_count = 52;
    
    def __init__(self, id = None, name = None, church_group_id = None) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.church_group_id = church_group_id
        pass
        
    def get_fund(self, year : int, sunday_id : int) -> float:
        # Get fund for prediction
        try :
            with self._connection.cursor() as cursor:
                query = f"SELECT SUM(amount) FROM donation WHERE church_id = \'{self.id}\' AND YEAR(date) = {year} AND sunday_id < {sunday_id}"
                cursor.execute(query)  
                return cursor.fetchmany(1)[0][0]
        except Exception as e :
            raise e 
        
    def get_fund_at (self, date) :
        # Get fund for a specific date
        try :
            with self._connection.cursor() as cursor:
                query = f"SELECT * FROM fund WHERE church_id = \'{self.id}\' AND date = \'{date}\'"
                cursor.execute(query)  
                return Fund().__class__(cursor.fetchmany(1)[0][0])
        except Exception as e :
            raise e 
    
    def calculate_percentage(self, year : int, sunday_id) :
        past_year_fund = self.get_fund(year=year-1, sunday_id=sunday_id)
        current_year_fund = self.get_fund(year=year, sunday_id=sunday_id)
        percentage = calculate_proportion(current_year_fund, past_year_fund)
        return percentage
    
    def get_donations (self, year : int) -> [Donation] :
        donations = []
        try :
            with self._connection.cursor() as cursor:
                query = f"SELECT * FROM donation WHERE church_id = \'{self.id}\' AND YEAR(date) = {year}"
                cursor.execute(query)  
                data = cursor.fetchall()
                for row in data : print(row)
                donations = [Donation().__class__(*row) for row in data]
                assert all(isinstance(obj, Donation) for obj in donations), "Unexpected object in donation list"
                return donations
        except Exception as e :
            raise e
    
    def get_loan(self, before = None, after = None) -> [Loan]:
        loan = []
        try :
            with self._connection.cursor() as cursor:
                if before : query = f"SELECT * FROM loan WHERE church_id = \'{self.id}\' AND request_date > {before}"
                elif after : query = f"SELECT * FROM loan WHERE church_id = \'{self.id}\' AND request_date < {after}"
                else : raise Exception("One date is atleast required")
                cursor.execute(query)  
                loan = [Loan().__class__(*row) for row in cursor.fetchall()]
                assert all(isinstance(obj, Loan) for obj in loan), "Unexpected object in loan list"
                return loan
        except Exception as e :
            raise e
        
    def predict_donation (self, year : int) :
        result = []
        if(year == 2024):
            donations = self.get_donations(year)
            if(len(donations) < self.week_count) :
                percentage = self.calculate_percentage(2024, len(donations)) 
                past_year = self.get_donations(2023)
                for i in range (len(donations), 52) :
                    temp = past_year[i].__copy__()
                    temp.date = get_sunday_date(i, 2024)
                    temp.amount = temp.amount * percentage
                    result.append(temp)
        else : 
            past_year = self.get_donations(year - 1)
            if len(past_year) != self.week_count : raise Exception("Cannot predict cause past year is no complete")
            percentage = self.calculate_percentage(2024, 52) 
            print(percentage)
            for i in range (0, 52) :
                    temp = past_year[i].__copy__()
                    temp.date = get_sunday_date(temp.sunday_id, year=year)
                    temp.amount = temp.amount * percentage
                    print(i)
                    result.append(temp)
        return result
    
    def predict_delivery_date (self, donations, amount, fund, sunday_id) :
        if (sunday_id == 52) : 
            donations = self.predict_donation(donations[51].date.year)
            sunday_id = 1
            
        index = sunday_id - 1
        
        donation = donations[index]
        temp = fund + donation.amount
        if (temp >= amount) :
            return {
                "delivery_date" : get_sunday_date(sunday_id= sunday_id, year=donation.date.year),
                 "fund" : temp - amount
                }   
        else :
            fund = temp
            sunday_id += 1
            return self.predict_delivery_date(donations=donations, amount=amount, fund=fund, sunday_id=sunday_id)
        
    def handle_loan_request (self, loan : Loan) -> Loan:
        loan_before = self.get_loan(before=loan.request_date)
        loan_after = self.get_loan(after=loan.request_date)
        if len(loan_before) > 0 :
            latest_loan = loan_before[len(loan_before) - 1]
            lateset_delivery_date = latest_loan.delivery_date
            fund = self.get_fund(lateset_delivery_date)
            