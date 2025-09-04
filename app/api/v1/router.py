from app.services.embedding_search import *
from app.services.kg_search import KnowledgeGraphService
from app.services.keyword_search import search as bm25_search
from app.services.call_llm import call_gemini_response_answer, call_gemini_response_query_optimizer
from fastapi import APIRouter, HTTPException
import sqlite3, os
from dotenv import load_dotenv
import httpx
from typing import List,Dict
from pydantic import BaseModel, Field
from app.utils.logger import logger
from app.services.database_interaction import get_last_messages, get_last_user_queries
load_dotenv()
HISTORY_DB_PATH = os.getenv("HISTORY_DB_PATH", "app/database/history_dialogs/chat_history.db")
app = APIRouter()

class Query(BaseModel):
    query: str = Field(..., example="What are the symptoms of diabetes?")
    
@app.post("/chatbot")
async def answer(question: Query):
    """
    Trả lời câu hỏi dựa trên 3 nguồn:
    - KG search
    - Embedding search (FAISS)
    - Keyword search (BM25)
    Trả về câu trả lời từ nguồn đầu tiên có kết quả
    """
    logger.info(f"\n🤖 User question: {question.query}")
    print(f"\n🤖 User question: {question.query}")
    query_optimizer = call_gemini_response_query_optimizer(question.query, get_last_user_queries())
    print(f"\n🤖 User question optimizer: {query_optimizer}")

    results = {}
    # 1. KG search
    kg_db = os.getenv("KG_DB_PATH", "data/kg_db.json")
    kg = KnowledgeGraphService(kg_db)
    kg_results = await kg.search(query_optimizer)
    answers = []
    for r in kg_results:
        if not r['neighbors']:
            continue
        print(f"\n🎯 Node: {r['node']}")
        for n in r["neighbors"]:
            if n['target'] and n['relationship']:
                answers.append(f"- {n['relationship']} → {n['target']}")
                # print(f"  ➡ {n['relationship']} → {n['target']}")

        print(f"🔍 KG found {len(answers)} answers.")
        results["KG"] = answers

    # 2. Embedding search
    faiss_db = await load_faiss_db()
    docs = faiss_db.similarity_search(query_optimizer, k=3)
    image_path = await user_input_images(query_optimizer)
    if docs:
        print(f"🔍 Embedding found {len(docs)} documents.")
        results["Embedding"] = {"image_path:": image_path, 
                                "documents": docs}


    # 3. Keyword search (BM25)
    bm25_results = await bm25_search(query_optimizer, top_k=3)
    if bm25_results:
        print(f"🔍 BM25 found {len(bm25_results)} documents.")
        answers = [f"- {doc} (Score: {score:.4f})" for doc, score in bm25_results]
        results["BM25"] = answers
    # Chuẩn bị câu trả lời
    answer = call_gemini_response_answer(
        question=query_optimizer,
        documents= results.get("Embedding", {}).get("documents", []),
        history=get_last_messages(),
        context="\n".join(results.get("KG", [])) + "\n" + "\n".join(results.get("BM25", []))
    )
    # print(f"get_last_messages {get_last_messages()}")

    final_results = {
        "answer": answer,
        "images": results.get("Embedding", {}).get("image_path:", [])
    }
    # print(results)
    # Nếu không có kết quả từ cả 3 nguồn
    return final_results if results else {"message": "Không tìm thấy thông tin phù hợp."}
