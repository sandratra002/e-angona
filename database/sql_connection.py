import pyodbc

class SQLConnection:
    @staticmethod
    def get_connection():
        # db_conf = json.load("../conf/database.json")
        connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=Sandratra;DATABASE=e-angona;UID=Aina;PWD=aina'
        conn = pyodbc.connect(connectionString)
        return conn