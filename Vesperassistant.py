import tkinter as tk
from tkinter import font as tkfont
import threading
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import requests
import time
import math

# ─────────────────────────────────────────────
#  VOICE ENGINE  (thread-safe)
# ─────────────────────────────────────────────
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 175)
_speak_lock = threading.Lock()

def speak(audio: str):
    """Speak text without blocking the GUI."""
    def _speak():
        with _speak_lock:
            engine.say(audio)
            engine.runAndWait()
    threading.Thread(target=_speak, daemon=True).start()


# ─────────────────────────────────────────────
#  GREETING
# ─────────────────────────────────────────────
def get_greeting() -> str:
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good Morning, Boss! ☀️"
    elif hour < 18:
        return "Good Afternoon, Boss! 🌤️"
    else:
        return "Good Evening, Boss! 🌙"


# ─────────────────────────────────────────────
#  SPEECH RECOGNITION
# ─────────────────────────────────────────────
def take_command() -> str:
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.6)
            r.pause_threshold = 1.0
            audio = r.listen(source, timeout=8, phrase_time_limit=10)
        query = r.recognize_google(audio, language='en-in')
        return query
    except sr.WaitTimeoutError:
        return "None"
    except sr.UnknownValueError:
        return "None"
    except Exception:
        return "None"


# ─────────────────────────────────────────────
#  COMMAND PROCESSOR
# ─────────────────────────────────────────────
def process_command(query: str, app) -> str:
    """Process a voice/text command and return the assistant's reply."""
    q = query.lower().strip()

    if q in ("", "none"):
        return "I didn't catch that. Could you repeat?"

    # ── Wikipedia ──────────────────────────────
    if 'wikipedia' in q:
        topic = q.replace("wikipedia", "").strip()
        if not topic:
            return "Please tell me what to search on Wikipedia."
        try:
            app.set_status("Searching Wikipedia…")
            result = wikipedia.summary(topic, sentences=2, auto_suggest=True)
            speak(result)
            return f"📖 Wikipedia: {result}"
        except wikipedia.DisambiguationError as e:
            return f"Ambiguous topic. Did you mean: {', '.join(e.options[:4])}?"
        except Exception:
            return "Couldn't fetch Wikipedia results right now."

    # ── Web browsers ───────────────────────────
    elif 'open youtube' in q:
        webbrowser.open("https://www.youtube.com"); return "🎬 Opening YouTube!"
    elif 'open google' in q:
        webbrowser.open("https://www.google.com"); return "🔍 Opening Google!"
    elif 'open gmail' in q:
        webbrowser.open("https://mail.google.com"); return "📧 Opening Gmail!"
    elif 'open lpu' in q:
        webbrowser.open("https://ums.lpu.in/lpuums/"); return "🎓 Opening LPU portal!"
    elif 'open github' in q:
        webbrowser.open("https://www.github.com"); return "💻 Opening GitHub!"
    elif 'open news' in q or 'news' in q:
        webbrowser.open("https://timesofindia.indiatimes.com/home/headlines")
        return "📰 Here are some headlines from the Times of India. Happy reading!"

    # ── Search ─────────────────────────────────
    elif q.startswith('search '):
        topic = q.replace("search", "", 1).strip()
        webbrowser.open(f"https://www.google.com/search?q={topic}")
        return f"🔍 Searching the web for: {topic}"

    # ── System apps ────────────────────────────
    elif 'play music' in q:
        music_dir = os.path.join(os.path.expanduser("~"), "Music")
        if os.path.exists(music_dir):
            songs = [f for f in os.listdir(music_dir)
                     if f.endswith(('.mp3', '.wav', '.m4a'))]
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
                return f"🎵 Playing: {songs[0]}"
            return "No music files found in your Music folder."
        return "Music folder not found."

    elif 'open code' in q or 'open vs code' in q:
        try:
            os.startfile("code"); return "🖥️ Opening VS Code!"
        except Exception:
            return "VS Code not found. Is it installed?"

    elif 'open chrome' in q:
        paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        for p in paths:
            if os.path.exists(p):
                os.startfile(p); return "🌐 Opening Chrome!"
        return "Chrome not found."

    elif 'open edge' in q:
        path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        if os.path.exists(path):
            os.startfile(path); return "🌐 Opening Edge!"
        return "Edge not found."

    elif 'open excel' in q:
        _open_office("EXCEL.EXE"); return "📊 Opening Excel!"
    elif 'open powerpoint' in q:
        _open_office("POWERPNT.EXE"); return "📊 Opening PowerPoint!"
    elif 'open word' in q:
        _open_office("WINWORD.EXE"); return "📝 Opening Word!"

    # ── Time & Date ────────────────────────────
    elif 'time' in q:
        t = datetime.datetime.now().strftime("%I:%M %p")
        return f"🕐 The time is {t}."

    elif 'date' in q:
        d = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"📅 Today is {d}."

    # ── Weather ────────────────────────────────
    elif 'weather' in q:
        city = q.replace("weather", "").replace("in", "").strip()
        if not city:
            return "Please say: weather in [city name]"
        return get_weather(city)

    # ── Small talk ─────────────────────────────
    elif 'how are you' in q:
        return "I'm running smoothly and ready to help! 😊"
    elif 'your name' in q:
        return "I'm Vesper, your personal AI assistant! ☀️"
    elif 'who made you' in q or 'who created you' in q or 'boss' in q:
        return "I was crafted by Satyam — and he is absolutely my boss! 💪"
    elif 'joke' in q:
        return "Why do programmers prefer dark mode? Because light attracts bugs! 🐛😄"
    elif 'thank' in q:
        return "You're welcome, Boss! Always at your service. 🤝"

    # ── Exit ───────────────────────────────────
    elif 'close' in q or 'exit' in q or 'goodbye' in q or 'bye' in q:
        speak("Goodbye! Have a great day, Boss!")
        app.root.after(1500, app.root.destroy)
        return "👋 Goodbye! Have a great day!"

    # ── Fallback ───────────────────────────────
    else:
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"🔍 I'm not sure about that. Searching Google for: {query}"


