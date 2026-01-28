# def build_prompt(context_chunks, query):
#     context = "\n".join(
#         chunk if isinstance(chunk, str) else " ".join(map(str, chunk))
#         for chunk in context_chunks
#     )

#     return f"""Use the following context to answer the question.

# Context:
# {context}

# Question:
# {query}

# Answer:"""

def build_prompt(context_chunks, query):
    if not context_chunks:
        context = "No relevant context found."
    else:
        context = "\n".join(
            chunk if isinstance(chunk, str)
            else " ".join(map(str, chunk))
            for chunk in context_chunks
        )

    return f"""
You are a helpful assistant. Answer the question using ONLY the context below.
If the answer is not present in the context, say "I don't know".

Context:
{context}

Question:
{query}

Answer:
""".strip()
