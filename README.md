<div align="center">

# ✦ VESPER
### AI Desktop Assistant

![Python](https://img.shields.io/badge/Python-3.8+-00D4FF?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-7B5CFA?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-00FFB2?style=for-the-badge&logo=windows&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-00D4FF?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-2.0-7B5CFA?style=for-the-badge)

**A voice-powered AI desktop assistant with a sleek dark UI — built entirely in Python.**

*Speak a command. Vesper handles the rest.*

</div>

---

## 📌 Overview

Vesper is a personal AI desktop assistant that combines **voice recognition**, **real-time web data**, and **system automation** into one smooth, dark-themed application. No cloud subscription. No login. Just run it and talk.

Built with Python and Tkinter, Vesper runs fully on your local machine and responds to both voice commands and typed text through a modern chat-bubble interface with a live animated orb that pulses when listening.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎙️ **Voice Input** | Speak naturally — Vesper transcribes via Google Speech API |
| 💬 **Chat Interface** | Timestamped chat bubbles for every interaction |
| 🌦️ **Live Weather** | Real-time weather for any city (temp, humidity, wind) |
| 📖 **Wikipedia Search** | Instant 2-sentence summaries spoken aloud |
| 🌐 **Web Launcher** | Open YouTube, Google, Gmail, GitHub, and more |
| 🖥️ **App Automation** | Launch VS Code, Chrome, Excel, Word, PowerPoint |
| 🎵 **Music Player** | Play music from your local library |
| 🕐 **Time & Date** | Ask for the current time or today's date |
| ✨ **Animated UI** | Glowing orb pulses in real-time while listening |
| ⚡ **Non-blocking TTS** | Text-to-speech runs on a background thread — UI never freezes |

---

## 🖼️ UI Preview

```
┌─────────────────────────────────────────────────────────┐
│  ✦ VESPER          Chat with Vesper    Thu, Jan 01 12:00 │
│══════════════════════════════════════════════════════════│
│  [Animated Orb]   ┌──────────────────────────────────┐  │
│                   │ Vesper  12:00 PM                  │  │
│  VESPER           │ Good Evening, Boss! 🌙            │  │
│  AI Assistant     │ I'm Vesper, your AI assistant.    │  │
│                   └──────────────────────────────────┘  │
│  QUICK COMMANDS                        ┌──────────────┐  │
│  ☀️  Weather                          │ You  12:01PM │  │
│  🌐  Open YouTube               │ weather in Delhi │  │
│  🔍  Open Google                       └──────────────┘  │
│  📖  Wikipedia       ┌──────────────────────────────────┐│
│  🕐  Current Time    │ Vesper  12:01 PM                 ││
│  📅  Today's Date    │ 🌦️ Weather in Delhi:             ││
│  😂  Tell a Joke     │    Haze · 🌡️ 28°C (feels 31°C) ││
│  📰  Top News        │    💧 55%  💨 3.2 m/s           ││
│                      └──────────────────────────────────┘│
│  ● Ready                                                  │
│──────────────────────────────────────────────────────────│
│  🎙️  [ Type a command...                    ] [ Send ➤ ] │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8 or higher** — [python.org](https://python.org/downloads)
- A working **microphone**
- An active **internet connection** (for weather, Wikipedia, and speech recognition)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/satyam/vesper-assistant.git
cd vesper-assistant
```

**2. Install dependencies**
```bash
pip install pyttsx3 SpeechRecognition wikipedia requests pyaudio
```

> ⚠️ If `pyaudio` fails on Windows:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

**3. Run Vesper**
```bash
python vesper_assistant.py
```

---

## 🗣️ Commands

### 🌐 Web & Search
```
open youtube        → Opens YouTube
open google         → Opens Google
open gmail          → Opens Gmail
open github         → Opens GitHub
open news           → Opens Times of India headlines
search [anything]   → Google search for any query
```

### 📖 Knowledge
```
wikipedia [topic]   → Wikipedia summary (e.g. "wikipedia quantum computing")
weather in [city]   → Live weather (e.g. "weather in Mumbai")
```

### 🖥️ System Apps
```
open code           → VS Code
open chrome         → Google Chrome
open edge           → Microsoft Edge
open excel          → Microsoft Excel
open powerpoint     → Microsoft PowerPoint
open word           → Microsoft Word
play music          → Plays first track in ~/Music
```

### 🕐 Time & Date
```
what is the time    → Reads current time
what is the date    → Reads today's date
```

### 💬 Small Talk
```
how are you
what is your name
who created you
tell me a joke
thank you
```

### 👋 Exit
```
close / exit / goodbye / bye
```

---

## ⚙️ Configuration

### Change Voice Speed
In `vesper_assistant.py`, find:
```python
engine.setProperty('rate', 175)   # words per minute — increase or decrease
```

### Change TTS Voice
```python
engine.setProperty('voice', voices[0].id)  # 0 = first voice, 1 = second
```

### Custom Weather API Key
The project includes a default key. For production use, get your own free key at [openweathermap.org](https://openweathermap.org/api) and replace:
```python
api_key = "your_api_key_here"
```

### Custom Music Folder
```python
music_dir = os.path.join(os.path.expanduser("~"), "Music")
# Change to any path, e.g.: music_dir = "D:\\My Music"
```

### Mac / Linux
`sapi5` is Windows-only. Replace the engine init line:
```python
# engine = pyttsx3.init('sapi5')   # Windows
engine = pyttsx3.init()             # Mac / Linux
```

---

## 🔧 Troubleshooting

| Problem | Fix |
|---|---|
| `pyaudio` fails to install | Run `pip install pipwin` then `pipwin install pyaudio` |
| `No module named pyttsx3` | Run `pip install pyttsx3` |
| Mic not detected | Check **Settings → Privacy → Microphone** on Windows |
| "Say that again" every time | Check your internet — Google Speech API needs a connection |
| Weather: "City Not Found" | Use English city names (e.g. `Mumbai` not `Bombay`) |
| VS Code won't open | Add `code` to your PATH: in VS Code → Command Palette → *Install 'code' in PATH* |
| App freezes when speaking | Make sure you're on v2.0 — TTS now runs on a background thread |

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `pyttsx3` | Offline text-to-speech (SAPI5 on Windows) |
| `SpeechRecognition` | Microphone input + Google Speech transcription |
| `wikipedia` | Wikipedia article summaries |
| `requests` | HTTP calls for weather API |
| `pyaudio` | Microphone audio stream |
| `tkinter` | GUI framework (built into Python) |

---

## 📁 Project Structure

```
vesper-assistant/
│
├── vesper_assistant.py     # Main application — all-in-one
├── README.md               # This file
├── ABOUT.md                # Project background and credits
└── requirements.txt        # Pip dependencies
```

---

## 📄 `requirements.txt`

```
pyttsx3
SpeechRecognition
wikipedia
requests
pyaudio
```

---

## 📜 License

This project is open source under the **MIT License** — use it, modify it, share it freely.

---

<div align="center">

Built with ♥ by **Satyam**

*Vesper v2.0 — Your AI Desktop Assistant*

</div>