def _open_office(exe: str):
    base = r"C:\Program Files\Microsoft Office\root\Office16"
    path = os.path.join(base, exe)
    if os.path.exists(path):
        os.startfile(path)


def get_weather(city: str) -> str:
    api_key = "8ef61edcf1c576d65d836254e11ea420"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        data = requests.get(url, timeout=6).json()
        if data.get("cod") != 200:
            return f"City '{city}' not found. Please check the name."
        main = data["main"]
        desc = data["weather"][0]["description"].capitalize()
        temp = main["temp"]
        feels = main["feels_like"]
        hum = main["humidity"]
        wind = data["wind"]["speed"]
        result = (
            f"🌦️ Weather in {city.title()}:\n"
            f"   {desc}\n"
            f"   🌡️ Temp: {temp}°C  (feels like {feels}°C)\n"
            f"   💧 Humidity: {hum}%\n"
            f"   💨 Wind: {wind} m/s"
        )
        speak(f"Weather in {city}: {desc}, temperature {temp} degrees Celsius.")
        return result
    except requests.exceptions.ConnectionError:
        return "No internet connection. Cannot fetch weather."
    except Exception as e:
        return f"Weather error: {str(e)}"


# ─────────────────────────────────────────────
#  COLOUR PALETTE & THEME
# ─────────────────────────────────────────────
C = {
    "bg":          "#0A0E1A",   # deep navy
    "sidebar":     "#0F1525",   # slightly lighter
    "panel":       "#131928",   # card bg
    "border":      "#1E2D4A",   # subtle border
    "accent1":     "#00D4FF",   # electric cyan
    "accent2":     "#7B5CFA",   # violet
    "accent3":     "#00FFB2",   # mint green
    "user_bubble": "#1A2744",
    "bot_bubble":  "#0F2030",
    "text":        "#E8F0FF",
    "subtext":     "#6B7FA8",
    "danger":      "#FF4C6A",
    "warn":        "#FFB347",
}


