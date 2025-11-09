import streamlit as st
from openai import OpenAI
import base64

# -------------------------
# 🌸 設定
# -------------------------
st.set_page_config(page_title="アヤとおしゃべり🎤", page_icon="🎀")

# パスワード設定（任意）
PASSWORD = "yuto4325"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("### 💬 アヤに会うにはパスワードが必要やで！")
    pw = st.text_input("🔑 パスワードを入れてな", type="password")
    if st.button("ログイン"):
        if pw == PASSWORD:
            st.session_state.authenticated = True
            st.success("ようこそっ！アヤやで〜💖")
        else:
            st.error("ちゃうで、それやない💦")
    st.stop()

# -------------------------
# 💫 OpenAI設定
# -------------------------
client = OpenAI()

st.title("🎀 アヤとおしゃべり（関西弁ver）🎀")
st.markdown("明るくてフレンドリーな関西弁女子・アヤがしゃべってくれるで〜✨")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "あなたは明るくてフレンドリーな関西弁の女子学生『アヤ』として話します。"}
    ]

# -------------------------
# 💬 入力と表示
# -------------------------
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("なんでも話してな〜💞"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 🤖 GPTの返答
    with st.chat_message("assistant", avatar="https://i.imgur.com/Ef8G2oE.png"):
        with st.spinner("アヤが考え中やで...💭"):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

            st.session_state.messages.append({"role": "assistant", "content": reply})

            # 🔊 音声合成（TTS）
            audio_response = client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice="alloy",  # 声の種類：他にも"verse"や"aria"などある
                input=reply,
            )

            audio_bytes = audio_response.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            audio_html = f"""
            <audio autoplay controls>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
