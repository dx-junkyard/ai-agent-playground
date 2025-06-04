import os
import queue
import json
import shutil
import zipfile
import streamlit as st
import requests
import sounddevice as sd
from vosk import Model, KaldiRecognizer

API_URL = "http://api:8000/api/v1/user-message"
VOSK_MODEL_PATH = os.getenv("VOSK_MODEL_PATH", "model")
MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-ja-0.22.zip"


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


def recognize_voice(duration: int = 5) -> str:
    """Record audio from microphone and transcribe it using Vosk."""
    if not ensure_vosk_model():
        return ""

    model = Model(VOSK_MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)
    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            st.warning(str(status))
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                           channels=1, callback=callback):
        for _ in range(int(duration * 16000 / 8000)):
            data = q.get()
            recognizer.AcceptWaveform(data)
    result = json.loads(recognizer.FinalResult())
    return result.get("text", "")

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

    col1, col2 = st.columns(2)
    with col1:
        st.button("送信", on_click=submit)
    with col2:
        if st.button("音声入力"):
            with st.spinner("録音中..."):
                text = recognize_voice()
            if text:
                st.session_state["input"] = text
                submit()

    # 履歴表示
    for chat in st.session_state.history:
        st.markdown(f"**あなた:** {chat['user']}")
        st.markdown(f"**AI:** {chat['ai']}")

if __name__ == "__main__":
    main()
