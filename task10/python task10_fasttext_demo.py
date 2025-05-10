"""
Word Embedding 실습 스크립트 (FastText 버전)
⦁ 영어 NLTK movie_reviews 코퍼스 → fastText Skip-gram 학습
⦁ 유사도 / 아날로지 계산 → 출력
⦁ t-SNE 시각화 → PNG 저장
실행:  python task10_fasttext_demo.py
"""

import os, re, random, pathlib, itertools, math
import nltk, fasttext, fasttext.util
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

# ──────────────────────────────────────────────
## 1) 데이터 준비
print("▶ NLTK corpus download / preprocess …")
nltk.download('movie_reviews', quiet=True)
sents = [" ".join(tokens) for tokens in nltk.corpus.movie_reviews.sents()]
corpus_path = pathlib.Path("movie_reviews.txt")
corpus_path.write_text("\n".join(sents), encoding="utf-8")
print(f"✓ 영화리뷰 문장수 = {len(sents):,}")

# ──────────────────────────────────────────────
## 2) FastText Skip-gram 학습
print("\n▶ fastText training … (10 epoch, 200-dim)")
model = fasttext.train_unsupervised(
    str(corpus_path),
    model="skipgram",
    dim=200,
    ws=5,
    epoch=10,
    minn=3, maxn=6,   # subword
    thread=os.cpu_count() or 4
)
model.save_model("movie_reviews_ft.bin")
print("✓ 모델 저장: movie_reviews_ft.bin")

# ──────────────────────────────────────────────
## 3) 유사도 & 아날로지
def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v) + 1e-9)

print("\n▶ 단어 유사도(actor ~ actress)")
sim = cosine(model.get_word_vector("actor"), model.get_word_vector("actress"))
print(f"    cosine(actor, actress) = {sim:.4f}")

def analogy(a, b, c, topn=5):
    target = model.get_word_vector(a) - model.get_word_vector(b) + model.get_word_vector(c)
    words, scores = [], []
    for w in itertools.islice(model.get_words(), 50000):   # 상위 5만 단어만 탐색
        v = model.get_word_vector(w)
        score = cosine(target, v)
        words.append(w); scores.append(score)
    best = sorted(zip(words, scores), key=lambda x: -x[1])
    return [w for w, _ in best if w not in (a, b, c)][:topn]

print("▶ 아날로지: king - man + woman ≈ ?")
print("   ", analogy("king", "man", "woman", 5))

# ──────────────────────────────────────────────
## 4) t-SNE 시각화
print("\n▶ t-SNE (500 words) → png …")
words = model.get_words()[:500]
vecs  = np.vstack([model.get_word_vector(w) for w in words])

tsne  = TSNE(n_components=2, perplexity=40, random_state=0, n_iter=1200)
coords = tsne.fit_transform(vecs)

plt.figure(figsize=(12, 8))
plt.scatter(coords[:, 0], coords[:, 1], s=8)
for (x, y), w in zip(coords, words):
    plt.annotate(w, (x, y), fontsize=8)
plt.title("t-SNE of FastText vectors (top-500 movie-review words)")
plt.tight_layout()
plt.savefig("tsne_fasttext_movie_reviews.png", dpi=200)
print("✓ 시각화 파일: tsne_fasttext_movie_reviews.png")

print("\n🎉 실습 완료!  스크립트가 생성한 PNG와 콘솔 결과를 과제 보고서에 캡처하세요.")
