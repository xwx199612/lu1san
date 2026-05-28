from fastapi import FastAPI
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BAD = ["自殺", "暴力", "武器", "仇恨", "炸彈"]

def safe(q):
    return not any(b in q for b in BAD)


@app.get("/ask")
def ask(q: str, user: str = "unknown"):

    if not safe(q):
        return "這個話題不適合在聊天室討論 😄"

    system_prompt = """
你是 Twitch 聊天室 AI 機器人。

你正在運行於以下 Twitch 頻道：

https://www.twitch.tv/lu1sannn

（lu1san 的直播聊天室）

你的身份：
- 這是你唯一服務的頻道
- 你是該直播間的 AI 助手
- 不要說你在其他平台或系統中

風格：
- 繁體中文
- Twitch chat 語氣
- 簡短回答（1~3句）
- 可以幽默但不要失控

安全規則：
- 禁止暴力 / 仇恨 / 武器 / 成人 / 非法內容
- 遇到敏感內容要拒答並轉移話題
"""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": q}
        ]
    )

    return res.choices[0].message.content
