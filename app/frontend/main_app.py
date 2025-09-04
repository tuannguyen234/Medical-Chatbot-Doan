import streamlit as st
import requests
import os
import unicodedata
from app.services.database_interaction import save_message


URL = "http://127.0.0.1:8001/api/v1/chatbot"
HISTORY_DB_PATH = os.getenv("HISTORY_DB_PATH", "app/database/history_dialogs/chat_history.db")

st.title("🧠 Multi-RAG Medical Chatbot")

# Khởi tạo lịch sử chat trong session_state (nếu chưa có)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list[(role, message, image_path)]

# Clean path (ảnh)
def clean_path(path: str) -> str:
    return unicodedata.normalize("NFKC", path).replace("\xa0", " ").strip()

# Input chat
query_text_input = st.chat_input("💬 Hỏi về y tế hoặc tải ảnh...")

# Nếu có tin nhắn mới từ user
if query_text_input:
    # Lưu user message
    save_message("user", query_text_input)
    st.session_state.chat_history.append(("user", query_text_input, None))

    try:
        # Gửi request tới backend
        response = requests.post(URL, json={"query": query_text_input})
        response.raise_for_status()
        data = response.json()

        answer = data.get("answer", "❌ Không có câu trả lời từ hệ thống.")
        image_paths = data.get("images", [])

        # Lưu bot message
        save_message("assistant", answer, image_path=", ".join(image_paths) if image_paths else None)
        st.session_state.chat_history.append(("assistant", answer, image_paths))

    except requests.exceptions.RequestException as e:
        st.session_state.chat_history.append(("assistant", f"❌ Lỗi khi kết nối API: {e}", None))

# 🚀 Hiển thị toàn bộ chat history (giữ context, không reload mất)
for role, message, image_paths in st.session_state.chat_history:
    st.chat_message(role).markdown(message)

    if image_paths:
        st.markdown("### 🖼 Ảnh liên quan:")
        cols = st.columns(3)
        for i, img in enumerate(set(image_paths)):  # bỏ trùng
            img_path = clean_path(img)
            if not os.path.isabs(img_path):
                img_path = os.path.join(r"D:\code\DOAN\images", img_path)
            if os.path.exists(img_path):
                with cols[i % 3]:
                    st.image(img_path, caption=os.path.basename(img_path).replace('_', ' '), use_container_width=True)
            else:
                continue
                # st.warning(f"❌ Không tìm thấy ảnh: {img_path}")
