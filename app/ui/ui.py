import os
import streamlit as st
import requests

API_URL = "http://api:8000/api/v1/user-message"

def send_message(msg: str) -> str:
    try:
        resp = requests.post(API_URL, json={"message": msg})
        resp.raise_for_status()
        return resp.text.strip()
    except Exception as e:
        st.error(f"送信エラー: {e}")
        return ""

def submit():
    msg = st.session_state["input"]
    if msg:
        ai = send_message(msg)
        st.session_state.history.append({"user": msg, "ai": ai})
    else:
        st.warning("メッセージを入力してください。")
    # ← ここでのみ input をクリア
    st.session_state["input"] = ""

def main():
    st.set_page_config(page_title="AI チャットアプリ", page_icon="🤖")
    if "history" not in st.session_state:
        st.session_state.history = []

    # テキスト入力ウィジェット：ここでは state["input"] が自動的に使われる
    st.text_input("メッセージを入力してください:", key="input")

    # ボタンにコールバックを登録
    st.button("送信", on_click=submit)

    # 履歴表示
    for chat in st.session_state.history:
        st.markdown(f"**あなた:** {chat['user']}")
        st.markdown(f"**AI:** {chat['ai']}")

if __name__ == "__main__":
    main()
