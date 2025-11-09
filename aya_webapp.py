import streamlit as st
from openai import OpenAI
import io
import tempfile

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
# 💖 背景＆文字＆吹き出しデザイン（文字黒固定）
# ------------------------------
st.markdown(
    """
    <style>
    /* 背景ピンク */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #ffe6f2 0%, #fff0f6 100%);
    }

    [data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0);
    }

    /* 吹き出しデザイン */
    .stChatMessage {
        border-radius: 20px !important;
        padding: 10px;
        background-color: #fff0f5 !important;
        color: #000000 !important;  /* ← 文字を黒 */
    }

    /* markdownやテキストも黒 */
    .stMarkdown, .stText {
        color: #000000 !important;
    }
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
        {"role": "system", "content": "あなたは明るくてフレンドリーな関西弁の女子学生『アヤ』として会話します。"}
    ]

# ------------------------------
# 💬 ユーザー入力
# ------------------------------
user_input = st.chat_input("アヤに話しかけてみてな💬")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # テキスト返答
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state["messages"]
    )
    reply = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": reply})

    # ------------------------------
    # 🔊 音声生成（スマホ対応：一時ファイルに保存）
    # ------------------------------
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=reply
    )
    audio_bytes = speech.read()

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    # スマホでも確実に再生できる
    st.audio(tmp_path, format="audio/mp3")

# ------------------------------
# 💬 会話表示
# ------------------------------
for msg in st.session_state["messages"][1:]:
    if msg["role"] == "user":
        st.chat_message("user", avatar="👤").write(msg["content"])
    else:
        st.chat_message("assistant", avatar="aya_icon.png").write(msg["content"])

