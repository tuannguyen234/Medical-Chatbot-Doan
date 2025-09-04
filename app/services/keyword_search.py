# pip install rank-bm25
from rank_bm25 import BM25Okapi
import json
from app.utils.logger import logger
# --- Load dữ liệu từ file ---
json_path = r"D:\code\DOAN\Neo4j\knowledge-graph-llms\medical_chatbot\Medical-Chatbot-Doan\app\database\bm25_db\bm25_corpus.json"

with open(json_path, 'r', encoding='utf-8') as f:
    documents = json.load(f)

# --- Tiền xử lý: tokenize đơn giản ---
tokenized_docs = [doc.split() for doc in documents]

# --- Khởi tạo BM25 ---
bm25 = BM25Okapi(tokenized_docs)

# --- Hàm query ---
async def search(query: str, top_k: int = 5):
    tokenized_query = query.split()
    scores = bm25.get_scores(tokenized_query)
    # Lấy index của top-k scores lớn nhất
    top_indexes = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    results = [(documents[i], scores[i]) for i in top_indexes]
    return results

# --- Test ---
if __name__ == "__main__":
    import asyncio
    query = "triệu chứng của bệnh tiểu đường"
    results = asyncio.run(search(query, top_k=3))
    for doc, score in results:
        print(f"Score: {score:.4f} | Doc: {doc[:100]}...")
