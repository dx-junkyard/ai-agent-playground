import os
import requests
import streamlit as st


class AudioOutput:
    """Generate speech using VOICEVOX (VoiceBox) engine and play it."""

    def __init__(self, base_url: str = None, speaker: int = 1) -> None:
        self.base_url = base_url or os.environ.get("VOICEBOX_URL", "http://voicebox:50021")
        self.speaker = speaker

    def _synthesize(self, text: str) -> bytes:
        """Request VOICEVOX to synthesize speech and return WAV bytes."""
        query = requests.post(
            f"{self.base_url}/audio_query",
            params={"speaker": self.speaker, "text": text},
        )
        query.raise_for_status()
        synthesis = requests.post(
            f"{self.base_url}/synthesis",
            params={"speaker": self.speaker},
            json=query.json(),
        )
        synthesis.raise_for_status()
        return synthesis.content

    def speak(self, text: str) -> None:
        if not text:
            return
        try:
            audio = self._synthesize(text)
            st.audio(audio, format="audio/wav", autoplay=True)
        except Exception as e:
            st.error(f"音声生成失敗: {e}")
