from models.church import Church

try :
    church = Church(name="Eglise Catholique Malaza", church_group_id="CHG0001")
    church.create()
except Exception as e:
    print(e)  