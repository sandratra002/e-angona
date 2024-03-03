from database.db_manager import DatabaseManager

class Church (DatabaseManager):
    def __init__(self, id = None, name = None, group_id = None) -> None:
        self.id = id
        self.name = name
        self.group_id = group_id
        pass
        
    