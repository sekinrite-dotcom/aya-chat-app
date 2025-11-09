import streamlit as st
import os
import openai

# ------------------------------
# 🔹 OpenAI API Key を Secrets から取得
# ------------------------------
openai.api_key = st.secrets.get("OPENAI_API_KEY")
if not openai.api_key:
    st.error("OpenAI APIキーが設定されていません。Secrets を確認してね。")
    st.stop()

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
# 💬 会話管理
# ------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.chat_input("アヤに話しかけてみて💬")
if user_input:
    st.session_state["messages"].append({"role":"user","content":user_input})
    
    # 🔹 最新 API に対応した OpenAI 呼び出し
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたは明るくてフレンドリーな関西弁の女子学生『アヤ』として会話します。"},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state["messages"]]
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = "ごめん💦 今アヤはちょっとお休み中やね…"

    st.session_state["messages"].append({"role":"assistant","content":reply})
    st.session_state["last_reply"] = reply

# 会話表示
for msg in st.session_state["messages"]:
    if msg["role"]=="user":
        st.chat_message("user", avatar="👤").write(msg["content"])
    else:
        st.chat_message("assistant", avatar="aya_icon.png").write(msg["content"])
