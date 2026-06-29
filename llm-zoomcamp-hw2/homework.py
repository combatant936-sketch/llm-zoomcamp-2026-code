from gitsource import GithubRepositoryDataReader
from tqdm.auto import tqdm
import numpy as np
reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id="8c1834d",
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)

documents = [file.parse() for file in reader.read()]
def embeded_docs(documents):
    texts = [doc["content"] + " " + doc["filename"] for doc in documents]

    from tqdm.auto import tqdm
    import numpy as np

    batch_size = 50
    X = []

    for i in tqdm(range(0, len(texts), batch_size)):
        batch = texts[i:i + batch_size]
        batch_vectors = embed.encode_batch(batch)
        X.extend(batch_vectors)

    X = np.array(X)

    return X
# print(len(documents))
from embedder import Embedder


embed = Embedder()


X=embeded_docs(documents)


query = "How does approximate nearest neighbor search work?"
v_query = embed.encode(query)

scores = X.dot(v_query)
# print(len(scores))
print(f"Answer to Q1 {scores[0]}")

# Answer to Q1 = 0.3151876106372894


# ///2


topics=[r for r in documents if r["filename"]=="02-vector-search/lessons/07-sqlitesearch-vector.md"]


# print(topics)
embeded_docs_var=embeded_docs(topics)
    
query = "How does approximate nearest neighbor search work?"
v_query = embed.encode(query)

scores = embeded_docs_var.dot(v_query)
# print(len(scores))
# print(scores[0])
print(f"Answer to Q2 {scores[0]}")

# Answer to Q2 0.36107027225589694

## 3///

from gitsource import chunk_documents
chunks = chunk_documents(documents, size=2000, step=1000)

query = "How does approximate nearest neighbor search work?"
v_query = embed.encode(query)
embeded_docs_var=embeded_docs(chunks)
import numpy as np
scores=embeded_docs_var.dot(v_query)
idx = np.argmax(scores)

print(f"Answer to Q3 {chunks[idx]["filename"]}")


# Answer to Q3 02-vector-search/lessons/07-sqlitesearch-vector.md

from minsearch import VectorSearch
embeded_docs_var=embeded_docs(documents)
vindex = VectorSearch()
vindex.fit(embeded_docs_var, documents)

query = "What metric do we use to evaluate a search engine?"
query_vector = embed.encode(query)

results = vindex.search(query_vector, num_results=5)
# for r in results:
#     print(r["filename"])

print(f"Answer to Q4 {results[0]["filename"]}")
# 04-evaluation/lessons/05-search-metrics.md
# 04-evaluation/lessons/01-intro.md
# 01-agentic-rag/lessons/05-search.md
# 04-evaluation/lessons/15-next-steps.md
# 07-project-example/lessons/02-evaluating-retrieval.md





print("-------------------------------------------- Vector base/n")

question = "How do I store vectors in PostgreSQL?"

from minsearch import VectorSearch
embeded_docs_var=embeded_docs(documents)
vindex = VectorSearch()
vindex.fit(embeded_docs_var, documents)

query = question
query_vector = embed.encode(query)

results = vindex.search(query_vector, num_results=5)

# for r in results:
#     print(r["filename"])


from minsearch import Index

index = Index(
    text_fields=["content"],
)

index.fit(documents)




search_results = index.search(
    question,
    num_results=5
)

print("-------------------------------------------- Text base/n")

# for r in search_results:
#     print(r["filename"])

# -------------------------------------------- Vector base/n
# 02-vector-search/lessons/08-pgvector.md
# 05-monitoring/lessons/05-database.md
# 02-vector-search/lessons/02-embeddings.md
# 02-vector-search/lessons/04-vector-search.md
# 02-vector-search/lessons/07-sqlitesearch-vector.md
# -------------------------------------------- Text base/n
# 02-vector-search/lessons/02-embeddings.md
# 02-vector-search/lessons/01-intro.md
# 02-vector-search/lessons/03-embeddings-dataset.md
# 03-orchestration/lessons/05-rag.md
# 02-vector-search/lessons/10-next-steps.md


# ///Answer to question 5
# in vector but not in text

# 02-vector-search/lessons/08-pgvector.md
# 05-monitoring/lessons/05-database.md
# 02-vector-search/lessons/04-vector-search.md
# 02-vector-search/lessons/07-sqlitesearch-vector.md

print("Answer 5 in the comment")

print("-------------------------------------------- Vector base/n")

question = "How do I give the model access to tools?"

from minsearch import VectorSearch
embeded_docs_var=embeded_docs(documents)
vindex = VectorSearch()
vindex.fit(embeded_docs_var, documents)

query = question
query_vector = embed.encode(query)

results = vindex.search(query_vector, num_results=5)

# for r in results:
#     print(r["filename"])


from minsearch import Index

index = Index(
    text_fields=["content"],
)

index.fit(documents)




search_results = index.search(
    question,
    num_results=5
)

print("-------------------------------------------- Text base/n")

# for r in search_results:
#     print(r["filename"])

def rrf(result_lists, k=60, num_results=5):
    scores = {}
    docs = {}

    for results in result_lists:
        for rank, doc in enumerate(results):
            key = (doc["filename"], doc["content"])
            scores[key] = scores.get(key, 0) + 1 / (k + rank)
            docs[key] = doc

    ranked = sorted(scores, key=scores.get, reverse=True)
    return [docs[key] for key in ranked[:num_results]]

results = rrf([results, search_results])

print("rrf")
# for t in results:
#     print(t["filename"])

# 01-agentic-rag/lessons/16-other-frameworks.md
# 01-agentic-rag/lessons/13-function-calling.md
# 05-monitoring/lessons/02-assistant-setup.md
# 01-agentic-rag/lessons/14-agentic-loop.md
# 01-agentic-rag/lessons/07-llm.md

print(f"Answer to Q6 {results[0]["filename"]}")
# 01-agentic-rag/lessons/16-other-frameworks.md