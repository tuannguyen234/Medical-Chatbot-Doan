# Chatbot & Hệ thống Truy xuất Thông tin

Hệ thống kết hợp **chatbot thông minh** và **cơ sở dữ liệu tri thức**, hỗ trợ truy xuất thông tin từ FAISS, BM25, Knowledge Graph và lưu lịch sử hội thoại.

## Thành viên nhóm
- Nguyễn Tuấn – Backend & AI
- [Tên thành viên 2] – Frontend
- [Tên thành viên 3] – Database & Embedding
- [Tên thành viên 4] – NLP
- [Tên thành viên 5] – Kiểm thử & Triển khai

## Cấu hình môi trường
```bash
GOOGLE_API_KEY='your_key'
FAISS_DB_PATH='app\database\embedding_db\faiss_index_image'
FAISS_DB_IMAGE_PATH='app\database\embedding_db\faiss_VN_sbert'
BM25_DB_PATH='app\database\bm25_db\chunk_list.jsonl'
KG_DB_PATH='app\database\kg_db\corpus_KG_normalized.json'
EMBEDDING_MODEL_NAME="TuanNM171284/TuanNM171284-HaLong-embedding-medical-v5"
HISTORY_DB_PATH='app\database\history_dialogs\chat_history.db'
PROMPT_PATH='app/prompts/prompts.md'
Chạy ứng dụng
Backend API: uvicorn app.main_api:app --reload

Frontend Streamlit: streamlit run app/frontend/main_app.py

Cấu trúc dự án
bash
Copy code
app/
├─ database/       # FAISS, BM25, KG, History
├─ frontend/       # Streamlit app
├─ prompts/        # Prompt cho chatbot
└─ main_api.py     # Backend FastAPI
Công nghệ
Python, FastAPI, Streamlit, FAISS, BM25, Knowledge Graph, SBERT, SQLite
