import datetime
from datetime import date, timedelta
from calendar import day_name, monthcalendar
from itertools import islice

def sum(data, field_name):
  total = 0
  for item in data:
    if hasattr(item, field_name):
      total += getattr(item, field_name)
  return total

def get_sunday_id_int(date):
  date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
  if(date.weekday() != 6) : raise Exception("The date is not sunday")
  return date.isocalendar().week

def get_week_day_id (date : date) :
    date = date.split(" ")[0]
    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    return date.isocalendar().week

def calculate_proportion(num1, num2):
  if num2 == 0:
    return 0  

  proportion = (num1 / num2) 
  return round(proportion, 2)  

def get_first_january(year):
  return date(year, 1, 1)

def get_first_sunday(year) :
  for i in range (1, 8) :
    temp = date(year, 1, i)
    if temp.weekday() == 6 : return temp
 
def get_sunday_date(sunday_id, year):
  if not (1 <= sunday_id <= 52) or year < 1:
    raise ValueError("Invalid Sunday ID or year")

  first_sunday = get_first_sunday(year)
   
  return first_sunday + timedelta(days=(sunday_id - 1) * 7)

def to_datetime (date : str) :
  print(date)
  cal = date.split("T")[0]
  hour = date.split("T")[1]
  hour += ":00"
  print(f"Changed valueeee {cal + " " + hour}")
  return cal + " " + hour

def get_next_sunday(dt):
  while (dt.weekday() != 6) :
    dt = dt + timedelta(days=1)
  return dt