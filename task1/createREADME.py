import os

# 분석할 파일 목록
files = [
    "3_인어 공주.txt",
    "이효석-모밀꽃_필_무렵.txt",
    "현진건-운수_좋은_날+B3356-개벽.txt"
]

# README.TXT 파일명
output_file = "README.TXT"

def text_stats(file_path):
    """파일의 바이트 크기, 문자 수, 단어 수, 줄 수를 계산"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    text = ''.join(lines)
    
    byte_size = os.path.getsize(file_path)  # 파일 크기 (바이트)
    char_count = len(text)  # 문자 개수
    word_count = len(text.split())  # 단어 개수
    line_count = len(lines)  # 줄 개수

    return byte_size, char_count, word_count, line_count

# README.TXT 작성
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("텍스트 데이터 분석 결과\n\n")
    
    for file in files:
        byte_size, char_count, word_count, line_count = text_stats(file)
        f.write(f"파일명: {os.path.basename(file)}\n")
        f.write(f"   - 파일 크기: {byte_size} 바이트\n")
        f.write(f"   - 문자 개수: {char_count} 개\n")
        f.write(f"   - 단어 개수: {word_count} 개\n")
        f.write(f"   - 줄 개수: {line_count} 개\n")
        f.write("\n")

print(f"README.TXT 생성 완료: {output_file}")
