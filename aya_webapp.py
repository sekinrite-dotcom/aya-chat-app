import streamlit as st
from openai import OpenAI

# OpenAIのAPIキーを設定
client = OpenAI(api_key="ここに自分のAPIキーを入れてね")

st.set_page_config(page_title="アヤとおしゃべり", page_icon="🎀")
st.title("🎀 アヤとおしゃべりしよ！")

# 会話履歴を保持
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは明るくてフレンドリーな関西弁の女子学生『アヤ』として会話します。"}
    ]

# 入力欄
user_input = st.chat_input("アヤに話しかけてみよ！")

if user_input:
    # ユーザーのメッセージを保存
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # OpenAI API呼び出し
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state["messages"]
    )

    reply = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": reply})

# 会話表示
for msg in st.session_state["messages"][1:]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
