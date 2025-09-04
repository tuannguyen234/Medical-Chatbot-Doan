import re
import os
from dotenv import load_dotenv
load_dotenv()
def read_prompts(prompt_type: str) -> str:
    PROMPT_PATH = os.getenv("PROMPT_PATH", "app/prompts/prompts.md")
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Split prompts by headings (## Prompt Name)
    prompts = re.split(r"##\s+", content)[1:]  # Skip anything before first heading
    prompt_dict = {}
    for p in prompts:
        lines = p.strip().split("\n")
        name = lines[0].strip()
        text = "\n".join(lines[1:]).strip()
        prompt_dict[name] = text
    return prompt_dict[prompt_type]
if __name__ == "__main__":
    print(read_prompts("Prompt template có thêm lịch sử hội thoại"))
