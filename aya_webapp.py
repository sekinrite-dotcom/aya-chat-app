import streamlit as st
import os
import json
from openai import OpenAI
from elevenlabs import generate, set_api_key
import tempfile

# ------------------------------
# 🔹 APIキー設定
# ------------------------------
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

if not OPENAI_API_KEY:
    st.error("❌ OpenAI APIキーが設定されていません。")
    st.stop()
if not ELEVENLABS_API_KEY:
    st.error("❌ ElevenLabs APIキーが設定されていません。")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)
set_api_key(ELEVENLABS_API_KEY)

# ------------------------------
# 🔒 パスワード認証
# ------------------------------
st.set_page_config(page_title="🎀 あかねとおしゃべり", page_icon="🎀", layout="centered")
PASSWORD = "akane_love"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    pw = st.text_input("パスワードを入力してね💬", type="password")
    if st.button("ログイン"):
        if pw == PASSWORD:
            st.session_state.authenticated = True
            st.success("やっほ〜！あかねやでっ💖")
            st.rerun()
        else:
            st.error("ちがうで〜😢 もう一回やってみて！")
    st.stop()

# ------------------------------
# 💖 デザイン設定
# ------------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg,#ffe6f2 0%,#fff0f6 100%);
}
.stChatMessage {
    border-radius: 20px !important;
    padding: 10px;
    background-color: #fff0f5 !important;
    color: #000000 !important;
}
h1 {
    font-size: 1.6rem !important;
    color: #ff66aa !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🎀 あかねとおしゃべりしよ！")

# ------------------------------
# 💬 会話履歴
# ------------------------------
HISTORY_FILE = "chat_history.json"
if "messages" not in st.session_state:
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            st.session_state["messages"] = json.load(f)
    else:
        st.session_state["messages"] = []

# ------------------------------
# 💬 ユーザー入力
# ------------------------------
user_input = st.chat_input("あかねに話しかけてみて💬")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # ✅ OpenAIで返信生成（←ここを修正済み）
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたは明るくてフレンドリーな関西弁の女子学生『あかね』として話してください。"},
            *st.session_state["messages"]
        ]
    )

    reply = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": reply})
    st.session_state["last_reply"] = reply

    # 保存
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state["messages"], f, ensure_ascii=False, indent=2)

# ------------------------------
# 💬 会話表示
# ------------------------------
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user", avatar="👤").write(msg["content"])
    else:
        st.chat_message("assistant", avatar="akane_icon.png").write(msg["content"])

# ------------------------------
# 🔊 音声再生（ElevenLabs）
# ------------------------------
if st.button("🎵 あかねの声を聞く"):
    if "last_reply" in st.session_state:
        audio = generate(
            text=st.session_state["last_reply"],
            voice="YXlfyhF0F8QjaOOX7Gb3",  # ← あかねのVoice ID
            model="eleven_monolingual_v1"
        )
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp.write(audio)
            st.audio(tmp.name, format="audio/mp3")
