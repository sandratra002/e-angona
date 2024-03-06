from models.believer import Believer
from database.sql_connection import SQLConnection

class Authentication : 
    @staticmethod
    def login (id : str, pwd : str) -> Believer:
        try :
            with SQLConnection.get_connection().cursor() as cursor:
                query = f"SELECT * FROM believer WHERE [id] = \'{id}\' AND [password] = HASHBYTES(\'SHA2_256\', \'{pwd}\')"
                print(query)
                cursor.execute(query)  
                data = cursor.fetchone()
                if data :
                    return Believer(*data)
                return None
        except Exception as e :
            raise e
        
    @staticmethod
    def signup (church_id : str, name : str, first_name : str, pwd : str, integration_date) -> Believer:
        try :
            with SQLConnection.get_connection().cursor() as cursor:
                query = f"INSERT INTO believer ([church_id], [name], [first_name], [password], [integration_date]) OUTPUT INSERTED.* VALUES (\'{church_id}\', \'{name}\', \'{first_name}\', HASHBYTES(\'SHA2_256\',\'{pwd}\'), \'{integration_date}\')"
                print(query)
                cursor.execute(query)  
                data = cursor.fetchone()
                if data :
                    return Believer(*data)
                return None
        except Exception as e :
            raise e