# ─────────────────────────────────────────────
#  ANIMATED CANVAS ORB
# ─────────────────────────────────────────────
class PulseOrb(tk.Canvas):
    """Animates a glowing orb that pulses when the assistant is listening."""
    def __init__(self, parent, size=64, **kwargs):
        super().__init__(parent, width=size, height=size,
                         bg=C["sidebar"], highlightthickness=0, **kwargs)
        self.size = size
        self.cx = size // 2
        self.cy = size // 2
        self.t = 0
        self.listening = False
        self._draw()

    def _draw(self):
        self.delete("all")
        cx, cy, r = self.cx, self.cy, self.size // 2 - 4
        # outer glow rings
        for i in range(3):
            factor = 0.55 + 0.15 * i
            if self.listening:
                pulse = 1 + 0.18 * math.sin(self.t * 0.18 + i * 1.2)
            else:
                pulse = 1 + 0.06 * math.sin(self.t * 0.06 + i * 1.2)
            rr = r * factor * pulse
            self.create_oval(cx - rr, cy - rr, cx + rr, cy + rr,
                             fill="", outline=C["accent1"], width=1)
        # core
        core_r = r * 0.42
        if self.listening:
            beat = 1 + 0.22 * math.sin(self.t * 0.22)
            core_r *= beat
        # gradient simulation with layered ovals
        layers = 8
        for i in range(layers, 0, -1):
            frac = i / layers
            cr = core_r * frac
            blend = int(0 + (frac * 80))
            col = f"#00{blend:02x}{min(255, blend + 130):02x}"
            self.create_oval(cx - cr, cy - cr, cx + cr, cy + cr,
                             fill=col, outline="")
        self.t += 1
        self.after(30, self._draw)

    def set_listening(self, state: bool):
        self.listening = state


