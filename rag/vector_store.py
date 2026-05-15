import numpy as np

from rag.embeddings import embedding_model


class SimpleVectorStore:

    def __init__(self):

        self.vectors = None
        self.chunks = []

    def add_documents(
        self,
        chunks,
        batch_size=64
    ):
        """
        Embed all chunks and build vector store.
        """

        if not chunks:

            print("No chunks to embed.")

            return

        print(
            f"Embedding {len(chunks)} chunks..."
        )

        self.chunks = chunks

        texts = [
            chunk['text']
            for chunk in chunks
        ]

        self.vectors = embedding_model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True
        )

        print(
            f"\nVector store ready: "
            f"{self.vectors.shape[0]} chunks | "
            f"{self.vectors.shape[1]} dimensions"
        )

    def search(
        self,
        query,
        k=5
    ):
        """
        Semantic similarity search.
        """

        if (
            self.vectors is None
            or len(self.chunks) == 0
        ):

            return []

        # Query embedding
        query_vec = embedding_model.encode(
            [query],
            convert_to_numpy=True
        )[0]

        # Normalize vectors
        norm_vectors = (
            self.vectors
            / (
                np.linalg.norm(
                    self.vectors,
                    axis=1,
                    keepdims=True
                ) + 1e-10
            )
        )

        norm_query = (
            query_vec
            / (
                np.linalg.norm(query_vec)
                + 1e-10
            )
        )

        # Cosine similarity
        scores = np.dot(
            norm_vectors,
            norm_query
        )

        # Top K indices
        top_k = np.argsort(scores)[-k:][::-1]

        results = []

        for i in top_k:

            chunk = self.chunks[i]

            results.append({
                'score': float(scores[i]),
                'text': chunk['text'],
                'subject': chunk['subject'],
                'from': chunk['from'],
                'account': chunk['account'],
                'date': chunk['date'],
                'chunk_number': chunk['chunk_number']
            })

        return results