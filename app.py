from models.church_group import ChurchGroup
from models.sql_connection import SQLConnection

try :
    church_group = ChurchGroup(name="Andoharanofotsy", id="CHG0001")
    datas = church_group.read()
    for data in datas : print(data.name)
    data = church_group.read_by_id()
    print(data.id)
    church_group.update()
    church_group.delete()
except RuntimeError as err:
    print(err)  