# ─────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────
class VesperApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Vesper — AI Assistant")
        self.root.geometry("860x620")
        self.root.minsize(760, 540)
        self.root.configure(bg=C["bg"])
        self.root.resizable(True, True)

        # ── Fonts ──
        self.font_title  = tkfont.Font(family="Segoe UI", size=20, weight="bold")
        self.font_sub    = tkfont.Font(family="Segoe UI", size=10)
        self.font_label  = tkfont.Font(family="Segoe UI", size=9, weight="bold")
        self.font_chat   = tkfont.Font(family="Segoe UI", size=11)
        self.font_input  = tkfont.Font(family="Segoe UI", size=12)
        self.font_btn    = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.font_cmd    = tkfont.Font(family="Segoe UI", size=9)
        self.font_status = tkfont.Font(family="Segoe UI", size=9, slant="italic")

        self._build_ui()
        self._greet()

    # ── UI CONSTRUCTION ──────────────────────────
    def _build_ui(self):
        # outer container
        outer = tk.Frame(self.root, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=1, pady=1)

        # ─ LEFT SIDEBAR ──────────────────────────
        sidebar = tk.Frame(outer, bg=C["sidebar"], width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # logo area
        logo_frame = tk.Frame(sidebar, bg=C["sidebar"], pady=24)
        logo_frame.pack(fill="x")

        self.orb = PulseOrb(logo_frame, size=72)
        self.orb.pack()

        tk.Label(logo_frame, text="VESPER", bg=C["sidebar"],
                 fg=C["accent1"], font=self.font_title).pack(pady=(8, 0))
        tk.Label(logo_frame, text="AI Assistant v2.0", bg=C["sidebar"],
                 fg=C["subtext"], font=self.font_sub).pack()

        # divider
        tk.Frame(sidebar, bg=C["border"], height=1).pack(fill="x", padx=16, pady=12)

        # quick commands
        tk.Label(sidebar, text="QUICK COMMANDS", bg=C["sidebar"],
                 fg=C["subtext"], font=self.font_label).pack(anchor="w", padx=16)

        cmds = [
            ("☀️  Weather", "weather in Delhi"),
            ("🌐  Open YouTube", "open youtube"),
            ("🔍  Open Google", "open google"),
            ("📖  Wikipedia", "wikipedia Python"),
            ("🕐  Current Time", "what is the time"),
            ("📅  Today's Date", "what is the date"),
            ("😂  Tell a Joke", "tell me a joke"),
            ("📰  Top News", "open news"),
        ]
        for label, cmd in cmds:
            btn = tk.Button(
                sidebar, text=label, anchor="w",
                bg=C["sidebar"], fg=C["text"],
                activebackground=C["panel"], activeforeground=C["accent1"],
                relief="flat", cursor="hand2",
                font=self.font_cmd, padx=16, pady=6,
                command=lambda c=cmd: self._run_command(c)
            )
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=C["panel"], fg=C["accent1"]))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=C["sidebar"], fg=C["text"]))

        tk.Frame(sidebar, bg=C["border"], height=1).pack(fill="x", padx=16, pady=12)

        # status indicator
        self.status_var = tk.StringVar(value="● Ready")
        tk.Label(sidebar, textvariable=self.status_var,
                 bg=C["sidebar"], fg=C["accent3"],
                 font=self.font_status).pack(anchor="w", padx=18, pady=4)

        # ─ MAIN PANEL ─────────────────────────────
        main = tk.Frame(outer, bg=C["bg"])
        main.pack(side="left", fill="both", expand=True)

        # header bar
        header = tk.Frame(main, bg=C["panel"], height=52)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="Chat with Vesper", bg=C["panel"],
                 fg=C["text"], font=self.font_title).pack(side="left", padx=20, pady=10)

        # datetime label
        self.dt_var = tk.StringVar()
        tk.Label(header, textvariable=self.dt_var,
                 bg=C["panel"], fg=C["subtext"],
                 font=self.font_sub).pack(side="right", padx=20)
        self._update_clock()

        # thin accent line
        tk.Frame(main, bg=C["accent2"], height=2).pack(fill="x")

        # ─ CHAT AREA ──────────────────────────────
        chat_outer = tk.Frame(main, bg=C["bg"])
        chat_outer.pack(fill="both", expand=True, padx=0, pady=0)

        self.chat_frame = tk.Frame(chat_outer, bg=C["bg"])
        self.chat_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.chat_frame, bg=C["bg"],
                                highlightthickness=0)
        scrollbar = tk.Scrollbar(self.chat_frame, orient="vertical",
                                 command=self.canvas.yview,
                                 bg=C["bg"], troughcolor=C["bg"])
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.msg_container = tk.Frame(self.canvas, bg=C["bg"])
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.msg_container, anchor="nw")

        self.msg_container.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # ─ INPUT BAR ──────────────────────────────
        input_bar = tk.Frame(main, bg=C["panel"], height=70)
        input_bar.pack(fill="x", side="bottom")
        input_bar.pack_propagate(False)

        # mic button
        self.mic_btn = tk.Button(
            input_bar, text="🎙️", font=tkfont.Font(size=18),
            bg=C["panel"], fg=C["accent1"],
            activebackground=C["panel"], activeforeground=C["accent3"],
            relief="flat", cursor="hand2", width=3,
            command=self._start_voice_thread
        )
        self.mic_btn.pack(side="left", padx=(16, 4), pady=12)

        # text entry
        entry_frame = tk.Frame(input_bar, bg=C["border"],
                               highlightbackground=C["border"],
                               highlightthickness=1, bd=0)
        entry_frame.pack(side="left", fill="both", expand=True, pady=14, padx=4)

        self.entry = tk.Entry(
            entry_frame, font=self.font_input,
            bg=C["user_bubble"], fg=C["text"],
            insertbackground=C["accent1"],
            relief="flat", bd=8
        )
        self.entry.pack(fill="both", expand=True)
        self.entry.bind("<Return>", lambda e: self._send_text())
        self.entry.bind("<FocusIn>",
            lambda e: entry_frame.configure(highlightbackground=C["accent1"]))
        self.entry.bind("<FocusOut>",
            lambda e: entry_frame.configure(highlightbackground=C["border"]))

        # send button
        self.send_btn = self._accent_button(
            input_bar, "Send ➤", C["accent1"],
            command=self._send_text
        )
        self.send_btn.pack(side="right", padx=(4, 16), pady=14)

    # ── BUBBLE RENDERING ─────────────────────────
    def _add_bubble(self, text: str, sender: str):
        """Render a chat bubble for user or bot."""
        is_user = (sender == "user")
        outer = tk.Frame(self.msg_container, bg=C["bg"], pady=4)
        outer.pack(fill="x", padx=12)

        # timestamp
        ts = datetime.datetime.now().strftime("%I:%M %p")

        if is_user:
            side_frame = tk.Frame(outer, bg=C["bg"])
            side_frame.pack(side="right")
            label_row = tk.Frame(side_frame, bg=C["bg"])
            label_row.pack(anchor="e")
            tk.Label(label_row, text=f"You  {ts}", bg=C["bg"],
                     fg=C["subtext"], font=self.font_label).pack(side="right")
            bubble_color = C["user_bubble"]
            fg_color = C["text"]
            bubble_side = "right"
            max_w = 420
        else:
            side_frame = tk.Frame(outer, bg=C["bg"])
            side_frame.pack(side="left")
            label_row = tk.Frame(side_frame, bg=C["bg"])
            label_row.pack(anchor="w")
            tk.Label(label_row, text=f"Vesper  {ts}", bg=C["bg"],
                     fg=C["accent1"], font=self.font_label).pack(side="left")
            bubble_color = C["bot_bubble"]
            fg_color = C["text"]
            bubble_side = "left"
            max_w = 480

        bubble = tk.Frame(side_frame, bg=bubble_color,
                          padx=14, pady=10,
                          highlightbackground=C["border"],
                          highlightthickness=1)
        bubble.pack(anchor="e" if is_user else "w")

        msg_label = tk.Label(bubble, text=text, bg=bubble_color,
                             fg=fg_color, font=self.font_chat,
                             wraplength=max_w, justify="left" if not is_user else "right",
                             anchor="w")
        msg_label.pack()

        self.root.update_idletasks()
        self.canvas.yview_moveto(1.0)

    # ── ACCENT BUTTON FACTORY ────────────────────
    def _accent_button(self, parent, text, color, command=None):
        btn = tk.Button(
            parent, text=text, font=self.font_btn,
            bg=color, fg=C["bg"],
            activebackground=C["accent2"], activeforeground=C["text"],
            relief="flat", cursor="hand2", padx=18, pady=8,
            command=command
        )
        btn.bind("<Enter>", lambda e: btn.configure(bg=C["accent2"], fg=C["text"]))
        btn.bind("<Leave>", lambda e: btn.configure(bg=color, fg=C["bg"]))
        return btn

    # ── CANVAS RESIZE ────────────────────────────
    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ── CLOCK ────────────────────────────────────
    def _update_clock(self):
        now = datetime.datetime.now().strftime("%A, %b %d  •  %I:%M:%S %p")
        self.dt_var.set(now)
        self.root.after(1000, self._update_clock)

    # ── STATUS BAR ───────────────────────────────
    def set_status(self, text: str, color: str = None):
        color = color or C["accent3"]
        self.status_var.set(f"● {text}")
        # reset to ready after delay
        self.root.after(3000, lambda: self.status_var.set("● Ready"))

    # ── SEND TEXT ────────────────────────────────
    def _send_text(self):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, "end")
        self._run_command(text)

    # ── RUN COMMAND ──────────────────────────────
    def _run_command(self, query: str):
        self._add_bubble(query, "user")
        self.set_status("Thinking…")
        threading.Thread(
            target=self._process_and_reply,
            args=(query,), daemon=True
        ).start()

    def _process_and_reply(self, query: str):
        reply = process_command(query, self)
        self.root.after(0, lambda: self._add_bubble(reply, "bot"))
        self.root.after(0, lambda: self.set_status("Ready"))

    # ── VOICE INPUT ──────────────────────────────
    def _start_voice_thread(self):
        threading.Thread(target=self._listen_and_process,
                         daemon=True).start()

    def _listen_and_process(self):
        self.root.after(0, lambda: self.mic_btn.configure(
            fg=C["danger"], text="⏹️"))
        self.root.after(0, lambda: self.orb.set_listening(True))
        self.root.after(0, lambda: self.set_status("Listening…", C["danger"]))

        query = take_command()

        self.root.after(0, lambda: self.mic_btn.configure(
            fg=C["accent1"], text="🎙️"))
        self.root.after(0, lambda: self.orb.set_listening(False))

        if query and query.lower() != "none":
            self.root.after(0, lambda: self._run_command(query))
        else:
            self.root.after(0, lambda: self._add_bubble(
                "I didn't catch that. Try again or type your command.", "bot"))
            self.root.after(0, lambda: self.set_status("Ready"))

    # ── GREETING ─────────────────────────────────
    def _greet(self):
        greeting = get_greeting()
        welcome = (
            f"{greeting}\n"
            "I'm Vesper, your AI assistant.\n"
            "Type a command below or click 🎙️ to speak."
        )
        self._add_bubble(welcome, "bot")
        speak(greeting + " I'm Vesper, your AI assistant. How may I assist you?")

    # ── RUN ──────────────────────────────────────
    def run(self):
        self.root.mainloop()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = VesperApp()
    app.run()