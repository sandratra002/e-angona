from models.church import Church
from utils.utils import get_sunday_id_int as ids
import datetime

try :
    church = Church(id="CHU0001")
    data1 = church.get_fund(year=2023, sunday_id=8)
    data2 = church.get_fund(year=2024, sunday_id=8)
    print(data1)
    print(data2)
except Exception as e:      
    print(e)  