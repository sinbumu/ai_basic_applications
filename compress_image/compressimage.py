import os
import sys
from PIL import Image
import shutil

def compress_image(input_path, output_path, max_size_bytes=1024*1024):
    # 원본 파일 크기 확인
    original_size = os.path.getsize(input_path)
    
    # 이미 크기가 작으면 그대로 복사
    if original_size <= max_size_bytes:
        shutil.copy2(input_path, output_path)
        print(f"복사됨: {os.path.basename(input_path)} (이미 1MB 미만)")
        return
    
    # 이미지 열기
    img = Image.open(input_path)
    
    # 초기 품질
    quality = 90
    
    # 압축 시도
    while quality > 10:
        try:
            img.save(output_path, "JPEG", quality=quality, optimize=True)
            new_size = os.path.getsize(output_path)
            
            if new_size <= max_size_bytes:
                print(f"압축됨: {os.path.basename(input_path)} (품질: {quality}%, 크기: {new_size/1024:.2f} KB)")
                return
            
            # 품질 낮추기
            quality -= 10
        except Exception as e:
            print(f"오류 발생: {os.path.basename(input_path)} - {str(e)}")
            return
    
    # 최저 품질로도 안되면 마지막 시도
    try:
        img.save(output_path, "JPEG", quality=10, optimize=True)
        print(f"경고: {os.path.basename(input_path)} - 최저 품질로 저장됨")
    except Exception as e:
        print(f"오류 발생: {os.path.basename(input_path)} - {str(e)}")

def process_directory(source_dir, output_dir):
    # 출력 디렉토리 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 모든 파일과 하위 디렉토리 처리
    for root, dirs, files in os.walk(source_dir):
        # 상대 경로 계산
        rel_path = os.path.relpath(root, source_dir)
        # 출력 디렉토리 생성
        if rel_path != ".":
            curr_output_dir = os.path.join(output_dir, rel_path)
            if not os.path.exists(curr_output_dir):
                os.makedirs(curr_output_dir)
        else:
            curr_output_dir = output_dir
        
        # 파일 처리
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                input_path = os.path.join(root, file)
                output_path = os.path.join(curr_output_dir, file)
                compress_image(input_path, output_path)

if __name__ == "__main__":
    # 경로 설정
    source_dir = r"C:\Users\sinbu\Desktop\국민대_특수대학원_수업\2025_1학기_수업\데이터분석 (714250b-01)\12주차\재활용품 분류하기\재활용품 분류하기\recyclable_materials"
    output_dir = os.path.join(source_dir, "_compressed")
    
    process_directory(source_dir, output_dir)
    print(f"완료! 압축된 이미지는 {output_dir} 에 저장되었습니다.")
