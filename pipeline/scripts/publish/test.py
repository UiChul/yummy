import re

file_name = "OddddN_0010_comp_v001.nknc"
p = re.compile("O....N")
print (p.match(file_name))