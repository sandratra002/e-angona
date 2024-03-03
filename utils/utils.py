def sum(data, field_name):
  total = 0
  for item in data:
    if hasattr(item, field_name):
      total += getattr(item, field_name)
  return total