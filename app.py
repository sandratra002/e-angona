from models.church import Church
from utils.utils import get_sunday_id_int as ids
import datetime

try :
    church = Church(id="CHU0001")
    datas = church.get_donations(year=2023)
    for data in datas :
        print(data.amount)
except Exception as e:      
    print(e)  