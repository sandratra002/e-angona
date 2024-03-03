from database.db_manager import DatabaseManager

class Church (DatabaseManager):
    id : str; name : str; church_group_id : str;
    
    def __init__(self, id = None, name = None, church_group_id = None) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.church_group_id = church_group_id
        pass
        