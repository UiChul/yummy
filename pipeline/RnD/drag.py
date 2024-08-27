import os


root_dir = '/home/rapa/YUMMY/project/YUMMIE/seq'
seqs = os.listdir(root_dir)
# 각 샷에 대한 리스트
# shots = ['TTL_010', 'TTL_020', 'TTL_030', 'TTL_040']

# 각 작업 단계에 대한 리스트
steps = ['ani', 'cmp', 'lgt', 'ly', 'mm']

# 각 단계별 하위 디렉터리
sub_dirs = ['dev', 'pub']

# 각 하위 디렉터리 내의 폴더들
sub_folders = ['exr', 'mov', 'work']

# 루트 디렉터리 (필요에 따라 수정)
for seq in seqs:
    seq_path = os.path.join(root_dir, seq)
    shots = os.listdir(seq_path)
    print(shots)
    for shot in shots:
        for step in steps:
            for sub_dir in sub_dirs:
                for sub_folder in sub_folders:
                    # 경로 생성
                    path = os.path.join(root_dir,seq,shot, step, sub_dir, sub_folder)

                    # 디렉터리 생성
                    if os.path.isdir(path):
                        print("파일이 이미 존재")
                        break
                    os.makedirs(path, exist_ok=True)
                    print(f"Created: {path}")
