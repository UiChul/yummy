# # new_path = []
# # nk_new_path = "a"
# # exr_new_path = "b"
# # mov_new_path = "c"
# # new_path.extend([nk_new_path, exr_new_path, mov_new_path])

# # print(new_path)

# import re

# # a = os.path.basename("C:/Users/LEE JIYEON/Desktop/YUMMY/project/Marvelous/seq/OPN/OPN_0010/cmp/dev/work")
# # print(a)
# base = "C:/Users/LEE JIYEON/Desktop/YUMMY/project/Marvelous/seq/OPN/OPN_0010/cmp/dev/work/test0825_v002"
# version_pattern = re.compile("v\d{3}")
# match = version_pattern.search(base)
# # print(match)
# current_version = match.group(0)
# new_number = int(current_version[1:]) + 1
# new_version = f"v{new_number:03}"   # 현재 버전 번호가 존재하면 버전 번호를 증가
# print(new_number)
# print(new_version)

# a = base.replace(current_version, new_version)

# print(a)


# import shutil
# original = "C:/Users/LEE JIYEON/Desktop/YUMMY/project/Marvelous/seq/OPN/OPN_0010/cmp/dev/source/mov/test_v002.mov"
# change = "C:/Users/LEE JIYEON/Desktop/YUMMY/project/Marvelous/seq/OPN/OPN_0010/cmp/dev/source/mov/test_v003.mov"
# shutil.copy2(original, change)

base = "work/"
file = "abc.ext"

print(base+file)
