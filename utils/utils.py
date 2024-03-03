import datetime
from calendar import day_name, monthcalendar
from itertools import islice

def sum(data, field_name):
  total = 0
  for item in data:
    if hasattr(item, field_name):
      total += getattr(item, field_name)
  return total

def get_sunday_id_int(date):
  date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
  if(date.weekday() != 6) : raise Exception("The date is not sunday")
  return date.isocalendar().week