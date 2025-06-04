import json
import streamlit as st


class AudioOutput:
    """Utility for speaking text via the browser using Web Speech API."""

    @staticmethod
    def speak(text: str, lang: str = "ja-JP") -> None:
        """Speak the given text using the browser's speech synthesis."""
        if not text:
            return
        escaped = json.dumps(text)
        st.components.v1.html(
            f"""
            <script>
            var utt = new SpeechSynthesisUtterance({escaped});
            utt.lang = '{lang}';
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(utt);
            </script>
            """,
            height=0,
        )

