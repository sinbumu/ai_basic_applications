import os
from konlp.kma.klt2023 import klt2023
from konlpy.tag import Okt, Kkma, Komoran, Hannanum

# 분석기 초기화
klt = klt2023()
okt = Okt()
kkma = Kkma()
komoran = Komoran()
hannanum = Hannanum()

# 분석할 폴더 경로 (현재 스크립트 기준)
target_folder = os.path.dirname(__file__)

# 분석 대상 텍스트 파일들만 가져오기
txt_files = [f for f in os.listdir(target_folder) if f.endswith(".txt")]

print(f"분석할 파일 목록: {txt_files}")

for file in txt_files:
    file_path = os.path.join(target_folder, file)
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    output_lines = []

    output_lines.append(f"\n=== {file} 분석 결과 ===\n")

    # KLT2000
    output_lines.append("[KLT2000 분석]")
    output_lines.append("형태소: " + str(klt.morphs(text[:100])))
    output_lines.append("명사: " + str(klt.nouns(text[:100])))
    output_lines.append("품사: " + str(klt.pos(text[:100])))

    # KoNLPy 분석기들
    output_lines.append("\n[Okt 분석]")
    output_lines.append(str(okt.pos(text[:100])))

    output_lines.append("\n[Kkma 분석]")
    output_lines.append(str(kkma.pos(text[:100])))

    try:
        output_lines.append("\n[Komoran 분석]")
        output_lines.append(str(komoran.pos(text[:100])))
    except Exception as e:
        output_lines.append("\n[Komoran 분석] 실패: " + str(e))

    output_lines.append("\n[Hannanum 분석]")
    output_lines.append(str(hannanum.pos(text[:100])))

    # 결과 파일 저장
    output_file = os.path.join(target_folder, f"output-{file}")
    with open(output_file, "w", encoding="utf-8") as out:
        out.write("\n".join(output_lines))

    # 화면 출력 일부
    print(f"\n✅ {file} 분석 완료 — 결과는 {output_file}에 저장됨.")
    print("▶ 요약 출력 (KLT2000 명사):", klt.nouns(text[:100]))
