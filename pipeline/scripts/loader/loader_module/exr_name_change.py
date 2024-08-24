import os

# 변경할 폴더 경로를 입력하세요


folder_path = "/home/rapa/YUMMY/project/YUMMIE/seq/INS/INS_010/lgt/dev/exr/INS_010_lgt_v003"

# 폴더 내 모든 파일을 가져옵니다
files = os.listdir(folder_path)

# 파일 이름 변경 및 삭제 작업을 수행합니다
for filename in files:
    file_path = os.path.join(folder_path, filename)
    
    if filename.startswith('OPN_0010_ani_v003.') and filename.endswith('.exr'):
        # 기존 파일 번호 추출
        file_number = filename.split('.')[1]
        new_filename = f'INS_0010_lgt_v003.{file_number}.exr'
        
        # 새로운 파일 경로 생성
        new_file_path = os.path.join(folder_path, new_filename)
        
        # 파일 이름 변경
        os.rename(file_path, new_file_path)
    
    elif not filename.endswith('.exr'):
        # 확장자가 .exr가 아닌 파일 삭제
        os.remove(file_path)

print("파일 이름 변경 및 삭제 완료")
