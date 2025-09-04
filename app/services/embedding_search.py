import streamlit as st
import sqlite3
import os
import unicodedata
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from app.services.read_md_file import read_prompts

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

FAISS_DB_PATH = os.getenv("FAISS_DB_PATH")
FAISS_DB_IMAGE_PATH = os.getenv("FAISS_DB_IMAGE_PATH")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")


# Dùng sync vì HuggingFaceEmbeddings không phải async
def embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)


async def load_faiss_db():
    return FAISS.load_local(
        folder_path=FAISS_DB_PATH,
        embeddings= embedding_model(),
        allow_dangerous_deserialization=True
    )

async def get_chain():
    prompts = read_prompts('Prompt template có thêm lịch sử hội thoại')

    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    prompt = PromptTemplate(
        template=prompts,
        input_variables=["context", "question", "history"]
    )
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)


# Clean path (ảnh)
def clean_path(path: str) -> str:
    return unicodedata.normalize("NFKC", path).replace("\xa0", " ").strip()


async def user_input_images(query):
    # Load FAISS index
    vector_store = FAISS.load_local(r"D:\code\RAG\faiss_index_image", embedding_model(), allow_dangerous_deserialization=True)
    
    # Get top K results
    results = vector_store.similarity_search(query)
    print(type(results[0]))
    print(results[0])
    if results:
        matched_descriptions = [r.page_content for r in results]  # Extract descriptions
        # Connect to SQLite & retrieve matching image paths
        conn = sqlite3.connect('D:\code\DOAN\image_database copy.db')
        cursor = conn.cursor()
        
        placeholders = ",".join(["?"] * len(matched_descriptions))  # Create ?,?,? for SQL query
        cursor.execute(f"SELECT image_path FROM images WHERE description IN ({placeholders})", matched_descriptions)
        
        image_paths = [row[0] for row in cursor.fetchall()]  # Fetch all results
        conn.close()

        # return image_paths if image_paths else None
        prompt_template = read_prompts("Prompt xử lí path ảnh")
        # tạo prompt
        prompt = f"{prompt_template}\n\nCâu hỏi: {query}\n\nDanh sách ảnh:\n" + "\n".join(image_paths)

        # gọi model
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        list_images = [clean_path(i.strip()) for i in response.text.split('\n') if i.strip()]
        list_images = list(set(list_images))  # bỏ trùng
    return list_images

# Main sync entrypoint
async def main():
    user_query = "Bệnh addison là gì?"

    db = await load_faiss_db()
    docs = db.similarity_search(user_query, 2)
    print(f"docs: {docs}")

    # Tìm ảnh liên quan
    image_paths = await user_input_images(user_query)
    print(f"image_paths: {image_paths}")

    chain =await get_chain()
    response = chain(
        {"input_documents": docs, "question": user_query, "context": "", "history": ""}
    )
    print(f"response: {response}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
