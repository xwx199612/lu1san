from fastapi import FastAPI
import time
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

app = FastAPI()
client = OpenAI(api_key="YOUR_KEY")

CACHE = {"about": "", "game": "Just Chatting", "t": 0}

def refresh():
    if time.time() - CACHE["t"] < 600:
        return

    try:
        html = requests.get("https://www.twitch.tv/lu1san").text
        soup = BeautifulSoup(html, "html.parser")

        meta = soup.find("meta", {"name": "description"})
        CACHE["about"] = meta["content"] if meta else "No info"
    except:
        CACHE["about"] = "No info"

    CACHE["game"] = "Just Chatting"
    CACHE["t"] = time.time()


BAD = ["自殺", "炸彈", "暴力", "武器", "仇恨"]

def safe(q):
    return not any(b in q for b in BAD)


@app.get("/ask")
def ask(q: str, user: str = "unknown"):

    if not safe(q):
        return "這個話題不適合在聊天室討論 😄"

    refresh()

    system_prompt = f"""
你是 lu1san Twitch AI 助手。

【主播資訊】
{CACHE['about']}

【直播分類】
{CACHE['game']}

規則：
- 禁止暴力 / 仇恨 / NSFW / 武器 / 非法內容
- Twitch chat 風格
- 繁體中文
- 不要太長
"""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": q}
        ]
    )

    return res.choices[0].message.content