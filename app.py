import pyodbc

connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=Sandratra;DATABASE=e-angona;UID=Aina;PWD=aina'
conn = pyodbc.connect(connectionString)