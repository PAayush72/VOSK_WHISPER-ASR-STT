# VOSK + WHISPER: Hybrid Speech-to-Text System

A high-performance speech-to-text (STT) solution combining **VOSK** (offline speech recognition) and **OpenAI's Whisper** for multilingual, real-time audio transcription with GPU acceleration.

## 🎯 Overview

This project provides a hybrid approach to speech recognition that leverages:
- **VOSK**: Fast, offline speech recognition framework for Indian languages
- **Whisper (faster-whisper)**: Advanced AI-powered transcription with superior accuracy
- **GPU Acceleration**: CUDA support for high-speed processing
- **Multi-language Support**: English (Indian), Hindi, Gujarati
- **Real-time Web Interface**: Live transcription via HTML/WebSocket

## ✨ Features

- ✅ **Hybrid Recognition**: Combine VOSK and Whisper for optimal speed/accuracy tradeoff
- ✅ **Multi-language Support**: Hindi, Gujarati, English (Indian variant)
- ✅ **GPU Acceleration**: CUDA support for fast transcription (Whisper Turbo model)
- ✅ **Real-time Processing**: WebSocket-based live transcription
- ✅ **Offline Capability**: VOSK models work without internet
- ✅ **Web UI**: Modern web interface for easy usage
- ✅ **Audio Debugging**: Debug recordings stored for analysis
- ✅ **Silence Detection**: Automatic silence threshold handling
- ✅ **Name Bias**: Custom entity recognition via NAME_BIAS configuration

## 📁 Project Structure

```
.
├── final_stt.py              # Main hybrid STT engine with WebSocket
├── hybrid_live_asr.py        # Hybrid ASR implementation
├── IndicWhisper.py           # Whisper-only for Indic languages
├── voskrecog.py              # VOSK recognition implementation
├── whisper.py                # Whisper model handling
├── index.html                # Web UI for live transcription
├── gpt.js                     # GPT integration JavaScript
├── test.js                    # JavaScript test utilities
├── test.py                    # Python test suite
├── last.py                    # Last working version backup
├── debug_recordings/          # Debug audio files
├── Vosk/                      # VOSK models directory
│   ├── vosk-model-en-in-0.5/             # English (India)
│   ├── vosk-model-hi-0.22/               # Hindi
│   ├── vosk-model-gu-0.42/               # Gujarati
│   └── vosk-model-small-en-in-0.4/       # Small English (India)
└── whisper.cpp/              # Whisper C++ implementation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- CUDA 11.0+ (for GPU acceleration, optional but recommended)
- FFmpeg (for Whisper audio processing)
- ~5GB storage for models

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/vosk-whisper.git
   cd vosk-whisper
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download Models** (Already included in Vosk/ directory)

## 📦 Installation Details

### Core Dependencies

```
pyaudio>=0.2.13            # Audio input/output
vosk>=0.3.47              # Speech recognition framework
faster-whisper>=0.7.0     # Optimized Whisper implementation
torch>=2.0.0              # Deep learning (GPU support)
sounddevice>=0.4.5        # Alternative audio capture
numpy>=1.21.0             # Numerical computing
websockets>=11.0          # Real-time WebSocket communication
```

### Optional Dependencies

- **CUDA**: nvidia-cuda-toolkit for GPU acceleration
- **FFmpeg**: For audio format conversion
- **TorchVision**: For advanced audio processing

## 💻 Usage

### 1. Final STT (Recommended) - Main Application with WebSocket
```bash
python final_stt.py
```
Features:
- Hybrid VOSK + Whisper processing
- WebSocket server on port 8765
- Real-time transcription
- Silence detection and buffering
- Debug audio recording
- Custom name bias

**Configuration** (edit `final_stt.py`):
```python
VOSK_MODEL_PATH = "./Vosk/vosk-model-en-in-0.5"  # Model selection
WHISPER_MODEL_SIZE = "turbo"                      # Model size: tiny/base/small/medium/large/turbo
DEVICE = "cuda"                                   # GPU acceleration
RATE = 16000                                      # Sample rate
SILENCE_THRESHOLD = 0.6                           # Silence detection
MAX_BUFFER_SECONDS = 6                            # Max buffer duration
NAME_BIAS = "Ujjval,ChatGPT,India,..."          # Custom entities
```

### 2. VOSK-Only Recognition
```bash
python voskrecog.py
```
- Fast, offline speech recognition
- No GPU required
- Supports: English (India), Hindi, Gujarati

### 3. Indic Whisper (Better accuracy for Indian languages)
```bash
python IndicWhisper.py
```
- Whisper-optimized for Indic script languages
- Requires GPU for optimal performance
- Higher accuracy for Hindi/Gujarati

### 4. Hybrid Live ASR
```bash
python hybrid_live_asr.py
```
- Balanced VOSK + Whisper combination
- Real-time processing

### 5. Web UI
Open `index.html` in a browser:
```bash
# Simple HTTP server
python -m http.server 8000

