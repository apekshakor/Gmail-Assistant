from sentence_transformers import CrossEncoder

print(
    "Loading cross-encoder reranker..."
)

reranker = CrossEncoder(
    'cross-encoder/ms-marco-MiniLM-L-6-v2'
)

print("Reranker ready")


def search_and_rerank(
    query,
    vector_store,
    k_retrieve=20,
    k_final=5
):
    """
    Two-stage retrieval:
    1. Bi-encoder retrieval
    2. Cross-encoder reranking
    """

    candidates = vector_store.search(
        query=query,
        k=k_retrieve
    )

    if not candidates:
        return []

    pairs = [
        (query, doc['text'])
        for doc in candidates
    ]

    scores = reranker.predict(
        pairs
    )

    # Attach rerank scores
    for doc, score in zip(
        candidates,
        scores
    ):

        doc['rerank_score'] = float(score)

    reranked = sorted(
        candidates,
        key=lambda d: d['rerank_score'],
        reverse=True
    )

    return reranked[:k_final]