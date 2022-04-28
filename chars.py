from string import printable


buff = '['
for char in printable:
    buff = buff + f'"ascii_{char}",'
buff = buff[:-2]+']'
print(buff)