from database.db_manager import DatabaseManager
from utils.utils import calculate_proportion, get_sunday_date, get_sunday_id_int, get_week_day_id
from models.donation import Donation
from models.loan import Loan
from models.fund import Fund

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
        
    def get_fund_at (self, date, first_time = False) :
        # Get fund for a specific date
        try :
            with self._connection.cursor() as cursor:
                if not first_time : query = f"SELECT * FROM fund WHERE church_id = \'{self.id}\' AND date = \'{date}\'"
                else : query = f"SELECT SUM(amount) FROM donation WHERE church_id = \'{self.id}\' AND date <= \'{date}\' AND YEAR(date) = {date.year}"
                cursor.execute(query)  
                if not first_time :
                    return Fund().__class__(cursor.fetchmany(1)[0][0])
                else : return Fund(amount=cursor.fetchone()[0])
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
                if before : query = f"SELECT * FROM v_loan_church WHERE church_id = \'{self.id}\' AND request_date > \'{before}\'"
                elif after : query = f"SELECT * FROM v_loan_church WHERE church_id = \'{self.id}\' AND request_date < \'{after}\'"
                else : raise Exception("One date is atleast required")
                cursor.execute(query)  
                loan = [Loan().__class__(*row) for row in cursor.fetchall()]
                assert all(isinstance(obj, Loan) for obj in loan), "Unexpected object in loan list"
                return loan
        except Exception as e :
            raise e
        
    def predict_donation (self, year : int) -> [Donation]:
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
            else : result = donations
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
            donations = self.predict_donation(donations[51].date.year + 1)
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
            fund = self.get_fund_at(lateset_delivery_date)
            donations = self.predict_donation(loan.request_date.year)
            obj = self.predict_delivery_date(donations=donations, amount=loan.amount, fund=fund.amount, sunday_id=get_week_day_id(loan.request_date))
            print(obj)
        else :
            donations = self.predict_donation(loan.request_date.year)
            fund = self.get_fund_at(loan.request_date, first_time=True)
            print(f"Fund amount : {fund.amount}")
            obj = self.predict_delivery_date(donations=donations, amount=loan.amount, fund=fund.amount, sunday_id=get_week_day_id(str(loan.request_date)))
            
        for loan in loan_after :
            self.handle_loan_request(self, loan)
            
    def save_loan_request (self, loan : Loan, obj) -> None:
        fund = Fund(church_id=self.id, date=loan.delivery_date, amount=obj.fund)
        fund.create()

        
        
        loan.create()
        return None