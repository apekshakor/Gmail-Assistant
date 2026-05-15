from sentence_transformers import SentenceTransformer
import os 
# Load embedding model once

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models",
    "all-MiniLM-L6-v2"
)

embedding_model = SentenceTransformer(MODEL_PATH)


def generate_embedding(text):
    """
    Generate embedding for a single text.
    """

    return embedding_model.encode(text)


def generate_embeddings(text_list):
    """
    Generate embeddings for multiple texts.
    """

    return embedding_model.encode(text_list)