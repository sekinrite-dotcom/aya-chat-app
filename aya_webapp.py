import streamlit as st
from elevenlabs import generate, set_api_key, stream
import tempfile

# ------------------------------
# 🔒 パスワード認証
# ------------------------------
st.set_page_config(page_title="🎀 アヤとおしゃべり", page_icon="🎀", layout="centered")
PASSWORD = "aya_love"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password_input = st.text_input("パスワードを入力してね💬", type="password")
    if st.button("ログイン"):
        if password_input == PASSWORD:
            st.session_state.authenticated = True
            st.success("ようこそっ！アヤやで〜💖")
            st.rerun()
        else:
            st.error("ちがうで〜😢 もう一回やってみて！")
    st.stop()

# ------------------------------
# 💖 背景＆文字デザイン
# ------------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(180deg,#ffe6f2 0%,#fff0f6 100%); }
.stChatMessage { border-radius: 20px !important; padding: 10px;
    background-color: #fff0f5 !important; color: #000000 !important; }
.stMarkdown, .stText { color: #000000 !important; }
</style>
""", unsafe_allow_html=True)

st.title("🎀 アヤとおしゃべりしよ！")

# ------------------------------
# 💫 ElevenLabs API Key 設定
# ------------------------------
ELEVENLABS_API_KEY = "sk_51f7f0a7767cdbf62730a70f4ea541293f43e8895ad116a8"
set_api_key(ELEVENLABS_API_KEY)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ------------------------------
# 💬 ユーザー入力
# ------------------------------
user_input = st.chat_input("アヤに話しかけてみて💬")
if user_input:
    st.session_state["messages"].append({"role":"user","content":user_input})
    
    # ここではデモとして文字反転で返答
    reply = f"アヤ: {user_input[::-1]} って感じかな〜💖"
    st.session_state["messages"].append({"role":"assistant","content":reply})
    st.session_state["last_reply"] = reply

# ------------------------------
# 💬 会話表示
# ------------------------------
for msg in st.session_state["messages"]:
    if msg["role"]=="user":
        st.chat_message("user", avatar="👤").write(msg["content"])
    else:
        st.chat_message("assistant", avatar="aya_icon.png").write(msg["content"])

# ------------------------------
# 🔊 ElevenLabs TTS 再生
# ------------------------------
if st.button("🎵 アヤの声を聞く"):
    if "last_reply" in st.session_state:
        audio_bytes = generate(
            text=st.session_state["last_reply"],
            voice="alloy_female",  # ← ElevenLabsの女の子声に変更可能
            model="eleven_monolingual_v1"
        )
        # 一時ファイルに保存して再生
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        st.audio(tmp_path, format="audio/mp3")
