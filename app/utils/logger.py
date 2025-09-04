import logging
import os
from datetime import datetime
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

# Đường dẫn gốc dự án
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Thư mục logs
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Tên file log cố định, để xoay file theo ngày
log_path = os.path.join(LOG_DIR, "app.log")

# Tạo handler xoay file theo ngày
file_handler = TimedRotatingFileHandler(
    filename=log_path,
    when='midnight',        # Xoay mỗi đêm (00:00)
    interval=1,             # Mỗi 1 ngày
    backupCount=7,          # Giữ tối đa 7 file log cũ
    encoding='utf-8',
    utc=True                # Nếu muốn dùng giờ UTC (hoặc bỏ đi nếu muốn theo giờ hệ thống)
)

file_handler.suffix = "%Y-%m-%d"  # Format tên file sau khi xoay

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        file_handler,
        logging.StreamHandler()
    ]
)

# Root logger
logger = logging.getLogger()