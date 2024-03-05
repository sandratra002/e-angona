from models.church import Church
from models.believer import Believer
from utils.utils import get_sunday_id_int as ids, get_sunday_date
import datetime

# try :
church = Church(id="CHU0001")
believer = Believer("BEL0001")
loan = believer.request_loan(date=datetime.date(2024, 2, 1), amount=600000)
church.handle_loan_request(loan=loan)
# datas = church.predict_donation(2025)
# for data in datas :
    # data.create()
    # print(f"Sunday id: {data.sunday_id} -> {data.amount}")
    # print(get_sunday_date(52, 2024))
# except Exception as e:      
    # print(e)  