import logging
import requests
import streamlit as st

from voice_input import VoiceInput
from audio_output import AudioOutput

logger = logging.getLogger(__name__)

API_URL = "http://api:8000/api/v1/user-message"


class ChatUI:
    """Main chat UI handling text and voice input."""

    def __init__(self):
        self.voice = VoiceInput()
        self.audio_output = AudioOutput()

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
            st.session_state.speak_text = ai
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

        # If we have audio from the previous run, transcribe it before any
        # widgets are created so we can safely set session state.
        if "last_audio" in st.session_state:
            text = self.voice.transcribe(st.session_state.pop("last_audio"))
            if text and not st.session_state.voice_processed:
                st.session_state.voice_processed = True
                st.session_state["input"] = text
                self.submit()
                self._rerun()
            elif not text:
                st.session_state.voice_processed = False

        st.markdown(
            """
            <style>
            #chat-area {
                max-height: calc(100vh - 140px);
                overflow-y: auto;
                padding-bottom: 120px;
            }
            #input-area {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                width: 100%;
                background: white;
                padding: 10px 5px;
                box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
                display: flex;
                gap: 8px;
                align-items: center;
                z-index: 1000;
            }
            @keyframes voice-blink {
                0%, 100% {background-color: #fdd;}
                50% {background-color: #fee;}
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        with st.container():
            st.markdown('<div id="chat-area">', unsafe_allow_html=True)
            for chat in st.session_state.history:
                st.markdown(f"**あなた:** {chat['user']}")
                st.markdown(f"**AI:** {chat['ai']}")
            st.markdown('</div>', unsafe_allow_html=True)
            if 'speak_text' in st.session_state:
                self.audio_output.speak(st.session_state.pop('speak_text'))

        input_container = st.container()
        with input_container:
            input_container.markdown('<div id="input-area">', unsafe_allow_html=True)
            st.text_input(
                "メッセージを入力してください:",
                key="input",
                label_visibility="collapsed",
                placeholder="メッセージを入力してください",
            )
            col_send, col_voice = st.columns([1, 1])
            with col_send:
                st.button("送信", key="send_button", on_click=self.submit)
            with col_voice:
                audio = self.voice.record_audio()
                if len(audio) > 0:
                    st.session_state.last_audio = audio
                    # allow the new audio to be processed on the next run
                    st.session_state.voice_processed = False
                    # immediately rerun so transcription can happen
                    self._rerun()
            input_container.markdown('</div>', unsafe_allow_html=True)

        st.markdown(
            """
            <script>
            const sendBtn = window.parent.document.querySelector('button[id="send_button"]');
            const observer = new MutationObserver(() => {
                const stopBtn = Array.from(window.parent.document.querySelectorAll('button')).find(b => b.innerText.includes('録音中'));
                if (stopBtn) {
                    if (sendBtn) sendBtn.disabled = true;
                    stopBtn.style.animation = 'voice-blink 2s ease-in-out infinite';
                } else {
                    if (sendBtn) sendBtn.disabled = false;
                }
            });
            observer.observe(window.parent.document.body, {subtree: true, childList: true});
            </script>
            """,
            unsafe_allow_html=True,
        )


def main():
    ChatUI().run()


if __name__ == "__main__":
    main()