# Or use your preferred web server
```
Then visit: `http://localhost:8000`

## 🔧 Configuration

### Model Selection

**VOSK Models** (in `./Vosk/`):
- `vosk-model-en-in-0.5` - English (India) - Recommended
- `vosk-model-small-en-in-0.4` - Lightweight English (India)
- `vosk-model-hi-0.22` - Hindi
- `vosk-model-gu-0.42` - Gujarati

**Whisper Models**:
- `tiny` - Fastest, lowest accuracy
- `base` - Good balance
- `small` - Better accuracy
- `medium` - Much better accuracy
- `large` - Best accuracy
- `turbo` - Latest, fastest large model (Recommended with GPU)

### GPU Configuration

Enable CUDA acceleration:
```python
DEVICE = "cuda"
COMPUTE_TYPE = "float16"  # Lower memory usage, faster
# or
COMPUTE_TYPE = "float32"  # Higher accuracy
```

### Audio Settings

```python
RATE = 16000              # Sample rate (Hz)
CHANNELS = 1              # Mono audio
CHUNK = 1600              # Chunk size
SILENCE_THRESHOLD = 0.6   # Silence detection (0-1)
MAX_BUFFER_SECONDS = 6    # Max accumulated audio
MIN_SENTENCE_LENGTH = 2   # Min words per sentence
```

## 📊 Performance Benchmarks

| Model | Speed | Accuracy | GPU Memory | CPU Only |
|-------|-------|----------|-----------|----------|
| VOSK | ⚡⚡⚡ | Medium | N/A | ✅ Yes |
| Whisper Tiny | ⚡⚡ | Low | <1GB | ✅ Yes |
| Whisper Base | ⚡ | Medium | 2GB | ✅ Yes |
| Whisper Medium | ⚡ | High | 4GB | ❌ Slow |
| Whisper Turbo | ⚡⚡ | Very High | 5GB | ❌ Very Slow |

## 🎤 Audio Input

The system supports multiple audio input methods:

1. **PyAudio** (Default)
   - Cross-platform compatibility
   - Device selection available

2. **SoundDevice**
   - Alternative high-performance option
   - Used in IndicWhisper.py

3. **Line-in/Microphone**
   - Real-time streaming
   - Automatic level adjustment

## 🌐 WebSocket API

### Connection
```javascript
const ws = new WebSocket('ws://localhost:8765');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Transcription:', data.text);
};
```

### Message Format
```json
{
  "text": "Transcribed text here",
  "confidence": 0.95,
  "language": "en-IN",
  "source": "whisper"
}
```

## 🐛 Debugging

### Debug Audio Recording
All recordings are saved to `debug_recordings/` with timestamps:
```
debug_recordings/
├── 2024-03-05_14-30-45.wav
├── 2024-03-05_14-31-12.wav
└── ...
```

### Check Logs
Monitor transcription quality and processing time in console output.

### VOSK Model Issues
If VOSK fails:
1. Check model path exists
2. Verify model files integrity
3. Try different model size

### GPU Memory Issues
If CUDA out of memory:
1. Reduce WHISPER_MODEL_SIZE
2. Change COMPUTE_TYPE to "int8"
3. Reduce MAX_BUFFER_SECONDS
4. Use VOSK only mode

## 🤝 Integration Examples

### Python Integration
```python
from vosk import Model, KaldiRecognizer
from faster_whisper import WhisperModel

# Quick VOSK transcription
model = Model("./Vosk/vosk-model-en-in-0.5")
recognizer = KaldiRecognizer(model, 16000)

# Quick Whisper transcription
whisper = WhisperModel("turbo", device="cuda", compute_type="float16")
result = whisper.transcribe("audio.wav", language="en")
```

### JavaScript Integration
```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8765');

ws.onmessage = (event) => {
  const result = JSON.parse(event.data);
  document.getElementById('output').innerText = result.text;
};
```

## 📋 Requirements File

Create `requirements.txt`:
```
pyaudio>=0.2.13
vosk>=0.3.47
faster-whisper>=0.7.0
torch>=2.0.0
numpy>=1.21.0
sounddevice>=0.4.5
websockets>=11.0
```

Install with:
```bash
pip install -r requirements.txt
```

## 🔗 Dependencies & Libraries

