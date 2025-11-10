import streamlit as st
import os
import json
from openai import OpenAI
from elevenlabs import generate, set_api_key, play  # 追加

# ------------------------------
# 🔹 APIキー設定
# ------------------------------
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")  # 追加

if not OPENAI_API_KEY:
    st.error("OpenAI APIキーが設定されていません。Secretsを確認してね。")
    st.stop()

if not ELEVENLABS_API_KEY:
    st.error("ElevenLabs APIキーが設定されていません。Secretsを確認してね。")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)
set_api_key(ELEVENLABS_API_KEY)  # ElevenLabs APIキーセット

# ------------------------------
# 🔒 パスワード認証
# ------------------------------
st.set_page_config(page_title="🎀 あかねとおしゃべり", page_icon="🎀", layout="centered")
PASSWORD = "aya_love"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password_input = st.text_input("パスワードを入力してね💬", type="password")
    if st.button("ログイン"):
        if password_input == PASSWORD:
            st.session_state.authenticated = True
            st.success("ようこそっ！あかねやで〜💖")
            st.rerun()
        else:
            st.error("ちがうで〜😢 もう一回やってみて！")
    st.stop()

# ------------------------------
# 💖 背景＆文字デザイン
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
.stMarkdown, .stText { color: #000000 !important; }
</style>
""", unsafe_allow_html=True)

st.title("🎀 あかねとおしゃべりしよ！")

# ------------------------------
# 💬 会話履歴ファイル
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

    # 新APIで応答生成
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたは明るくてフレンドリーな関西弁の女子学生『あかね』として会話します。"},
            *st.session_state["messages"]
        ]
    )

    reply = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": reply})

    # ElevenLabsで音声生成・再生
    audio = generate(
        text=reply,
        voice="YX_lfyhF0F8QjaOOX7Gb3",  # あかね用のVoiceID
        model="eleven_multilingual_v1"
    )
    play(audio)  # ブラウザで再生

    # 会話を保存
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state["messages"], f, ensure_ascii=False, indent=2)

# ------------------------------
# 💬 会話表示
# ------------------------------
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user", avatar="👤").write(msg["content"])
    else:
        st.chat_message("assistant", avatar="aya_icon.png").write(msg["content"])
