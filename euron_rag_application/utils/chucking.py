# def chunk_text(text,max_words=100):
#     words=text.split()
#     return [" ".join(words[i:i+max_words]) for i in range(0,len(words),max_words)]

def chunk_text(text, max_words=100, overlap=20):
    words = text.split()
    chunks = []

    step = max_words - overlap
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)

    return chunks
