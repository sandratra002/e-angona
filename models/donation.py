from datetime import datetime, date
from database.db_manager import DatabaseManager

class Donation (DatabaseManager) :
    id : str; church_id : str; amount : float; sunday_id : int; is_prediction : int = 1;
    
    def __init__(self, id = None, church_id = None, amount = None, date = None, sunday_id = None, is_prediction = None) -> None:
        super().__init__()
        self.id = id
        self.church_id = church_id
        self.amount = amount
        self.sunday_id = sunday_id
        self.date = date
        self.is_prediction = is_prediction
        
    def __copy__ (self) :
        return Donation(self.id, church_id=self.church_id, amount=self.amount, date=self.date, sunday_id=self.sunday_id, is_prediction=self.is_prediction)
    
    def get_donations (self, year : int, church_id : str) :
        donations = []
        try :
            with self._connection.cursor() as cursor:
                query = f"SELECT * FROM donation WHERE church_id = \'{church_id}\' AND YEAR(date) = {year}"
                cursor.execute(query)  
                data = cursor.fetchall()
                donations = [Donation().__class__(*row) for row in data]
                assert all(isinstance(obj, Donation) for obj in donations), "Unexpected object in donation list"
                return donations
        except Exception as e :
            raise e
        
    def get_donation_by_sunday (self, year : int, church_id : str, sunday_id : int) :
        try :
            with self._connection.cursor() as cursor:
                query = f"SELECT * FROM donation WHERE church_id = \'{church_id}\' AND YEAR(date) = {year} AND sunday_id = {sunday_id}"
                cursor.execute(query)  
                data = cursor.fetchone()
                donation = Donation().__class__(*data)
                return donation
        except Exception as e :
            raise e
        
    def get_variation (self, year : int, sunday_id : int) :
        try :
            with self._connection.cursor() as cursor:
                query = self.get_query(year=year, sunday_id=sunday_id)
                cursor.execute(query)  
                data = cursor.fetchone()
                return data[0]
        except Exception as e :
            raise e

    def get_average (self, year : int, sunday_id : int) :
        try :
            with self._connection.cursor() as cursor:
                query = f"""
                    SELECT 
                        AVG([amount]) AS average ,
                        [church_id] , 
                        [sunday_id]
                    FROM [Donation] 
                    WHERE YEAR([date]) < {year} AND [sunday_id] = \'{sunday_id}\'
                    GROUP BY [church_id],[sunday_id]
                """
                print(query)    
            
                cursor.execute(query)  
                data = cursor.fetchone()
                return data[0]
        except Exception as e :
            raise e

    def get_query(self, year, sunday_id):
        query = f"""
            SELECT AVG(variation) as [value] FROM 
            (
                SELECT 
                    [church_id] , 
                    [sunday_id], 
                    AVG([amount]) AS average 
                FROM [Donation] 
                WHERE YEAR([date]) < {year} AND [sunday_id] = {sunday_id}
                GROUP BY [church_id],[sunday_id]
            ) AS s , 
            (
                SELECT m.*,(o.[amount] / m.[average]) AS [variation]
                    FROM(
                        SELECT 
                            [church_id], 
                            [sunday_id], 
                            AVG([amount]) AS [average] 
                        FROM [Donation] 
                        WHERE YEAR([date]) < 2024
                        GROUP BY [church_id], [sunday_id]  
                    ) AS m 
                    JOIN [Donation] AS o 
                    ON m.[church_id] = o.[church_id] AND m.[sunday_id]=o.[sunday_id] 
                    WHERE YEAR([date]) = {year} AND o.[sunday_id] < {sunday_id}
                ) AS mv
            GROUP BY s.average
        """
        return query
        