import os
import json
import shutil
import zipfile
import logging

import streamlit as st
import requests

from vosk import Model, KaldiRecognizer
from audiorecorder import audiorecorder

logger = logging.getLogger(__name__)

VOSK_MODEL_PATH = os.getenv("VOSK_MODEL_PATH", "model")
MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-ja-0.22.zip"


class VoiceInput:
    """Handle voice recording and speech recognition."""

    @staticmethod
    @st.cache_resource(show_spinner=False)
    def load_vosk_model() -> Model:
        """Load Vosk model once and reuse it across reruns."""
        if not VoiceInput.ensure_vosk_model():
            raise RuntimeError("Failed to prepare Vosk model")
        return Model(VOSK_MODEL_PATH)

    @staticmethod
    def ensure_vosk_model() -> bool:
        """Download the Japanese Vosk model if it's not available."""
        if os.path.isdir(VOSK_MODEL_PATH):
            return True
        try:
            st.info("Downloading Vosk Japanese model...")
            os.makedirs(VOSK_MODEL_PATH, exist_ok=True)
            zip_path = os.path.join(VOSK_MODEL_PATH, "model.zip")
            with requests.get(MODEL_URL, stream=True) as r:
                r.raise_for_status()
                with open(zip_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(VOSK_MODEL_PATH)
            os.remove(zip_path)

            # If the model is extracted into a directory, move contents up
            for item in os.listdir(VOSK_MODEL_PATH):
                path = os.path.join(VOSK_MODEL_PATH, item)
                if os.path.isdir(path) and item.startswith("vosk-model"):
                    for f in os.listdir(path):
                        shutil.move(os.path.join(path, f), VOSK_MODEL_PATH)
                    shutil.rmtree(path)
                    break
            return True
        except Exception as e:
            st.error(f"Vosk model download failed: {e}")
            return False

    @staticmethod
    def record_audio() -> "AudioSegment":
        """Render the audio recorder widget and return the recorded segment."""
        try:
            audio = audiorecorder(
                "🎤",
                "録音中",
                start_style={
                    "background-color": "#eee",
                    "border": "1px solid #ccc",
                    "border-radius": "50%",
                },
                stop_style={"background-color": "#fdd"},
                key="voice_recorder",
            )
        except FileNotFoundError:
            st.error("ffmpeg が見つかりません。Docker イメージを再ビルドしてください")
            from pydub import AudioSegment

            return AudioSegment.empty()
        except Exception as e:
            st.error(f"録音エラー: {e}")
            from pydub import AudioSegment

            return AudioSegment.empty()
        return audio

    @staticmethod
    def transcribe(audio) -> str:
        """Transcribe a recorded AudioSegment using Vosk."""
        if len(audio) == 0:
            return ""
        if not VoiceInput.ensure_vosk_model():
            return ""

        audio = (
            audio.set_channels(1)
            .set_frame_rate(16000)
            .set_sample_width(2)
        )
        with st.spinner("音声認識中..."):
            model = VoiceInput.load_vosk_model()
            recognizer = KaldiRecognizer(model, 16000)
            recognizer.AcceptWaveform(audio.raw_data)
            result = json.loads(recognizer.FinalResult())
        text = result.get("text", "")
        logger.info(f"Recognized voice text: {text}")
        return text

    def recognize_voice(self) -> str:
        """Record audio via widget then transcribe it."""
        audio = self.record_audio()
        return self.transcribe(audio)
