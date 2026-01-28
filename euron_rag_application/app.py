# import streamlit as st
# from utils.embedding import get_embedding
# from utils.chunking import chunk_text
# from utils.retrieval import load_faiss_index, retrieve_chunk
# from utils.prompt import build_prompt
# from utils.completion import generate_completion
# from pip._vendor.urllib3 import response

# st.title("Euron RAG Application")
# st.write("This is a simple demo of a RAG application using Euron API.")

# query=st.text_input("Enter your question:")

# if query:
#     index,chunk_mapping=load_faiss_index()
#     top_chunks=retrieve_chunk(query,index,chunk_mapping)
#     prompt=build_prompt(top_chunks,query)
#     response=generate_completion(prompt)
    
#     st.subheader("Answer:")
#     st.write(response)

#     with st.expander("Retrieved Chunks"):
#         for chunk in top_chunks:
#             st.markdown(f"-{chunk}")
            
import streamlit as st
from utils.embedding import get_embedding
from utils.chucking import chunk_text
from utils.retrieval import load_faiss_index, retrieve_chunk
from utils.prompt import build_prompt
from utils.completion import generate_completion

st.set_page_config(page_title="Euron RAG", layout="wide")

st.title("🚀 Euron RAG Application")
st.write("This is a simple demo of a RAG application using Euron API.")

# ---- Load FAISS only once ----
@st.cache_resource
def load_index():
    return load_faiss_index()

index, chunk_mapping = load_index()

query = st.text_input("Enter your question:")

if st.button("Search"):
    if query.strip() == "":
        st.warning("Please enter a question")
    else:
        with st.spinner("Thinking... 🤖"):
            try:
                top_chunks = retrieve_chunk(query, index, chunk_mapping)
                prompt = build_prompt(top_chunks, query)
                answer = generate_completion(prompt)

                st.subheader("✅ Answer")
                st.write(answer)

                with st.expander("📚 Retrieved Chunks"):
                    for chunk in top_chunks:
                        st.markdown(f"- {chunk}")

            except Exception as e:
                st.error("Something went wrong")
                st.exception(e)
