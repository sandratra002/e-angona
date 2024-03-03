from database.db_manager import DatabaseManager

class ChurchGroup (DatabaseManager) :
    def __init__(self, id = None, name = None) -> None:
        super().__init__()
        self.id = id
        self.name = name    
        pass