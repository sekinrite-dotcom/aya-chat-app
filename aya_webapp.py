import streamlit as st
from openai import OpenAI
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
# 💖 背景＆文字＆吹き出しデザイン
# ------------------------------
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #ffe6f2 0%, #fff0f6 100%);
    }
    [data-testid="stHeader"] { background: rgba(255, 255, 255, 0); }
    .stChatMessage { border-radius: 20px !important; padding: 10px;
        background-color: #fff0f5 !important; color: #000000 !important; }
    .stMarkdown, .stText { color: #000000 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎀 アヤとおしゃべりしよ！")

# ------------------------------
# 💫 OpenAI設定
# ------------------------------
client = OpenAI()

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "明るくてフレンドリーな関西弁の女子学生『アヤ』として会話してください。"}
    ]

# ------------------------------
# 💬 ユーザー入力
# ------------------------------
user_input = st.chat_input("アヤに話しかけてみて💬")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # AIのテキスト返答
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state["messages"]
    )
    reply = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": reply})

    st.session_state["last_reply"] = reply  # 最新の返答を保存

# ------------------------------
# 💬 会話表示
# ------------------------------
for msg in st.session_state["messages"][1:]:
    if msg["role"] == "user":
        st.chat_message("user", avatar="👤").write(msg["content"])
    else:
        st.chat_message("assistant", avatar="aya_icon.png").write(msg["content"])

# ------------------------------
# 🔊 音声再生ボタン
# ------------------------------
if st.button("🎵 アヤの声を聞く"):
    if "last_reply" in st.session_state:
        # TTS生成
        speech = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=st.session_state["last_reply"]
        )
        audio_bytes = speech.read()

        # 一時ファイルに保存して再生
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        st.audio(tmp_path, format="audio/mp3")
