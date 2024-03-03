from database.db_manager import DatabaseManager

class Believer(DatabaseManager) :
    name : str; church_id : str; first_name : str; password : str
    
    def __init__(self, name = None, church_id = None,first_name = None, password = None) :
        super().__init__()
        self.name = name
        self.church_id = church_id
        self.first_name = first_name
        self.password = password
        pass
        