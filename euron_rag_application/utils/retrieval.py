# import faiss
# import numpy as np
# import pickle
# import os
# from utils.embedding import get_embedding
# from utils.chucking import chunk_text

# def load_faiss_index():
#     if os.path.exists("faiss_store/index.faiss"):
#         index=faiss.read_index("faiss_store/index.faiss")
#         with open("faiss_store/chunk_mapping.pkl","rb") as f:
#             chunk_mapping=pickle.load(f)
#     else:
#         with open("data/founder_story.txt","r", encoding="utf-8") as f:
#             text=f.read()
#         chunks_mapping=[]
#         index=faiss.IndexFlatIP(1536)
#         for chunk in chunks:
#             emb=get_embedding(chunk)
#             index.add(np.array([emb]).astype('float32'))
#             chunk_mapping.append(chunk)
#         os.makedirs("faiss_store",exist_ok=True)
#         faiss.write_index(index,"faiss_store/index.faiss")
#         with open("faiss_store/chunk_mapping.pkl","wb") as f:
#             pickle.dump(chunk_mapping,f)
#     return index, chunk_mapping

# def retrieve_chunks(query,index,chunk_mapping,k=3):
#     query_vec=get_embedding(query)
#     D,I=index.search(np.array([query_vec]).astype('float32'),k)
#     return [chunk_mapping[i] for i in I[0]]


import faiss
import numpy as np
import pickle
import os
from utils.embedding import get_embedding
from utils.chucking import chunk_text


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FAISS_DIR = os.path.join(BASE_DIR, "faiss_store")
INDEX_PATH = os.path.join(FAISS_DIR, "index.faiss")
MAPPING_PATH = os.path.join(FAISS_DIR, "chunk_mapping.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "founder_story.txt")


def load_faiss_index():
    # If index already exists → load
    if os.path.exists(INDEX_PATH) and os.path.exists(MAPPING_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(MAPPING_PATH, "rb") as f:
            chunk_mapping = pickle.load(f)

    else:
        # Build new index
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text, max_words=100, overlap=20)

        dim = 1536  # embedding dimension
        index = faiss.IndexFlatL2(dim)   # L2 distance (safe default)
        chunk_mapping = []

        for chunk in chunks:
            emb = get_embedding(chunk)
            emb = np.array(emb, dtype=np.float32)

            # normalize (optional but good)
            faiss.normalize_L2(emb.reshape(1, -1))

            index.add(emb.reshape(1, -1))
            chunk_mapping.append(chunk)

        os.makedirs(FAISS_DIR, exist_ok=True)
        faiss.write_index(index, INDEX_PATH)

        with open(MAPPING_PATH, "wb") as f:
            pickle.dump(chunk_mapping, f)

    return index, chunk_mapping


def retrieve_chunk(query, index, chunk_mapping, k=3):
    query_vec = get_embedding(query)
    query_vec = np.array(query_vec, dtype=np.float32)

    faiss.normalize_L2(query_vec.reshape(1, -1))

    D, I = index.search(query_vec.reshape(1, -1), k)

    return [chunk_mapping[i] for i in I[0]]
