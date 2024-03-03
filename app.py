from models.church import Church
from utils.utils import get_sunday_id_int as ids
import datetime

try :
    # church = Church(name="Eglise Catholique Malaza", church_group_id="CHG0001")
    # church.create()
    id = ids(date="2024-4-14")
    print(id)
except Exception as e:      
    print(e)  