| Library | Purpose | Version |
|---------|---------|---------|
| vosk | Offline speech recognition | 0.3.47+ |
| faster-whisper | GPU-optimized Whisper | 0.7.0+ |
| torch | Deep learning framework | 2.0.0+ |
| pyaudio | Audio input/output | 0.2.13+ |
| numpy | Numerical computing | 1.21.0+ |
| websockets | Real-time communication | 11.0+ |
| sounddevice | Audio capture alternative | 0.4.5+ |

## 📝 File Descriptions

| File | Purpose | Status |
|------|---------|--------|
| `final_stt.py` | Main hybrid STT engine with WebSocket | ✅ Active |
| `hybrid_live_asr.py` | Hybrid ASR combining VOSK+Whisper | ⚠️ Alternative |
| `IndicWhisper.py` | Whisper-only for Indian languages | ✅ Active |
| `voskrecog.py` | VOSK recognition (Gujarati) | ✅ Active |
| `whisper.py` | Whisper-only implementation | ✅ Active |
| `last.py` | Previous working version | 📦 Backup |
| `index.html` | Web UI interface | ✅ Active |
| `gpt.js` | GPT integration utilities | 📦 Utility |
| `test.js` | JavaScript tests | 🧪 Test |
| `test.py` | Python tests | 🧪 Test |

## 🌍 Language Support

| Language | Model | Status |
|----------|-------|--------|
| English (India) | en-IN | ✅ Full |
| Hindi | hi-IN | ✅ Full |
| Gujarati | gu-IN | ✅ Full |
| English (Other) | en | ✅ Full |
| Others | - | 📦 Can be added |

## 🎯 Use Cases

1. **Real-time Transcription**: Live meetings, lectures, podcasts
2. **Accessibility**: Speech-to-text for accessibility features
3. **Multi-language Support**: Indian market applications
4. **Offline Processing**: Privacy-focused transcription
5. **Voice Search**: Voice querying systems
6. **Meeting Notes**: Automatic note-taking

## ⚙️ System Requirements

### Minimum
- CPU: 4 cores
- RAM: 8GB
- Storage: 2GB free
- No GPU required (slow)

### Recommended
- CPU: 8+ cores
- RAM: 16GB+
- Storage: 10GB free
- GPU: NVIDIA with CUDA 11.0+
- VRAM: 6GB+ for Turbo model

### Optimal
- RTX 3080/4080+
- 32GB+ RAM
- SSD storage
- Linux OS (Windows/Mac supported)

## 🔐 Security & Privacy

- ✅ VOSK runs completely offline
- ✅ Whisper processes locally on GPU
- ✅ No data sent to external APIs
- ✅ Audio files only stored in debug mode
- ✅ Clear debug recordings regularly

## 🐛 Troubleshooting

### "VOSK Model not found"
```bash
# Ensure model exists in correct directory
ls Vosk/vosk-model-en-in-0.5/
```

### "CUDA out of memory"
Reduce model size or use CPU mode:
```python
DEVICE = "cpu"
WHISPER_MODEL_SIZE = "base"
```

### "PyAudio installation fails"
Install system audio libraries:
- **Ubuntu**: `sudo apt-get install portaudio19-dev`
- **macOS**: `brew install portaudio`
- **Windows**: Use precompiled wheels

### "WebSocket connection refused"
Ensure `final_stt.py` is running and port 8765 is not blocked.

### Poor transcription accuracy
1. Try larger Whisper model
2. Improve audio quality (mic placement)
3. Reduce background noise
4. Add relevant words to NAME_BIAS

## 📚 References

- [VOSK Documentation](https://alphacephei.com/vosk/)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Faster Whisper](https://github.com/guillaumekln/faster-whisper)
- [PyAudio Documentation](http://people.csail.mit.edu/hubert/pyaudio/)

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- [ ] Additional language models
- [ ] Frontend UI improvements
- [ ] Performance optimization
- [ ] Docker containerization
- [ ] API documentation
- [ ] Unit tests

## 📄 License

[Add your license here - MIT, Apache 2.0, etc.]

## 👤 Author

**Aayush** - Created and maintained this hybrid STT system

## 🙏 Acknowledgments

- VOSK team for offline speech recognition
- OpenAI for Whisper model
- Guillaume Klein for faster-whisper optimization

## 📞 Support

For issues, questions, or suggestions, please:
1. Check existing issues/discussions
2. Create a detailed bug report
3. Include system info: OS, Python version, GPU info
4. Attach relevant debug recordings

---

**Last Updated**: March 2024  
**Version**: 1.0.0  
**Status**: Active & Maintained ✅
