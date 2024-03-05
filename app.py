from models.church import Church
from utils.utils import get_sunday_id_int as ids, get_sunday_date
import datetime

try :
    # church = Church(id="CHU0001")
    # datas = church.get_donations(year=2023)
    # for data in datas :
    #     print(data.amount)
    print(get_sunday_date(52, 2024))
except Exception as e:      
    print(e)  