import streamlit as st
from openai import OpenAI
import base64
import io

# ------------------------------
# 🔒 パスワード認証
# ------------------------------
st.set_page_config(page_title="🎀 アヤとおしゃべり", page_icon="🎀", layout="centered")

PASSWORD = "yuto4325"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown(
        "<h2 style='text-align:center; color:#ff7eb9;'>🎀 アヤの秘密の部屋 🎀</h2>",
        unsafe_allow_html=True
    )
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
# 💖 メイン画面
# ------------------------------
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #ffe6f2 0%, #fff0f6 100%);
    }
    [data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0);
    }
    .stChatMessage {
        border-radius: 20px !important;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎀 アヤとおしゃべりしよ！")

# APIクライアント
client = OpenAI()

# 会話履歴の初期化
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": "あなたは明るくてフレンドリーな関西弁の女子学生『アヤ』として会話します。"
        }
    ]

# チャット入力欄
user_input = st.chat_input("アヤに話しかけてみてな💬")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # テキスト返信
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state["messages"]
    )
    reply = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": reply})

    # 音声生成
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=reply
    )

    audio_bytes = speech.read()
    st.audio(io.BytesIO(audio_bytes), format="audio/mp3")

# 会話表示
for msg in st.session_state["messages"][1:]:
    if msg["role"] == "user":
        st.chat_message("user", avatar="👤").write(msg["content"])
    else:
        st.chat_message("assistant", avatar="aya_icon.png").write(msg["content"])
