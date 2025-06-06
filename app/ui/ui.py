import os
import streamlit as st
import requests

API_URL = os.environ.get("API_URL", "http://api:8000/api/v1/user-message")

st.set_page_config(page_title="AI チャットアプリ", page_icon="🤖")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "こんにちは！チャットへようこそ。"}
    ]


def call_api(text: str) -> str:
    try:
        resp = requests.post(API_URL, json={"message": text})
        resp.raise_for_status()
        return resp.text.strip()
    except Exception as e:
        st.error(f"送信エラー: {e}")
        return "エラーが発生しました"


for m in st.session_state.messages:
    with st.chat_message("user" if m["role"] == "user" else "ai"):
        st.markdown(m["content"])

prompt = st.chat_input("メッセージを入力...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    reply = call_api(prompt)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("ai"):
        st.markdown(reply)
