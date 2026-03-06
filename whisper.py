# import sounddevice as sd
# import numpy as np
# import queue
# import threading
# from faster_whisper import WhisperModel

# samplerate = 16000
# block_duration = 0.5
# chunk_duration = 2
# channels = 1

# frames_per_block = int(samplerate * block_duration)
# frames_per_chunk = int(samplerate * chunk_duration)

# audio_queue = queue.Queue()
# audio_buffer = []

# model = WhisperModel("turbo",device="cuda",compute_type="float16")

# def audio_callback(indata, frames, time, status):
#     if status:
#         print(status)
#     audio_queue.put(indata.copy())

   
# def recorder():
#     with sd.InputStream(samplerate=samplerate, channels=channels,
#                         callback=audio_callback, blocksize=frames_per_block):
#         print("Listnig in process ...")
#         while True:
#             sd.sleep(100)


# def transcriber():
#     global audio_buffer
#     while True:
#         block = audio_queue.get()
#         audio_buffer.append(block)

#         total_frames = sum(len(b) for b in audio_buffer)
#         if total_frames >= frames_per_chunk:
#             audio_data = np.concatenate(audio_buffer)[:frames_per_chunk]
#             audio_buffer = []

#             audio_data = audio_data.flatten().astype(np.float16)

#             segments, _= model.transcribe(
#                 audio_data,
#                 language="en",
#                 beam_size=1
#             )

#             for segment in segments:
#                 print(f"{segment.text}")


# threading.Thread(target=recorder, daemon=True).start()
# transcriber()










import sounddevice as sd
import numpy as np
import queue
import threading
from faster_whisper import WhisperModel

samplerate = 16000
block_duration = 0.5
chunk_duration = 2.0
channels = 1

frames_per_block = int(samplerate * block_duration)
frames_per_chunk = int(samplerate * chunk_duration)

audio_queue = queue.Queue()
audio_buffer = []

model = WhisperModel(
    "turbo",
    device="cuda",
    compute_type="float16"
)

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())

def has_speech(audio, threshold=0.01):
    # Energy-based silence detection
    return np.mean(np.abs(audio)) > threshold

def recorder():
    with sd.InputStream(
        samplerate=samplerate,
        channels=channels,
        callback=audio_callback,
        blocksize=frames_per_block
    ):
        print("🎤 Listening (Turbo + VAD)...")
        while True:
            sd.sleep(100)

def transcriber():
    global audio_buffer
    while True:
        block = audio_queue.get()
        audio_buffer.append(block)

        total_frames = sum(len(b) for b in audio_buffer)
        if total_frames >= frames_per_chunk:
            audio_data = np.concatenate(audio_buffer)[:frames_per_chunk]
            audio_buffer = []

            audio_data = audio_data.flatten().astype(np.float32)

            # 🔥 SILENCE GATE
            if not has_speech(audio_data):
                continue

            segments, _ = model.transcribe(
                audio_data,
                language="en",
                beam_size=1,
                vad_filter=True,
                vad_parameters=dict(
                    min_silence_duration_ms=400,
                    speech_pad_ms=100
                ),
                temperature=0.0,
                condition_on_previous_text=False
            )

            text = " ".join(s.text.strip() for s in segments)

            # 🔥 FINAL FILTER
            if len(text.split()) >= 2:
                print(text)

threading.Thread(target=recorder, daemon=True).start()
transcriber()
