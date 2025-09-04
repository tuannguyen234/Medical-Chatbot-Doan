import os
from dotenv import load_dotenv
from typing import List, Dict
from langchain.schema import Document
import google.generativeai as genai

# Load biến môi trường từ .env
load_dotenv()

# Lấy API key từ .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ Chưa thiết lập GOOGLE_API_KEY trong .env")

# Khởi tạo Gemini client
genai.configure(api_key=GOOGLE_API_KEY)

# Model bạn muốn dùng (có thể đổi sang "gemini-1.5-pro" hoặc "gemini-1.5-flash")
MODEL_NAME = "gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)


def call_gemini_response_answer(
    question: str,
    documents: Dict = None,
    history: List[Dict[str, str]] = None,
    context: str = ""
) -> str:
    """
    Gọi Gemini LLM để sinh câu trả lời.

    :param question: câu hỏi từ user
    :param documents: list Document (nội dung từ KG/FAISS/BM25)
    :param history: list dict [{"role": "user"/"assistant", "content": "..."}]
    :param context: text context bổ sung
    :return: string câu trả lời từ Gemini
    """

    prompt = f"""
    Bạn là trợ lý y tế thông minh. Trả lời ngắn gọn, chính xác, dễ hiểu.

    Ngữ cảnh: 
    {context}

    Tài liệu tham khảo:
    {documents}

    Lịch sử hội thoại:
    {history}

    Câu hỏi người dùng:
    {question}

    Trả lời:
    """

    # Gọi Gemini
    response = model.generate_content(prompt)

    return response.text if response and response.text else "❌ Không có câu trả lời từ Gemini."

def call_gemini_response_query_optimizer(
    current_question: str,
    history: List[str]
    ) -> str:
    """
    Gọi Gemini LLM để tối ưu câu hỏi.

    :param question: câu hỏi từ user
    :return: string câu hỏi đã được tối ưu từ Gemini
    """

    prompt = f"""
    Bạn là trợ lý y tế thông minh. Nhiệm vụ của bạn là dựa và câu hỏi hiện tại và các câu hỏi trước đưa ra một câu hỏi đầy đủ thông tin và đúng ý người dùng nhất.
    Câu hỏi người dùng: {current_question}
    Các câu hỏi trước đó: {history} """

    # Gọi Gemini
    response = model.generate_content(prompt)

    return response.text if response and response.text else "❌ Không có câu trả lời từ Gemini."

if __name__ == "__main__":
    # Ví dụ gọi hàm
    answer = call_gemini_response_answer("Bệnh tiểu đường là gì?")
    print("Câu trả lời từ Gemini:", answer)
