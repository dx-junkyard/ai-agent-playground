import logging
import requests
import streamlit as st

from voice import Voice

logger = logging.getLogger(__name__)

API_URL = "http://api:8000/api/v1/user-message"


class ChatUI:
    """Main chat UI handling text and voice input."""

    def __init__(self):
        self.voice = Voice()

    @staticmethod
    def send_message(msg: str) -> str:
        try:
            resp = requests.post(API_URL, json={"message": msg})
            resp.raise_for_status()
            return resp.text.strip()
        except Exception as e:
            st.error(f"送信エラー: {e}")
            return ""

    def submit(self):
        msg = st.session_state["input"]
        if msg:
            ai = self.send_message(msg)
            st.session_state.history.append({"user": msg, "ai": ai})
        else:
            st.warning("メッセージを入力してください。")
        st.session_state["input"] = ""

    def _rerun(self):
        """Rerun Streamlit script with backward compatibility."""
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            st.rerun()

    def run(self):
        st.set_page_config(page_title="AI チャットアプリ", page_icon="🤖")
        if "history" not in st.session_state:
            st.session_state.history = []
        if "voice_processed" not in st.session_state:
            st.session_state.voice_processed = False

        text = self.voice.recognize_voice()
        if text and not st.session_state.voice_processed:
            st.session_state.voice_processed = True
            st.session_state["input"] = text
            self.submit()
            self._rerun()
        elif not text:
            st.session_state.voice_processed = False

        st.text_input("メッセージを入力してください:", key="input")
        st.button("送信", on_click=self.submit)

        for chat in st.session_state.history:
            st.markdown(f"**あなた:** {chat['user']}")
            st.markdown(f"**AI:** {chat['ai']}")


def main():
    ChatUI().run()


if __name__ == "__main__":
    main()
