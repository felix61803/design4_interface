from numpy import arange
import numpy as np

my_data = [27, 35, 10, 5,2,4,5,6,7,4,3,1,5,45,3,4,123,124,235,346,547,234,1234,1234,56]
ech = 0.1

line = 8

mod = len(my_data)%line
factor = len(my_data)/line
print(factor)
if mod == 0:
    factor = int(factor)
else:
    factor = int(factor)+1

new_line = len(my_data)/factor
print("new nb_line : ",int(new_line))

ech_modif = round(factor*ech,10)

print(factor)
for i in range(int(new_line)):
    print(my_data[i*factor],ech_modif)




