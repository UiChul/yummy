import OpenEXR
import Imath
import os
import re
from collections import defaultdict

def read_exr_metadata(file_path):
    """
    EXR 파일의 메타데이터를 읽어오고 프레임 레인지를 반환하는 함수.
    """
    try:
        # EXR 파일 열기
        exr_file = OpenEXR.InputFile(file_path)
        
        # 메타데이터 읽기
        header = exr_file.header()
        frame_range = header.get("frames", "N/A")
        print(f"파일: {file_path}")
        print(f"프레임 레인지: {frame_range}")

        # 파일 닫기
        exr_file.close()
        return frame_range
    except Exception as e:
        print(f"파일을 열 수 없습니다: {file_path}. 에러: {e}")
        return None

def extract_render_set_and_frame_number(file_name):
    """
    파일 이름에서 렌더 세트와 프레임 번호를 추출하는 함수.
    파일 이름 포맷: 예를 들어 '215421_small_render1.0001.exr'
    """
    render_match = re.search(r'(.+?)\.(\d{4})\.exr', file_name)
    if render_match:
        render_set = render_match.group(1)
        frame_number = int(render_match.group(2))
        return render_set, frame_number
    return None, None

def get_frame_ranges_by_render(base_path):
    """
    디렉토리 내의 EXR 파일에서 각 렌더 세트별로 프레임 레인지를 읽어오는 함수.
    """
    render_frames = defaultdict(set)
    
    # EXR 파일 리스트
    exr_files = [f for f in os.listdir(base_path) if f.endswith(".exr")]

    for file_name in exr_files:
        file_path = os.path.join(base_path, file_name)
        
        # 렌더 세트와 프레임 번호 추출
        render_set, frame_number = extract_render_set_and_frame_number(file_name)
        
        if render_set is not None and frame_number is not None:
            render_frames[render_set].add(frame_number)
            
            # EXR 파일의 메타데이터에서 프레임 레인지 정보 읽기
            frame_range = read_exr_metadata(file_path)
            
            if frame_range and frame_range != "N/A":
                try:
                    # 프레임 레인지를 파싱하여 렌더 세트별 프레임 번호에 추가
                    start_frame, end_frame = map(int, frame_range.split("-"))
                    render_frames[render_set].update(range(start_frame, end_frame + 1))
                except ValueError:
                    print(f"프레임 레인지를 파싱할 수 없습니다: {frame_range}")

    # 각 렌더 세트별로 프레임 레인지 출력
    for render_set, frames in render_frames.items():
        if frames:
            min_frame = min(frames)
            max_frame = max(frames)
            print(f"\n렌더 세트 '{render_set}'의 프레임 레인지: {min_frame}-{max_frame}")
        else:
            print(f"렌더 세트 '{render_set}'에 대한 프레임을 찾을 수 없습니다.")

# EXR 파일이 저장된 디렉토리 경로
base_path = "/home/rapa/basic_Nuke/0726/exr"

# 각 렌더 세트별 프레임 레인지 계산
get_frame_ranges_by_render(base_path)
