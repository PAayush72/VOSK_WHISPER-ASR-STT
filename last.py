import json
import queue
import threading
import pyaudio
import wave
import os
import sys
import time
import shutil
import _thread
from datetime import datetime
from vosk import Model, KaldiRecognizer, SetLogLevel
from faster_whisper import WhisperModel
import asyncio
import websockets

VOSK_MODEL_PATH = "./Vosk/vosk-model-hi-0.22"
WHISPER_MODEL_SIZE = "turbo"
DEVICE = "cuda"
COMPUTE_TYPE = "float16"
RATE = 16000
CHANNELS = 1
CHUNK = 1600
SILENCE_THRESHOLD = 0.6
MAX_BUFFER_SECONDS = 6
MIN_SENTENCE_LENGTH = 2
DEBUG_AUDIO_DIR = "debug_recordings"
os.makedirs(DEBUG_AUDIO_DIR, exist_ok=True)

# ================= WEBSOCKET (ADDED) =================

WS_PORT = 8765
ws_clients = set()
ws_loop = None

async def ws_handler(websocket):
    ws_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        ws_clients.remove(websocket)

async def ws_broadcast(message: str):
    if ws_clients:
        await asyncio.gather(
            *[client.send(message) for client in ws_clients],
            return_exceptions=True
        )

async def ws_main():
    async with websockets.serve(ws_handler, "0.0.0.0", WS_PORT):
        print(f"🌐 WebSocket server running on ws://localhost:{WS_PORT}")
        await asyncio.Future()  # run forever

def start_ws_server():
    global ws_loop
    ws_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(ws_loop)
    ws_loop.run_until_complete(ws_main())

def send_ws(data: dict):
    if ws_loop and ws_loop.is_running():
        asyncio.run_coroutine_threadsafe(
            ws_broadcast(json.dumps(data)),
            ws_loop
        )


if not os.path.exists(VOSK_MODEL_PATH):
    print(f"❌ Error: Vosk model not found at {VOSK_MODEL_PATH}")
    sys.exit(1)
    
SetLogLevel(-1)
print("🔄 Loading Vosk (Live Stream)...")
vosk_model = Model(VOSK_MODEL_PATH)
recognizer = KaldiRecognizer(vosk_model, RATE)
recognizer.SetWords(True)
print("✅ Vosk Ready")

print("🔄 Loading Whisper (Background Polish)...")
whisper_model = WhisperModel(WHISPER_MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
print("✅ Whisper Ready")

audio_queue = queue.Queue()
polish_queue = queue.Queue()
session_audio = []

state_lock = threading.Lock()
committed_sentences = []
sentence_audio_buffer = []
live_partial = ""
is_processing = False

def extract_keywords(text, max_words=10):
    """
    Extracts proper nouns from Vosk to teach Whisper context.
    """
    words = text.split()
    valid = [w for w in words if len(w) > 2]
    return ", ".join(valid[:max_words])

def check_exit_command(text):
    """Checks if the user wants to quit based on the FINAL committed text."""
    triggers = ["stop listening", "end dictation", "goodbye", "terminate"]  
    return any(t in text.lower() for t in triggers)

def audio_recorder():
    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=pyaudio.paInt16, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    except OSError:
        print("❌ Mic Error")
        return

    print("\n🎤 LIVE! Speak naturally... (Ctrl+C to Stop)\n")
    
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_queue.put(data)
        session_audio.append(data)

        #================= UI REDRAW =================

def redraw():
    with state_lock:
        if is_processing:
            return

        print(f"\r\033[93m> {live_partial}\033[0m\033[K", end="", flush=True)
        send_ws({"type": "partial", "text": live_partial})

        send_ws({
            "type": "partial",
            "text": live_partial
        })



def whisper_worker():
    global is_processing
    while True:
        index, audio_bytes, rough_vosk_text = polish_queue.get()
        tmp_file = f"temp_{index}.wav"
        
        try:
            with wave.open(tmp_file, "wb") as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(2)
                wf.setframerate(RATE)
                wf.writeframes(audio_bytes)
            
            context_keywords = extract_keywords(rough_vosk_text)
            
            custom_prompt = (
                f"Context: {context_keywords}. "
                "Spoken dictation. Preserve questions and sentence boundaries."
            )
            
            segments, _ = whisper_model.transcribe(
                tmp_file,
                beam_size=1,
                best_of=1,
                temperature=0.0,
                initial_prompt=custom_prompt,
                vad_filter=False,
                condition_on_previous_text=False
            )
            polished_text = " ".join(s.text.strip() for s in segments)
            
            polished_text = polished_text.replace(" true.", "").replace(" True.", "")
            
            if polished_text:
                with state_lock:
                    if index < len(committed_sentences):
                        committed_sentences[index] = polished_text
                
                print(f"\r\033[K", end="") 
                print(f"✅ {polished_text}")
                send_ws({
                    "type": "final",
                    "text": polished_text
                })

                

                if check_exit_command(polished_text):
                    print("\n🛑 Voice Command: Stopping...")
                    _thread.interrupt_main()
            
            with state_lock:
                is_processing = False
            redraw()
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if os.path.exists(tmp_file):
                os.remove(tmp_file)
            polish_queue.task_done()

    

def main_loop():
    global live_partial, is_processing
    
    threading.Thread(target=audio_recorder, daemon=True).start()
    threading.Thread(target=whisper_worker, daemon=True).start()
    
    last_speech_time = time.time()
    
    while True:
        data = audio_queue.get()
        
        if not is_processing:
            sentence_audio_buffer.append(data)
        
        if recognizer.AcceptWaveform(data):
            last_speech_time = time.time()
        else:
            partial_res = json.loads(recognizer.PartialResult())
            partial_text = partial_res.get("partial", "")
            
            silence_duration = time.time() - last_speech_time
            if partial_text and silence_duration < SILENCE_THRESHOLD:
                last_speech_time = time.time()
                with state_lock:
                    live_partial = partial_text
                redraw()

        silence_duration = time.time() - last_speech_time
        buffer_duration = (len(sentence_audio_buffer) * CHUNK) / RATE
        
        should_commit = False
        
        if silence_duration > SILENCE_THRESHOLD and live_partial.strip():
            should_commit = True
            
        elif buffer_duration > MAX_BUFFER_SECONDS:
            should_commit = True
        
        if should_commit:
            result = json.loads(recognizer.FinalResult())
            text = result.get("text", "").strip()
            recognizer.Reset()

            if text and len(text.split()) >= MIN_SENTENCE_LENGTH:
                with state_lock:
                    committed_sentences.append(text)
                    live_partial = ""
                    idx = len(committed_sentences) - 1
                    is_processing = True 
                
                print(f"\r\033[K", end="")
                
                audio_bytes = b"".join(sentence_audio_buffer)
                
                polish_queue.put((idx, audio_bytes, text))
                
                sentence_audio_buffer.clear()
                last_speech_time = time.time()
                
            elif text:
                sentence_audio_buffer.clear()
                with state_lock:
                    live_partial = ""
                redraw()

if __name__ == "__main__":
    try:
        threading.Thread(target=start_ws_server, daemon=True).start()
        main_loop()
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping...")
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = f"{DEBUG_AUDIO_DIR}/session_{ts}.wav"
        with wave.open(path, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)
            wf.setframerate(RATE)
            wf.writeframes(b"".join(session_audio))
        print(f"💾 Full session saved: {path}")


