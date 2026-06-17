"""임베딩 모듈 - sentence-transformers 또는 TF-IDF 폴백"""

from __future__ import annotations

from typing import Any

import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """두 벡터 간 코사인 유사도"""
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


class Embedder:
    """텍스트 임베딩 - sentence-transformers 우선, TF-IDF 폴백"""

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self._model = None
        self._tfidf_vectorizer = None
        self._texts: list[str] = []
        self._backend = "none"

        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(model_name)
            self._backend = "sentence-transformers"
            print(f"  임베딩: sentence-transformers ({model_name})")
        except Exception:
            print("  임베딩: sentence-transformers 불가 - TF-IDF 폴백 사용")
            self._backend = "tfidf"

    @property
    def backend(self) -> str:
        return self._backend

    def embed(self, texts: list[str]) -> np.ndarray:
        """텍스트 리스트를 임베딩 벡터로 변환 (N x dim)"""
        if not texts:
            return np.array([])

        if self._backend == "sentence-transformers" and self._model is not None:
            return np.asarray(self._model.encode(texts, show_progress_bar=False), dtype=np.float32)
        return self._tfidf_embed(texts)

    def _tfidf_embed(self, texts: list[str]) -> np.ndarray:
        """TF-IDF 기반 임베딩 (폴백)"""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
        except ImportError:
            # 최후의 폴백: 단순 문자열 길이 기반 더미 임베딩
            return np.random.rand(len(texts), 64)

        if self._tfidf_vectorizer is None or len(texts) != len(self._texts):
            self._tfidf_vectorizer = TfidfVectorizer(
                max_features=128, sublinear_tf=True
            )
            self._texts = texts
            fit_matrix: Any = self._tfidf_vectorizer.fit_transform(texts)
            return np.asarray(fit_matrix.toarray(), dtype=np.float32)
        else:
            transform_matrix: Any = self._tfidf_vectorizer.transform(texts)
            return np.asarray(transform_matrix.toarray(), dtype=np.float32)

    def compute_similarity_matrix(
        self, texts: list[str]
    ) -> np.ndarray:
        """모든 텍스트 쌍의 코사인 유사도 행렬 계산"""
        embeddings = self.embed(texts)
        if embeddings.size == 0:
            return np.array([])

        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)
        normalized = embeddings / norms
        return normalized @ normalized.T

    def find_cross_link_candidates(
        self,
        page_titles: list[str],
        page_texts: list[str],
        top_k: int = 3,
        min_similarity: float = 0.3,
    ) -> dict[int, list[dict[str, object]]]:
        """각 페이지에 대해 코사인 유사도 상위 k개를 크로스링크 후보로 추출"""
        sim_matrix = self.compute_similarity_matrix(page_texts)
        candidates: dict[int, list[dict[str, object]]] = {}

        for i in range(len(page_titles)):
            sims = sim_matrix[i]
            # 자기 자신 제외
            sims[i] = -1.0
            top_indices = np.argsort(sims)[::-1][:top_k]

            candidates[i] = []
            for idx in top_indices:
                sim_val = float(sims[idx])
                if sim_val >= min_similarity:
                    candidates[i].append({
                        "target_index": int(idx),
                        "target_title": page_titles[idx],
                        "cosine_sim": round(sim_val, 4),
                    })

        return candidates
