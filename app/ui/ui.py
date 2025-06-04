import os
import json
import shutil
import zipfile
import logging
import streamlit as st
import requests

logger = logging.getLogger(__name__)
from audiorecorder import audiorecorder
from vosk import Model, KaldiRecognizer

API_URL = "http://api:8000/api/v1/user-message"
VOSK_MODEL_PATH = os.getenv("VOSK_MODEL_PATH", "model")
MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-ja-0.22.zip"


@st.cache_resource(show_spinner=False)
def load_vosk_model() -> Model:
    """Load Vosk model once and reuse it across reruns."""
    if not ensure_vosk_model():
        raise RuntimeError("Failed to prepare Vosk model")
    return Model(VOSK_MODEL_PATH)


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


def recognize_voice() -> str:
    """Record audio in the browser and transcribe it using Vosk."""
    try:
        audio = audiorecorder("録音開始", "録音終了")
    except FileNotFoundError as e:
        st.error("ffmpeg が見つかりません。Docker イメージを再ビルドしてください")
        return ""
    except Exception as e:
        st.error(f"録音エラー: {e}")
        return ""
    if len(audio) == 0:
        return ""
    if not ensure_vosk_model():
        return ""

    audio = (
        audio.set_channels(1)
        .set_frame_rate(16000)
        .set_sample_width(2)
    )
    with st.spinner("音声認識中..."):
        model = load_vosk_model()
        recognizer = KaldiRecognizer(model, 16000)
        recognizer.AcceptWaveform(audio.raw_data)
        result = json.loads(recognizer.FinalResult())
    text = result.get("text", "")
    logger.info(f"Recognized voice text: {text}")
    return text

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

def _rerun():
    """Rerun Streamlit script with backward compatibility."""
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.rerun()

def main():
    st.set_page_config(page_title="AI チャットアプリ", page_icon="🤖")
    if "history" not in st.session_state:
        st.session_state.history = []
    if "voice_processed" not in st.session_state:
        st.session_state.voice_processed = False

    # 音声入力があればテキストとしてセットして送信
    text = recognize_voice()
    if text and not st.session_state.voice_processed:
        st.session_state.voice_processed = True
        st.session_state["input"] = text
        submit()
        _rerun()
    elif not text:
        st.session_state.voice_processed = False

    # テキスト入力ウィジェット：ここでは state["input"] が自動的に使われる
    st.text_input("メッセージを入力してください:", key="input")

    st.button("送信", on_click=submit)

    # 履歴表示
    for chat in st.session_state.history:
        st.markdown(f"**あなた:** {chat['user']}")
        st.markdown(f"**AI:** {chat['ai']}")

if __name__ == "__main__":
    main()
