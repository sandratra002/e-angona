from database.db_manager import DatabaseManager
from utils.utils import calculate_proportion, get_sunday_date, get_sunday_id_int, get_week_day_id, get_next_sunday
from models.donation import Donation
from models.loan import Loan
from models.fund import Fund
from datetime import date, timedelta

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
                    row = cursor.fetchone()
                    fund = Fund(*row)
                    return fund
                else : return Fund(amount=cursor.fetchone()[0])
        except Exception as e :
            raise e 
    
    def calculate_percentage(self, year : int, sunday_id) :
        past_year_fund = self.get_fund(year=year-1, sunday_id=sunday_id)
        current_year_fund = self.get_fund(year=year, sunday_id=sunday_id)
        percentage = calculate_proportion(current_year_fund, past_year_fund)
        return percentage
        
    def predict_donation (self, year : int) -> [Donation]:
        result = []
        donation = Donation()
        if(year == 2024):
            donations = donation.get_donations(year=year, church_id=self.id)
            print("Donations lengthhh 57 : " , len(donations))
            if(len(donations) < self.week_count) :
                result = [*donations]
                percentage = self.calculate_percentage(2024, len(donations)) 
                past_year = donation.get_donations(year=2023, church_id=self.id)
                for i in range (len(donations), 52) :
                    temp = past_year[i].__copy__()
                    temp.date = get_sunday_date(i, 2024)
                    temp.amount = temp.amount * percentage
                    
                    result.append(temp)
            else : result = donations
        else : 
            past_year = donation.get_donations(year=year - 1, church_id=self.id)
            if len(past_year) >= self.week_count : raise Exception("Cannot predict cause past year is no complete")
            percentage = self.calculate_percentage(2024, 52) 
            for i in range (0, 52) :
                temp = past_year[i].__copy__()
                temp.date = get_sunday_date(temp.sunday_id, year=year)
                temp.amount = temp.amount * percentage
                result.append(temp)
                
        for donation in result : 
            print("Creating")
            donation.create()
        return result
    
    def predict_delivery_date (self, donations, amount, fund, sunday_id) :
        if (sunday_id == 52) : 
            donations = self.predict_donation(donations[20].date.year + 1)
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
        
    def handle_loan_request (self, loan : Loan, is_first = True) -> Loan:
        loan_before = loan.get_loan(church_id=self.id, before=True)
        loan_after = loan.get_loan(church_id=self.id, after=True)
        if len(loan_before) > 0 :
            latest_loan = loan_before[len(loan_before) - 1]
            lateset_delivery_date = latest_loan.delivery_date
            
            fund = self.get_fund_at(lateset_delivery_date)
            donations = self.predict_donation(loan.request_date.year)
            
            obj = self.predict_delivery_date(donations=donations, amount=loan.amount, fund=fund.amount, sunday_id=get_week_day_id(str(loan.request_date)))

            loan.delivery_date = obj["delivery_date"]
            
            self.save_loan_request(loan=loan, obj=obj, is_first=is_first)
        else :
            
            donations = self.predict_donation(loan.request_date.year)
            
            fund = self.get_fund_at(loan.request_date, first_time=True)
            
            obj = self.predict_delivery_date(donations=donations, amount=loan.amount, fund=fund.amount, sunday_id=get_week_day_id(str(loan.request_date)))

            self.save_loan_request(loan=loan, obj=obj, is_first = is_first)
            
        if(is_first):
            for temp in loan_after :
                self.handle_loan_request(temp, is_first=False)
            
    def save_loan_request (self, loan : Loan, obj, is_first : bool = True) -> None:
        loan.delivery_date = obj["delivery_date"]
        if(is_first) :
            loan.create()
        else : 
            loan.update()
        
        fund = Fund(church_id=self.id, date=loan.delivery_date, amount=obj["fund"])
        fund.create()
        return None
    
    def predict_date (self, loan : Loan) :
        donation = Donation()
        last_fund = Fund().get_last_fund()
        
        sunday = get_next_sunday(loan.request_date)
        id = get_sunday_id_int(sunday.strftime("%Y-%m-%d %H:%M:%S"))
        avg = donation.get_average(year=loan.request_date.year, sunday_id=id)
        
        variation = donation.get_variation(year=loan.request_date.year, sunday_id=id)
        average = donation.get_average(loan.request_date.year, id)
        
        print(f"Variation :: {variation}")
        print(f"Average :: {average}")
        
        if (not last_fund) :
            amount = variation * average
            print(f"Amount :: {amount}")
            last_fund = Fund()
            last_fund.amount = amount
            last_fund.date = sunday
            last_fund.church_id = self.id
            last_fund.create()
            
        temp_fund = last_fund.amount
        while ( temp_fund < loan.amount ):
            average = donation.get_average(year=loan.request_date.year, sunday_id=id + 1)
            amount = average * variation
            
            temp_fund += amount
            sunday = sunday + timedelta(7)
        
        loan.delivery_date = sunday
        loan.create()
        
        new_fund = Fund(church_id=self.id, date=sunday, amount=temp_fund)
        new_fund.create()
        
        return loan