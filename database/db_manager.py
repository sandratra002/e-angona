from database.sql_connection import SQLConnection as conn
from utils.string_utilities import to_snake_case

class DatabaseManager:
    def __init__(self) -> None:
        self._connection = conn.get_connection()
        pass
    
    def get_table_name (self) :
        return to_snake_case(type(self).__name__)
    
    def create (self) :
        try :
            with self._connection.cursor() as cursor:
                data = [(attr, getattr(self, attr)) for attr in self.__dict__.keys() if not attr.startswith("_") and not attr == "id" and not attr == "connection"]

                columns = ", ".join([item[0] for item in data])
                placeholders = ", ".join(["?"] * len(data))
                sql = f"INSERT INTO {self.get_table_name()} ({columns}) VALUES ({placeholders})"
                print(sql)
                cursor.execute(sql, [item[1] for item in data])  
                self._connection.commit()  
        except Exception as e :
            raise e   
            
    def read(self):
        try:
            with self._connection.cursor() as cursor:
                table_name = self.get_table_name() 
                sql = f"SELECT * FROM {table_name}"
                cursor.execute(sql)

                data = [self.__class__(*row) for row in cursor.fetchall()]
            return data
        except Exception as e:
            raise e
    
    def read_by_id(self):
        try :
            with self._connection.cursor() as cursor:
                table_name = self.get_table_name() 
                sql = f"SELECT * FROM {table_name} WHERE id = \'{self.id}\'"
                cursor.execute(sql)

                data = [self.__class__(*row) for row in cursor.fetchmany(1)]
            if len(data) > 0 : return data[0] 
            return None
        except Exception as e:
            raise e
    
    def update(self):
        try :
            with self._connection.cursor() as cursor:
                data = [(attr, getattr(self, attr)) for attr in self.__dict__.keys() if not attr.startswith("_") and attr != "id"]

                table_name =   self.get_table_name() 
                set_clause = ", ".join([f"{key} = ?" for key, value in data])
                where_clause = f"id = ?"  
                sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

                all_values = [value for _, value in data] + [getattr(self, "id")]
                cursor.execute(sql, all_values)
                self._connection.commit() 
        except Exception as e:
            raise e
            
    def delete(self):
        try :
            with self._connection.cursor() as cursor:
                table_name = self.get_table_name()
                where_clause = f"id = ?"  
                sql = f"DELETE FROM {table_name} WHERE {where_clause}"

                cursor.execute(sql, (getattr(self, "id"),))  
                self._connection.commit()
        except Exception as e:
            raise e
            