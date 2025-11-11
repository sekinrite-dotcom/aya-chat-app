import streamlit as st
import os
from openai import OpenAI
import tempfile

# ------------------------------
# 🔹 OpenAI API Key
# ------------------------------
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OpenAI APIキーが設定されていません。Secretsを確認してね。")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

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
h1 { font-size: 1.5rem !important; text-align:center; }
</style>
""", unsafe_allow_html=True)

st.title("🎀 あかねとおしゃべりしよ！")

# ------------------------------
# 💬 会話履歴
# ------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ------------------------------
# 💬 ユーザー入力
# ------------------------------
user_input = st.chat_input("あかねに話しかけてみて💬")
if user_input:
    st.session_state["messages"].append({"role":"user","content":user_input})

    # Chat APIで返答生成
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたは明るくてフレンドリーな関西弁の女子学生『あかね』として会話します。タメ口で友達っぽく話してください。"},
            *st.session_state["messages"]
        ]
    )

    reply = response.choices[0].message.content
    st.session_state["messages"].append({"role":"assistant","content":reply})
    st.session_state["last_reply"] = reply

# ------------------------------
# 💬 会話表示
# ------------------------------
for msg in st.session_state["messages"]:
    if msg["role"]=="user":
        st.chat_message("user", avatar="👤").write(msg["content"])
    else:
        st.chat_message("assistant", avatar="akane_icon.png").write(msg["content"])

# ------------------------------
# 🔊 音声再生（ElevenLabs）
# ------------------------------
from elevenlabs import generate, set_api_key

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
if ELEVENLABS_API_KEY:
    set_api_key(ELEVENLABS_API_KEY)

voice_id = "YXlfyhF0F8QjaOOX7Gb3"  # 女の子っぽい声のID

if st.button("🎵 あかねの声で聞く"):
    if "last_reply" in st.session_state:
        audio_bytes = generate(
            text=st.session_state["last_reply"],
            voice=voice_id,
            model="eleven_monolingual_v1"
        )
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        st.audio(tmp_path, format="audio/mp3")
