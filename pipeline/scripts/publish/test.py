
import os

self.increase_version("C:/Users/LEE JIYEON/Desktop/YUMMY/project/Marvelous/seq/OPN/OPN_0010/cmp/dev/work/test0825_v001.nknc")

def increase_version(self, file_path):
        """
        파일 경로 받아서 버전업하는 함수
        """
        base, ext = os.path.splitext(file_path)
        print(base)
        print(ext)
