def to_snake_case (str:str):
  word = []
  index = 0
  print('G'.islower())
  for char in str :
    if(char.isupper() and index == 0): word.append(char.lower())
    elif (char.isupper() and not index == 0) : word.append("_" + char.lower())
    else : word.append(char)
    index += 1
  return "".join(word)
