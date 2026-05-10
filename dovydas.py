import customtkinter as ctk
import serial
import serial.tools.list_ports
import threading
import ctypes
import ctypes.wintypes
import keyboard
import pythoncom
import json
import os
import time
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
PROFILES_FILE = os.path.join(BASE_DIR, "profiles.json")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

# ── Colors ─────────────────────────────────────────────────────────────────
BG_DARK     = "#0d1117"
BG_PANEL    = "#161b22"
BG_CARD     = "#1c2128"
BG_ROW      = "#21262d"
BG_ROW_ALT  = "#1c2128"
ACCENT      = "#2f81f7"
ACCENT_DARK = "#1a6fd4"
SUCCESS     = "#3fb950"
DANGER      = "#f85149"
WARNING     = "#d29922"
TEXT_PRI    = "#e6edf3"
TEXT_SEC    = "#8b949e"
TEXT_DIM    = "#484f58"
BORDER      = "#30363d"

# ── Language strings ───────────────────────────────────────────────────────
LANG = {
    "EN": {
        "title": "Stream Deck Controller",
        "subtitle": "Manage your Stream Deck",
        "connection": "CONNECTION",
        "rgb_mode": "RGB MODE",
        "led_speed": "LED SPEED",
        "slow": "SLOW", "fast": "FAST",
        "status_dis": "Disconnected",
        "status_con": "Connected",
        "status_err": "Error",
        "connect": "CONNECT", "stop": "STOP",
        "no_ports": "No Ports",
        "tab_buttons": "Buttons",
        "tab_audio": "Audio Mix",
        "tab_shortcuts": "Add Shortcuts",
        "tab_profiles": "Profiles",
        "button": "Button",
        "knob": "Knob",
        "key_ph": "Key (e.g. f13) or Path",
        "app_name_lbl": "Application Name",
        "app_name_ph": "e.g. Notepad",
        "app_path_lbl": "Path to .exe or URI",
        "app_path_ph": "e.g. C:\\Windows\\notepad.exe  or  discord://",
        "add_shortcut": "ADD SHORTCUT",
        "save_tab": "Save",
        "load_tab": "Load",
        "profile_name_ph": "Profile name...",
        "save_btn": "SAVE PROFILE",
        "load_btn": "LOAD PROFILE",
        "delete_btn": "DELETE",
        "no_profiles": "No saved profiles",
        "language": "LANGUAGE",
        "run_bg": "Run in background when closed",
        "saved_ok": "✓  Profile saved",
        "loaded_ok": "✓  Profile loaded",
        "deleted_ok": "✓  Profile deleted",
        "waiting_title": "Waiting for connection...",
        "waiting_body": "Connect your device to get started",
        "open": "Open", "exit": "Exit",
    },
    "LT": {
        "title": "Stream Deck Controller",
        "subtitle": "Valdykite savo Stream Deck",
        "connection": "JUNGTIS",
        "rgb_mode": "RGB REŽIMAS",
        "led_speed": "LED GREITIS",
        "slow": "LĖTAI", "fast": "GREITAI",
        "status_dis": "Atsijungta",
        "status_con": "Prisijungta",
        "status_err": "Klaida",
        "connect": "PRISIJUNGTI", "stop": "SUSTABDYTI",
        "no_ports": "Nėra jungčių",
        "tab_buttons": "Mygtukai",
        "tab_audio": "Garsas",
        "tab_shortcuts": "Nuorodos",
        "tab_profiles": "Profiliai",
        "button": "Mygtukas",
        "knob": "Potenc.",
        "key_ph": "Klavišas arba kelias",
        "app_name_lbl": "Programos pavadinimas",
        "app_name_ph": "pvz. Notepad",
        "app_path_lbl": "Kelias iki .exe arba URI",
        "app_path_ph": "pvz. C:\\Windows\\notepad.exe",
        "add_shortcut": "PRIDĖTI",
        "save_tab": "Išsaugoti",
        "load_tab": "Įkelti",
        "profile_name_ph": "Profilio pavadinimas...",
        "save_btn": "IŠSAUGOTI PROFILĮ",
        "load_btn": "ĮKELTI PROFILĮ",
        "delete_btn": "IŠTRINTI",
        "no_profiles": "Nėra išsaugotų profilių",
        "language": "KALBA",
        "run_bg": "Veikti fone uždarius langą",
        "saved_ok": "✓  Profilis išsaugotas",
        "loaded_ok": "✓  Profilis įkeltas",
        "deleted_ok": "✓  Profilis ištrintas",
        "waiting_title": "Laukiama prisijungimo...",
        "waiting_body": "Prijunkite įrenginį",
        "open": "Atidaryti", "exit": "Išeiti",
    },
    "RU": {
        "title": "Stream Deck Controller",
        "subtitle": "Управление Stream Deck",
        "connection": "ПОДКЛЮЧЕНИЕ",
        "rgb_mode": "RGB РЕЖИМ",
        "led_speed": "СКОРОСТЬ LED",
        "slow": "МЕДЛ.", "fast": "БЫСТРО",
        "status_dis": "Отключено",
        "status_con": "Подключено",
        "status_err": "Ошибка",
        "connect": "ПОДКЛЮЧИТЬ", "stop": "СТОП",
        "no_ports": "Нет портов",
        "tab_buttons": "Кнопки",
        "tab_audio": "Аудио",
        "tab_shortcuts": "Ярлыки",
        "tab_profiles": "Профили",
        "button": "Кнопка",
        "knob": "Регулятор",
        "key_ph": "Клавиша или путь",
        "app_name_lbl": "Название приложения",
        "app_name_ph": "напр. Notepad",
        "app_path_lbl": "Путь к .exe или URI",
        "app_path_ph": "напр. C:\\Windows\\notepad.exe",
        "add_shortcut": "ДОБАВИТЬ",
        "save_tab": "Сохранить",
        "load_tab": "Загрузить",
        "profile_name_ph": "Имя профиля...",
        "save_btn": "СОХРАНИТЬ ПРОФИЛЬ",
        "load_btn": "ЗАГРУЗИТЬ ПРОФИЛЬ",
        "delete_btn": "УДАЛИТЬ",
        "no_profiles": "Нет сохранённых профилей",
        "language": "ЯЗЫК",
        "run_bg": "Работать в фоне при закрытии",
        "saved_ok": "✓  Профиль сохранён",
        "loaded_ok": "✓  Профиль загружен",
        "deleted_ok": "✓  Профиль удалён",
        "waiting_title": "Ожидание подключения...",
        "waiting_body": "Подключите устройство",
        "open": "Открыть", "exit": "Выход",
    },
}

# ── Tray constants ─────────────────────────────────────────────────────────
WM_APP = 0x8000
NIM_ADD, NIM_DELETE = 0x00000000, 0x00000002
NIF_MESSAGE, NIF_ICON, NIF_TIP = 0x1, 0x2, 0x4
WM_RBUTTONUP = 0x0205
WM_LBUTTONDBLCLK = 0x0203
IDI_APPLICATION = 32512
TPM_RETURNCMD, TPM_NONOTIFY = 0x0100, 0x0080
MF_STRING = 0x0000

class NOTIFYICONDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize",           ctypes.c_ulong),
        ("hWnd",             ctypes.c_void_p),
        ("uID",              ctypes.c_uint),
        ("uFlags",           ctypes.c_uint),
        ("uCallbackMessage", ctypes.c_uint),
        ("hIcon",            ctypes.c_void_p),
        ("szTip",            ctypes.c_wchar * 128),
    ]

def shell_open(path: str):
    ctypes.windll.shell32.ShellExecuteW(None, "open", path, None, None, 1)

# ── Audio Worker ──────────────────────────────────────────────────────────
class AudioWorker(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self._lock    = threading.Lock()
        self._pending: dict[int, tuple[str, float]] = {}
        self._event   = threading.Event()
        self.running  = True

    def request(self, index: int, target: str, vol: float):
        with self._lock:
            self._pending[index] = (target, vol)
        self._event.set()

    def run(self):
        pythoncom.CoInitialize()
        try:
            while self.running:
                self._event.wait()
                self._event.clear()
                with self._lock:
                    tasks = dict(self._pending)
                    self._pending.clear()
                for target, vol in tasks.values():
                    self._apply(target, vol)
        finally:
            pythoncom.CoUninitialize()

    def _apply(self, target: str, vol: float):
        """
        target is the raw exe/key string (from audio_presets_map values),
        e.g. "master", "mic", "spotify.exe", etc.
        """
        vol = max(0.0, min(1.0, vol))
        try:
            if target == "master":
                # ── Master playback volume ─────────────────────────
                device   = AudioUtilities.GetSpeakers()
                endpoint = device.EndpointVolume
                endpoint.SetMasterVolumeLevelScalar(vol, None)

            elif target == "mic":
                # ── Microphone input level ─────────────────────────
                from pycaw.pycaw import AudioUtilities as AU
                mic = AU.GetMicrophone()
                if mic:
                    mic_endpoint = mic.EndpointVolume
                    mic_endpoint.SetMasterVolumeLevelScalar(vol, None)

            else:
                # ── Per-app session volume ─────────────────────────
                for s in AudioUtilities.GetAllSessions():
                    if s.Process and target.lower() in s.Process.name().lower():
                        s.SimpleAudioVolume.SetMasterVolume(vol, None)
        except Exception:
            pass

    def stop(self):
        self.running = False
        self._event.set()

# ── Settings ──────────────────────────────────────────────────────────────
def load_settings() -> dict:
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"language": "EN", "last_profile": ""}

def save_settings(data: dict):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def load_profiles() -> dict:
    try:
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_profiles(data: dict):
    try:
        with open(PROFILES_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

# ══════════════════════════════════════════════════════════════════════════
# Custom widgets
# ══════════════════════════════════════════════════════════════════════════

class SectionLabel(ctk.CTkLabel):
    def __init__(self, parent, text, **kw):
        super().__init__(parent, text=text,
                         font=("Segoe UI", 10, "bold"),
                         text_color=TEXT_SEC, **kw)

class StyledEntry(ctk.CTkEntry):
    def __init__(self, parent, **kw):
        kw.setdefault("fg_color", BG_ROW)
        kw.setdefault("border_color", BORDER)
        kw.setdefault("border_width", 1)
        kw.setdefault("text_color", TEXT_PRI)
        kw.setdefault("placeholder_text_color", TEXT_DIM)
        kw.setdefault("font", ("Segoe UI", 12))
        super().__init__(parent, **kw)

class StyledCombo(ctk.CTkComboBox):
    def __init__(self, parent, **kw):
        kw.setdefault("fg_color", BG_ROW)
        kw.setdefault("border_color", BORDER)
        kw.setdefault("border_width", 1)
        kw.setdefault("text_color", TEXT_PRI)
        kw.setdefault("button_color", BORDER)
        kw.setdefault("button_hover_color", ACCENT)
        kw.setdefault("dropdown_fg_color", BG_CARD)
        kw.setdefault("dropdown_hover_color", BG_ROW)
        kw.setdefault("dropdown_text_color", TEXT_PRI)
        kw.setdefault("font", ("Segoe UI", 12))
        super().__init__(parent, **kw)

class StyledButton(ctk.CTkButton):
    def __init__(self, parent, **kw):
        kw.setdefault("fg_color", ACCENT)
        kw.setdefault("hover_color", ACCENT_DARK)
        kw.setdefault("text_color", "#ffffff")
        kw.setdefault("font", ("Segoe UI", 12, "bold"))
        kw.setdefault("corner_radius", 6)
        kw.setdefault("height", 36)
        super().__init__(parent, **kw)

class DangerButton(ctk.CTkButton):
    def __init__(self, parent, **kw):
        kw.setdefault("fg_color", "#2d1a1a")
        kw.setdefault("hover_color", "#3d2020")
        kw.setdefault("text_color", DANGER)
        kw.setdefault("border_color", "#4a2020")
        kw.setdefault("border_width", 1)
        kw.setdefault("font", ("Segoe UI", 12, "bold"))
        kw.setdefault("corner_radius", 6)
        kw.setdefault("height", 36)
        super().__init__(parent, **kw)

# ══════════════════════════════════════════════════════════════════════════
# Main App
# ══════════════════════════════════════════════════════════════════════════

class PultoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.settings    = load_settings()
        self.lang_code   = self.settings.get("language", "EN")
        self.T           = LANG[self.lang_code]
        self.profiles    = load_profiles()
        self.ser         = None
        self.running     = False
        self.bg_run      = True   # minimize to tray when closed

        self.audio_worker = AudioWorker()
        self.audio_worker.start()

        # ── Built-in apps & system actions ────────────────────────
        # Special prefix "SYS:" means a system action, not a URI/path
        self.custom_apps = {
            # ── Communication ──────────────────────────────────────
            "Discord":          "discord://",
            "Telegram":         "tg://",
            "Slack":            "slack://open",
            "Teams":            "msteams://",
            "Zoom":             "zoommtg://zoom.us/start",
            "WhatsApp":         "whatsapp://",
            "Skype":            "skype:",
            # ── Music / Video ──────────────────────────────────────
            "Spotify":          "spotify:",
            "YouTube Music":    "https://music.youtube.com",
            "VLC":              r"C:\Program Files\VideoLAN\VLC\vlc.exe",
            "Netflix":          "https://netflix.com",
            "Twitch":           "https://twitch.tv",
            "YouTube":          "https://youtube.com",
            # ── Browsers ──────────────────────────────────────────
            "Chrome":           "https://google.com",
            "Firefox":          r"C:\Program Files\Mozilla Firefox\firefox.exe",
            "Edge":             r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            # ── Creative / Streaming ───────────────────────────────
            "OBS Studio":       r"C:\Program Files\obs-studio\bin\64bit\obs64.exe",
            "Photoshop":        r"C:\Program Files\Adobe\Adobe Photoshop 2024\Photoshop.exe",
            "Premiere Pro":     r"C:\Program Files\Adobe\Adobe Premiere Pro 2024\Adobe Premiere Pro.exe",
            "After Effects":    r"C:\Program Files\Adobe\Adobe After Effects 2024\AfterFX.exe",
            "DaVinci Resolve":  r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe",
            "Blender":          r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
            "GIMP":             r"C:\Program Files\GIMP 2\bin\gimp-2.10.exe",
            # ── Dev tools ─────────────────────────────────────────
            "VS Code":          r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            "Notepad":          r"C:\Windows\notepad.exe",
            "Notepad++":        r"C:\Program Files\Notepad++\notepad++.exe",
            "Terminal":         r"C:\Windows\System32\wt.exe",
            "CMD":              r"C:\Windows\System32\cmd.exe",
            "PowerShell":       r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
            # ── Games / Launchers ──────────────────────────────────
            "Steam":            "steam://open/main",
            "Epic Games":       r"C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe",
            "Battle.net":       r"C:\Program Files (x86)\Battle.net\Battle.net.exe",
            "Xbox App":         "xbox:",
            # ── Windows utilities ─────────────────────────────────
            "File Explorer":    r"C:\Windows\explorer.exe",
            "Task Manager":     r"C:\Windows\System32\Taskmgr.exe",
            "Calculator":       r"C:\Windows\System32\calc.exe",
            "Paint":            r"C:\Windows\System32\mspaint.exe",
            "Snipping Tool":    r"C:\Windows\System32\SnippingTool.exe",
            "Settings":         "ms-settings:",
            "Control Panel":    r"C:\Windows\System32\control.exe",
            # ── System actions (handled specially in listen()) ─────
            "Play / Pause":     "SYS:media_play_pause",
            "Next Track":       "SYS:media_next",
            "Prev Track":       "SYS:media_prev",
            "Volume Mute":      "SYS:media_mute",
            "Shutdown":         "SYS:shutdown",
            "Restart":          "SYS:restart",
            "Sleep":            "SYS:sleep",
            "Lock PC":          "SYS:lock",
            "Screenshot":       "SYS:screenshot",
            "Custom Key":       "SYS:custom",
        }
        # audio_presets: display_name -> exe_name (or special key)
        # "master"   = Windows master volume
        # "mic"      = microphone input level
        # anything else = searched in running app sessions by exe name
        self.audio_presets_map = {
            "🔊 Master Volume":     "master",
            "🎙 Microphone":        "mic",
            "🎵 Spotify":           "spotify.exe",
            "💬 Discord":           "discord.exe",
            "🌐 Chrome":            "chrome.exe",
            "🌐 Edge":              "msedge.exe",
            "🌐 Firefox":           "firefox.exe",
            "📺 VLC":               "vlc.exe",
            "🔴 OBS Studio":        "obs64.exe",
            "👥 Teams":             "teams.exe",
            "📹 Zoom":              "zoom.exe",
            "🎮 Discord (game)":    "discord.exe",
            "🎧 Voicemod":          "voicemod.exe",
            "🎚 Equalizer APO":     "peace.exe",
        }
        self.audio_presets = list(self.audio_presets_map.keys())

        self.title(self.T["title"])
        self.geometry("1180x740")
        self.minsize(900, 600)
        self.configure(fg_color=BG_DARK)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ── Custom window icon (place icon.ico or icon.png next to script) ──
        for _icon_name in ("icon.ico", "icon.png"):
            _icon_path = os.path.join(BASE_DIR, _icon_name)
            if os.path.exists(_icon_path):
                try:
                    if _icon_name.endswith(".ico"):
                        self.iconbitmap(_icon_path)
                    else:
                        from PIL import Image, ImageTk
                        _img = Image.open(_icon_path).resize((32, 32))
                        self._icon_img = ImageTk.PhotoImage(_img)
                        self.iconphoto(True, self._icon_img)
                except Exception:
                    pass
                break

        self._build_sidebar()
        self._build_main()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Auto-load last profile
        last = self.settings.get("last_profile", "")
        if last and last in self.profiles:
            self._apply_profile(self.profiles[last])

        # Auto-connect on startup (only if enabled in settings)
        if self.settings.get("auto_connect", True):
            self.after(300, self._try_auto_connect)

    # ══════════════════════════════════════════════════════════════
    # SIDEBAR
    # ══════════════════════════════════════════════════════════════
    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, width=270, corner_radius=0,
                          fg_color=BG_PANEL, border_width=0)
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)
        sb.grid_rowconfigure(99, weight=1)

        # Title block
        title_f = ctk.CTkFrame(sb, fg_color="transparent")
        title_f.pack(fill="x", padx=20, pady=(24, 0))
        ctk.CTkLabel(title_f, text="⬡", font=("Segoe UI", 26),
                     text_color=ACCENT).pack(side="left", padx=(0, 10))
        txt_f = ctk.CTkFrame(title_f, fg_color="transparent")
        txt_f.pack(side="left")
        ctk.CTkLabel(txt_f, text="Stream Deck",
                     font=("Segoe UI", 15, "bold"),
                     text_color=TEXT_PRI).pack(anchor="w")
        ctk.CTkLabel(txt_f, text=self.T["subtitle"],
                     font=("Segoe UI", 10),
                     text_color=TEXT_SEC).pack(anchor="w")

        # Divider
        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(
            fill="x", padx=20, pady=18)

        # Language
        SectionLabel(sb, self.T["language"]).pack(anchor="w", padx=20, pady=(0, 4))
        self.lang_menu = ctk.CTkSegmentedButton(
            sb, values=["EN", "LT", "RU"],
            command=self._change_language,
            fg_color=BG_ROW,
            selected_color=ACCENT,
            selected_hover_color=ACCENT_DARK,
            unselected_color=BG_ROW,
            unselected_hover_color=BG_CARD,
            text_color=TEXT_PRI,
            font=("Segoe UI", 12, "bold"),
        )
        self.lang_menu.set(self.lang_code)
        self.lang_menu.pack(fill="x", padx=20, pady=(0, 16))

        # Connection section
        SectionLabel(sb, self.T["connection"]).pack(anchor="w", padx=20, pady=(0, 4))
        self.port_menu = ctk.CTkOptionMenu(
            sb, values=self.get_ports(),
            fg_color=BG_ROW, button_color=BORDER,
            button_hover_color=ACCENT,
            dropdown_fg_color=BG_CARD,
            dropdown_hover_color=BG_ROW,
            text_color=TEXT_PRI,
            font=("Segoe UI", 12),
            dynamic_resizing=False,
        )
        self.port_menu.pack(fill="x", padx=20, pady=(0, 8))

        self.conn_btn = ctk.CTkButton(
            sb, text=f"⬡  {self.T['connect']}",
            fg_color=ACCENT, hover_color=ACCENT_DARK,
            text_color="#fff",
            font=("Segoe UI", 13, "bold"),
            height=40, corner_radius=8,
            command=self.toggle_connection,
        )
        self.conn_btn.pack(fill="x", padx=20, pady=(0, 10))

        # Status dot
        self.status_f = ctk.CTkFrame(sb, fg_color="transparent")
        self.status_f.pack(anchor="w", padx=20, pady=(0, 16))
        self.status_dot = ctk.CTkLabel(self.status_f, text="●",
                                        font=("Segoe UI", 10),
                                        text_color=TEXT_DIM)
        self.status_dot.pack(side="left")
        self.status_lbl = ctk.CTkLabel(self.status_f,
                                        text=f"Status: {self.T['status_dis']}",
                                        font=("Segoe UI", 11),
                                        text_color=TEXT_SEC)
        self.status_lbl.pack(side="left", padx=(4, 0))

        # RGB Mode
        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(
            fill="x", padx=20, pady=(0, 16))
        SectionLabel(sb, self.T["rgb_mode"]).pack(anchor="w", padx=20, pady=(0, 4))
        self.rgb_menu = ctk.CTkOptionMenu(
            sb,
            values=["Rainbow", "Solid Red", "Solid Green",
                    "Solid Blue", "White", "Custom Color", "Off"],
            fg_color=BG_ROW, button_color=BORDER,
            button_hover_color=ACCENT,
            dropdown_fg_color=BG_CARD,
            dropdown_hover_color=BG_ROW,
            text_color=TEXT_PRI,
            font=("Segoe UI", 12),
            command=self.change_rgb,
        )
        self.rgb_menu.pack(fill="x", padx=20, pady=(0, 16))

        # LED Speed — max 30 (above this Arduino Rainbow freezes)
        SectionLabel(sb, self.T["led_speed"]).pack(anchor="w", padx=20, pady=(0, 4))
        self.speed_slider = ctk.CTkSlider(
            sb, from_=1, to=30,
            button_color=ACCENT, button_hover_color=ACCENT_DARK,
            progress_color=ACCENT, fg_color=BG_ROW,
            command=self.change_speed,
        )
        self.speed_slider.set(10)
        self.speed_slider.pack(fill="x", padx=20)
        spd_lbl_f = ctk.CTkFrame(sb, fg_color="transparent")
        spd_lbl_f.pack(fill="x", padx=20, pady=(2, 16))
        ctk.CTkLabel(spd_lbl_f, text=self.T["slow"],
                     font=("Segoe UI", 9), text_color=TEXT_DIM).pack(side="left")
        ctk.CTkLabel(spd_lbl_f, text=self.T["fast"],
                     font=("Segoe UI", 9), text_color=TEXT_DIM).pack(side="right")

        # Info card at bottom
        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(
            fill="x", padx=20, pady=(0, 16))
        self.info_card = ctk.CTkFrame(
            sb, fg_color=BG_CARD,
            border_color=BORDER, border_width=1,
            corner_radius=10,
        )
        self.info_card.pack(fill="x", padx=20, pady=(0, 20))
        info_inner = ctk.CTkFrame(self.info_card, fg_color="transparent")
        info_inner.pack(fill="x", padx=14, pady=12)
        ctk.CTkLabel(info_inner, text="ℹ", font=("Segoe UI", 16),
                     text_color=ACCENT).pack(side="left", anchor="n", padx=(0, 8))
        info_txt = ctk.CTkFrame(info_inner, fg_color="transparent")
        info_txt.pack(side="left", fill="x", expand=True)
        self.info_title = ctk.CTkLabel(info_txt, text=self.T["waiting_title"],
                                        font=("Segoe UI", 12, "bold"),
                                        text_color=TEXT_PRI, anchor="w")
        self.info_title.pack(anchor="w")
        self.info_body = ctk.CTkLabel(info_txt, text=self.T["waiting_body"],
                                       font=("Segoe UI", 10),
                                       text_color=TEXT_SEC, anchor="w",
                                       wraplength=160, justify="left")
        self.info_body.pack(anchor="w")

        # Background checkbox
        self.bg_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            sb, text=self.T["run_bg"], variable=self.bg_var,
            font=("Segoe UI", 11), text_color=TEXT_SEC,
            fg_color=ACCENT, hover_color=ACCENT_DARK,
            checkmark_color="#fff",
        ).pack(padx=20, pady=(0, 6), anchor="w")

        # Auto-connect checkbox
        self.autocon_var = ctk.BooleanVar(
            value=self.settings.get("auto_connect", True)
        )
        def _toggle_autocon():
            self.settings["auto_connect"] = self.autocon_var.get()
            save_settings(self.settings)
        ctk.CTkCheckBox(
            sb, text="Auto-connect on startup", variable=self.autocon_var,
            font=("Segoe UI", 11), text_color=TEXT_SEC,
            fg_color=ACCENT, hover_color=ACCENT_DARK,
            checkmark_color="#fff",
            command=_toggle_autocon,
        ).pack(padx=20, pady=(0, 16), anchor="w")

    # ══════════════════════════════════════════════════════════════
    # MAIN CONTENT (tabs)
    # ══════════════════════════════════════════════════════════════
    def _build_main(self):
        main = ctk.CTkFrame(self, fg_color=BG_DARK, corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(0, weight=1)

        # Tab container
        tab_outer = ctk.CTkFrame(main, fg_color=BG_PANEL,
                                  corner_radius=12,
                                  border_color=BORDER, border_width=1)
        tab_outer.grid(row=0, column=0, sticky="nsew",
                       padx=20, pady=20)
        tab_outer.grid_rowconfigure(0, weight=1)
        tab_outer.grid_columnconfigure(0, weight=1)

        self.tabs = ctk.CTkTabview(
            tab_outer,
            fg_color=BG_PANEL,
            segmented_button_fg_color=BG_DARK,
            segmented_button_selected_color=ACCENT,
            segmented_button_selected_hover_color=ACCENT_DARK,
            segmented_button_unselected_color=BG_DARK,
            segmented_button_unselected_hover_color=BG_CARD,
            text_color=TEXT_SEC,
            text_color_disabled=TEXT_DIM,
            border_width=0,
        )
        self.tabs.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        for key in ["tab_buttons", "tab_audio", "tab_shortcuts", "tab_profiles"]:
            self.tabs.add(self.T[key])

        self._build_buttons_tab()
        self._build_audio_tab()
        self._build_shortcuts_tab()
        self._build_profiles_tab()

    # ── Buttons tab ───────────────────────────────────────────────
    def _build_buttons_tab(self):
        tab = self.tabs.tab(self.T["tab_buttons"])
        tab.configure(fg_color="transparent")

        scroll = ctk.CTkScrollableFrame(
            tab, fg_color="transparent",
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=ACCENT,
        )
        scroll.pack(fill="both", expand=True, padx=4, pady=4)
        scroll.grid_columnconfigure(0, weight=1)

        self.btn_configs = {}
        for i in range(10):
            row_bg = BG_ROW if i % 2 == 0 else BG_ROW_ALT
            row = ctk.CTkFrame(scroll, fg_color=row_bg,
                               corner_radius=8, height=48)
            row.pack(fill="x", pady=3, padx=4)
            row.pack_propagate(False)

            inner = ctk.CTkFrame(row, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=12, pady=6)

            # Grid icon dots
            ctk.CTkLabel(inner, text="⋮⋮", font=("Segoe UI", 14),
                         text_color=TEXT_DIM, width=20).pack(side="left", padx=(0, 8))

            # Button label — 1-based numbering
            ctk.CTkLabel(inner, text=f"{self.T['button']} {i+1}",
                         font=("Segoe UI", 13, "bold"),
                         text_color=TEXT_PRI, width=90).pack(side="left")

            # Action dropdown — all app names (SYS:custom shown as "Custom Key")
            combo = StyledCombo(
                inner,
                values=list(self.custom_apps.keys()),
                width=180,
            )
            combo.set("Custom Key")
            combo.pack(side="left", padx=(0, 8))

            # Key entry
            ent = StyledEntry(inner, placeholder_text=self.T["key_ph"])
            ent.pack(side="left", fill="x", expand=True)

            self.btn_configs[f"B{i}"] = (combo, ent)

    # ── Audio tab ─────────────────────────────────────────────────
    def _build_audio_tab(self):
        tab = self.tabs.tab(self.T["tab_audio"])
        tab.configure(fg_color="transparent")

        scroll = ctk.CTkScrollableFrame(
            tab, fg_color="transparent",
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=ACCENT,
        )
        scroll.pack(fill="both", expand=True, padx=4, pady=4)

        self.slider_selectors = {}
        for i in range(5):
            row_bg = BG_ROW if i % 2 == 0 else BG_ROW_ALT
            row = ctk.CTkFrame(scroll, fg_color=row_bg,
                               corner_radius=8, height=52)
            row.pack(fill="x", pady=3, padx=4)
            row.pack_propagate(False)

            inner = ctk.CTkFrame(row, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=12, pady=8)

            ctk.CTkLabel(inner, text="⋮⋮", font=("Segoe UI", 14),
                         text_color=TEXT_DIM, width=20).pack(side="left", padx=(0, 8))

            # Volume icon
            ctk.CTkLabel(inner, text="🔊", font=("Segoe UI", 14),
                         width=24).pack(side="left", padx=(0, 8))

            ctk.CTkLabel(inner, text=f"{self.T['knob']} {i+1}",
                         font=("Segoe UI", 13, "bold"),
                         text_color=TEXT_PRI, width=100).pack(side="left")

            sel = StyledCombo(inner, values=self.audio_presets, width=200)
            sel.set(
                self.audio_presets[i] if i < len(self.audio_presets) else "master"
            )
            sel.pack(side="left", padx=8)
            self.slider_selectors[i] = sel

    # ── Shortcuts tab ─────────────────────────────────────────────
    def _build_shortcuts_tab(self):
        tab = self.tabs.tab(self.T["tab_shortcuts"])
        tab.configure(fg_color="transparent")

        card = ctk.CTkFrame(tab, fg_color=BG_CARD,
                            corner_radius=12,
                            border_color=BORDER, border_width=1)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=30, pady=30)

        ctk.CTkLabel(inner, text=self.T["app_name_lbl"],
                     font=("Segoe UI", 12),
                     text_color=TEXT_SEC).pack(anchor="w", pady=(0, 4))
        self.new_app_name = StyledEntry(
            inner, placeholder_text=self.T["app_name_ph"], height=38
        )
        self.new_app_name.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(inner, text=self.T["app_path_lbl"],
                     font=("Segoe UI", 12),
                     text_color=TEXT_SEC).pack(anchor="w", pady=(0, 4))
        self.new_app_path = StyledEntry(
            inner, placeholder_text=self.T["app_path_ph"], height=38
        )
        self.new_app_path.pack(fill="x", pady=(0, 20))

        StyledButton(inner, text=self.T["add_shortcut"],
                     command=self.save_custom_app,
                     width=180).pack(anchor="w")

    # ── Profiles tab ─────────────────────────────────────────────
    def _build_profiles_tab(self):
        tab = self.tabs.tab(self.T["tab_profiles"])
        tab.configure(fg_color="transparent")

        # Two-column layout: Save | Load
        cols = ctk.CTkFrame(tab, fg_color="transparent")
        cols.pack(fill="both", expand=True, padx=16, pady=16)
        cols.grid_columnconfigure(0, weight=1)
        cols.grid_columnconfigure(1, weight=1)
        cols.grid_rowconfigure(0, weight=1)

        # ── SAVE column ───────────────────────────────────────────
        save_card = ctk.CTkFrame(cols, fg_color=BG_CARD,
                                  corner_radius=12,
                                  border_color=BORDER, border_width=1)
        save_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        save_inner = ctk.CTkFrame(save_card, fg_color="transparent")
        save_inner.pack(fill="both", expand=True, padx=24, pady=24)

        ctk.CTkLabel(save_inner, text=self.T["save_tab"],
                     font=("Segoe UI", 18, "bold"),
                     text_color=TEXT_PRI).pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(save_inner,
                     text="Save the current button & audio configuration",
                     font=("Segoe UI", 11), text_color=TEXT_SEC,
                     wraplength=220, justify="left").pack(anchor="w", pady=(0, 20))

        ctk.CTkLabel(save_inner, text=self.T["profile_name_ph"].replace("...", ""),
                     font=("Segoe UI", 11), text_color=TEXT_SEC).pack(anchor="w", pady=(0, 4))
        self.save_name_entry = StyledEntry(
            save_inner,
            placeholder_text=self.T["profile_name_ph"],
            height=38,
        )
        self.save_name_entry.pack(fill="x", pady=(0, 16))

        self.save_status = ctk.CTkLabel(save_inner, text="",
                                         font=("Segoe UI", 11),
                                         text_color=SUCCESS)
        self.save_status.pack(anchor="w", pady=(0, 8))

        StyledButton(save_inner, text=self.T["save_btn"],
                     command=self.save_profile,
                     height=40).pack(fill="x")

        # ── LOAD column ───────────────────────────────────────────
        load_card = ctk.CTkFrame(cols, fg_color=BG_CARD,
                                  corner_radius=12,
                                  border_color=BORDER, border_width=1)
        load_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        load_inner = ctk.CTkFrame(load_card, fg_color="transparent")
        load_inner.pack(fill="both", expand=True, padx=24, pady=24)

        ctk.CTkLabel(load_inner, text=self.T["load_tab"],
                     font=("Segoe UI", 18, "bold"),
                     text_color=TEXT_PRI).pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(load_inner,
                     text="Select a saved profile to restore settings",
                     font=("Segoe UI", 11), text_color=TEXT_SEC,
                     wraplength=220, justify="left").pack(anchor="w", pady=(0, 20))

        ctk.CTkLabel(load_inner, text="Saved Profiles",
                     font=("Segoe UI", 11), text_color=TEXT_SEC).pack(anchor="w", pady=(0, 4))

        profile_names = list(self.profiles.keys()) or [self.T["no_profiles"]]
        self.load_profile_menu = ctk.CTkOptionMenu(
            load_inner,
            values=profile_names,
            fg_color=BG_ROW, button_color=BORDER,
            button_hover_color=ACCENT,
            dropdown_fg_color=BG_CARD,
            dropdown_hover_color=BG_ROW,
            text_color=TEXT_PRI,
            font=("Segoe UI", 12),
            dynamic_resizing=False,
            height=38,
        )
        self.load_profile_menu.pack(fill="x", pady=(0, 16))

        self.load_status = ctk.CTkLabel(load_inner, text="",
                                         font=("Segoe UI", 11),
                                         text_color=SUCCESS)
        self.load_status.pack(anchor="w", pady=(0, 8))

        btn_row = ctk.CTkFrame(load_inner, fg_color="transparent")
        btn_row.pack(fill="x")
        StyledButton(btn_row, text=self.T["load_btn"],
                     command=self.load_profile,
                     height=40).pack(side="left", fill="x", expand=True, padx=(0, 6))
        DangerButton(btn_row, text=self.T["delete_btn"],
                     command=self.delete_profile,
                     height=40, width=80).pack(side="left")

    # ══════════════════════════════════════════════════════════════
    # Helpers
    # ══════════════════════════════════════════════════════════════
    def get_ports(self):
        ports = [p.device for p in serial.tools.list_ports.comports()]
        return ports or [self.T["no_ports"]]

    def _flash_status(self, label, text, color=SUCCESS, delay=2500):
        label.configure(text=text, text_color=color)
        self.after(delay, lambda: label.configure(text=""))

    def _change_language(self, lang: str):
        self.lang_code = lang
        self.settings["language"] = lang
        save_settings(self.settings)
        self.destroy()
        PultoApp().mainloop()

    def save_custom_app(self):
        name = self.new_app_name.get().strip()
        path = self.new_app_path.get().strip()
        if name and path:
            self.custom_apps[name] = path
            for combo, _ in self.btn_configs.values():
                combo.configure(values=list(self.custom_apps.keys()))
            self.new_app_name.delete(0, "end")
            self.new_app_path.delete(0, "end")

    # ── Profiles ──────────────────────────────────────────────────
    def _collect_profile(self) -> dict:
        buttons = {}
        for key, (combo, ent) in self.btn_configs.items():
            buttons[key] = {"action": combo.get(), "key": ent.get()}
        audio = {str(i): sel.get() for i, sel in self.slider_selectors.items()}
        return {"buttons": buttons, "audio": audio, "custom_apps": self.custom_apps}

    def _apply_profile(self, profile: dict):
        if "custom_apps" in profile:
            self.custom_apps = profile["custom_apps"]
        for key, cfg in profile.get("buttons", {}).items():
            if key in self.btn_configs:
                combo, ent = self.btn_configs[key]
                combo.configure(values=list(self.custom_apps.keys()))
                combo.set(cfg.get("action", "Custom Key"))
                ent.delete(0, "end")
                ent.insert(0, cfg.get("key", ""))
        for i_str, target in profile.get("audio", {}).items():
            i = int(i_str)
            if i in self.slider_selectors:
                self.slider_selectors[i].set(target)

    def _refresh_profile_list(self):
        names = list(self.profiles.keys()) or [self.T["no_profiles"]]
        self.load_profile_menu.configure(values=names)
        if self.profiles:
            self.load_profile_menu.set(list(self.profiles.keys())[0])

    def save_profile(self):
        name = self.save_name_entry.get().strip()
        if not name:
            self._flash_status(self.save_status, "⚠  Enter a profile name", WARNING)
            return
        self.profiles[name] = self._collect_profile()
        save_profiles(self.profiles)
        self.settings["last_profile"] = name
        save_settings(self.settings)
        self._refresh_profile_list()
        self.save_name_entry.delete(0, "end")
        self._flash_status(self.save_status, self.T["saved_ok"])

    def load_profile(self):
        name = self.load_profile_menu.get()
        if name in self.profiles:
            self._apply_profile(self.profiles[name])
            self.settings["last_profile"] = name
            save_settings(self.settings)
            self._flash_status(self.load_status, self.T["loaded_ok"])

    def delete_profile(self):
        name = self.load_profile_menu.get()
        if name in self.profiles:
            del self.profiles[name]
            save_profiles(self.profiles)
            self._refresh_profile_list()
            self._flash_status(self.load_status, self.T["deleted_ok"], DANGER)

    # ── Connection ────────────────────────────────────────────────
    def toggle_connection(self):
        if not self.running:
            try:
                self.ser = serial.Serial(self.port_menu.get(), 115200, timeout=0.01)
                self.running = True
                self.conn_btn.configure(
                    text=f"■  {self.T['stop']}", fg_color=DANGER,
                    hover_color="#c0392b"
                )
                self.status_dot.configure(text_color=SUCCESS)
                self.status_lbl.configure(
                    text=f"Status: {self.T['status_con']}", text_color=SUCCESS
                )
                self.info_title.configure(text="Device connected")
                self.info_body.configure(text="Stream Deck is active and listening")
                threading.Thread(target=self.listen, daemon=True).start()
            except Exception:
                self.status_dot.configure(text_color=DANGER)
                self.status_lbl.configure(
                    text=f"Status: {self.T['status_err']}", text_color=DANGER
                )
        else:
            self.running = False
            if self.ser:
                self.ser.close()
            self.conn_btn.configure(
                text=f"⬡  {self.T['connect']}", fg_color=ACCENT,
                hover_color=ACCENT_DARK
            )
            self.status_dot.configure(text_color=TEXT_DIM)
            self.status_lbl.configure(
                text=f"Status: {self.T['status_dis']}", text_color=TEXT_SEC
            )
            self.info_title.configure(text=self.T["waiting_title"])
            self.info_body.configure(text=self.T["waiting_body"])
            # Restart auto-connect scanning
            self.after(1000, self._try_auto_connect)

    def _try_auto_connect(self):
        """Launches auto-connect only if checkbox is enabled."""
        if self.running:
            return
        if not self.autocon_var.get():
            return  # user disabled auto-connect
        threading.Thread(target=self._auto_connect_worker, daemon=True).start()

    def _auto_connect_worker(self):
        """
        Finds Arduino Pro Micro by USB VID/PID — instant, no sleep needed.
        Pro Micro VIDs: 0x1B4F (SparkFun), 0x2341 (Arduino), 0x1209 (clone)
        Falls back to last known port if VID not found.
        Retries every 3s until connected.
        """
        if self.running:
            return

        # ── Step 1: find by USB hardware ID (most reliable) ──────
        PRO_MICRO_VIDS = {0x1B4F, 0x2341, 0x1209, 0x2A03}
        found_port = None

        last_port = self.settings.get("last_port", "")

        for p in serial.tools.list_ports.comports():
            if p.vid in PRO_MICRO_VIDS:
                found_port = p.device
                break

        # ── Step 2: fallback — try last known port ────────────────
        if not found_port and last_port:
            all_ports = [p.device for p in serial.tools.list_ports.comports()]
            if last_port in all_ports:
                found_port = last_port

        if not found_port:
            self.after(3000, self._try_auto_connect)
            return

        # ── Step 3: open the port ─────────────────────────────────
        try:
            s = serial.Serial(found_port, 115200, timeout=1.0)
            # Pro Micro 32U4: opening serial causes a brief reset
            # wait for sketch to start sending slider data (~30ms intervals)
            time.sleep(1.5)
            s.reset_input_buffer()
            # ── Connected! ────────────────────────────────────────
            self.ser     = s
            self.running = True
            self.settings["last_port"] = found_port
            save_settings(self.settings)
            self.after(0, lambda p=found_port: self._set_connected_ui(p))
            threading.Thread(target=self.listen, daemon=True).start()
        except Exception:
            self.after(3000, self._try_auto_connect)

    def _set_connected_ui(self, port: str):
        self.port_menu.set(port)
        self.conn_btn.configure(
            text=f"■  {self.T['stop']}", fg_color=DANGER, hover_color="#c0392b"
        )
        self.status_dot.configure(text_color=SUCCESS)
        self.status_lbl.configure(
            text=f"Status: {self.T['status_con']}", text_color=SUCCESS
        )
        self.info_title.configure(text="Device connected")
        self.info_body.configure(text=f"Auto-connected · {port}")

    def change_rgb(self, mode):
        if mode == "Custom Color":
            self._open_color_picker()
            return
        if self.ser and self.ser.is_open:
            modes = {
                "Rainbow":     "R",
                "Solid Red":   "F",
                "Solid Green": "G",
                "Solid Blue":  "B",
                "White":       "W",
                "Off":         "O",
            }
            cmd = modes.get(mode)
            if cmd:
                self.ser.write(cmd.encode())

    def _open_color_picker(self):
        """Round color palette popup — pick any color, send RGB to Arduino."""
        popup = ctk.CTkToplevel(self)
        popup.title("Custom Color")
        popup.geometry("320x360")
        popup.configure(fg_color=BG_DARK)
        popup.resizable(False, False)
        popup.grab_set()

        ctk.CTkLabel(popup, text="Pick a color",
                     font=("Segoe UI", 14, "bold"),
                     text_color=TEXT_PRI).pack(pady=(18, 10))

        # Canvas with HSV color wheel
        import math
        SIZE = 220
        canvas = ctk.CTkCanvas(popup, width=SIZE, height=SIZE,
                                bg=BG_DARK, highlightthickness=0)
        canvas.pack()

        # Draw color wheel pixel by pixel using PhotoImage
        img = ctk.CTkImage  # not used, use tkinter PhotoImage directly
        from tkinter import PhotoImage
        photo = PhotoImage(width=SIZE, height=SIZE)
        cx, cy, r = SIZE // 2, SIZE // 2, SIZE // 2 - 4

        pixels = []
        for y in range(SIZE):
            row = []
            for x in range(SIZE):
                dx, dy = x - cx, y - cy
                dist = math.sqrt(dx*dx + dy*dy)
                if dist <= r:
                    hue   = (math.atan2(-dy, dx) / (2 * math.pi)) % 1.0
                    sat   = dist / r
                    # HSV to RGB
                    h = hue * 6
                    i = int(h)
                    f = h - i
                    p, q, t = 1-sat, 1-sat*f, 1-sat*(1-f)
                    rgb_map = [
                        (1, t, p), (q, 1, p), (p, 1, t),
                        (p, q, 1), (t, p, 1), (1, p, q),
                    ]
                    rv, gv, bv = rgb_map[i % 6]
                    row.append(f"#{int(rv*255):02x}{int(gv*255):02x}{int(bv*255):02x}")
                else:
                    row.append(BG_DARK)
            pixels.append("{" + " ".join(row) + "}")
        photo.put(" ".join(pixels))

        canvas.create_image(0, 0, anchor="nw", image=photo)
        canvas._photo = photo  # prevent GC

        # Preview swatch
        swatch = ctk.CTkFrame(popup, width=60, height=24,
                              corner_radius=6, fg_color="#ffffff")
        swatch.pack(pady=8)
        swatch.pack_propagate(False)

        picked = {"hex": "#ffffff", "r": 255, "g": 255, "b": 255}

        def on_click(event):
            dx, dy = event.x - cx, event.y - cy
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > r:
                return
            hue  = (math.atan2(-dy, dx) / (2 * math.pi)) % 1.0
            sat  = dist / r
            h = hue * 6
            i = int(h)
            f = h - i
            p, q, t = 1-sat, 1-sat*f, 1-sat*(1-f)
            rgb_map = [
                (1, t, p), (q, 1, p), (p, 1, t),
                (p, q, 1), (t, p, 1), (1, p, q),
            ]
            rv, gv, bv = rgb_map[i % 6]
            ri, gi, bi = int(rv*255), int(gv*255), int(bv*255)
            hexc = f"#{ri:02x}{gi:02x}{bi:02x}"
            picked.update({"hex": hexc, "r": ri, "g": gi, "b": bi})
            swatch.configure(fg_color=hexc)

        canvas.bind("<Button-1>", on_click)
        canvas.bind("<B1-Motion>", on_click)

        def apply_color():
            if self.ser and self.ser.is_open:
                # Send custom RGB command: "C{r},{g},{b}\n"
                r2, g, b = picked["r"], picked["g"], picked["b"]
                self.ser.write(f"C{r2},{g},{b}\n".encode())
            popup.destroy()

        StyledButton(popup, text="APPLY",
                     command=apply_color, width=120).pack(pady=6)

    def change_speed(self, val):
        if self.ser and self.ser.is_open:
            # Arduino reads raw byte and assigns it to speed directly
            self.ser.write(bytes([int(val)]))

    # ── Action dispatcher ─────────────────────────────────────────
    def _do_action(self, choice: str, custom_key: str):
        """Execute the action for a button press."""
        path = self.custom_apps.get(choice, "")

        if path.startswith("SYS:"):
            cmd = path[4:]
            sys_map = {
                "media_play_pause": lambda: keyboard.press_and_release("play/pause"),
                "media_next":       lambda: keyboard.press_and_release("next track"),
                "media_prev":       lambda: keyboard.press_and_release("previous track"),
                "media_mute":       lambda: keyboard.press_and_release("volume mute"),
                "shutdown":         lambda: os.system("shutdown /s /t 0"),
                "restart":          lambda: os.system("shutdown /r /t 0"),
                "sleep":            lambda: ctypes.windll.powrprof.SetSuspendState(0, 1, 0),
                "lock":             lambda: ctypes.windll.user32.LockWorkStation(),
                "screenshot":       lambda: keyboard.press_and_release("print screen"),
                "custom":           lambda: keyboard.press_and_release(custom_key) if custom_key else None,
            }
            action = sys_map.get(cmd)
            if action:
                action()
        elif path:
            # Expand %USERNAME% and similar env vars in paths
            expanded = os.path.expandvars(path)
            shell_open(expanded)
        elif custom_key:
            keyboard.press_and_release(custom_key)

    # ── Serial listener ───────────────────────────────────────────
    def listen(self):
        while self.running:
            try:
                if self.ser.in_waiting > 0:
                    if self.ser.in_waiting > 100:
                        self.ser.reset_input_buffer()
                    line = (
                        self.ser.readline()
                        .decode("utf-8", errors="ignore")
                        .strip()
                    )
                    if line.startswith("B"):
                        combo, ent = self.btn_configs.get(line, (None, None))
                        if combo is None:
                            continue
                        choice = combo.get()
                        custom_key = ent.get().strip()
                        self._do_action(choice, custom_key)
                    elif line.startswith("S"):
                        vals = line[1:].split("|")
                        for i, v in enumerate(vals):
                            if i >= len(self.slider_selectors):
                                break
                            try:
                                display_name = self.slider_selectors[i].get()
                                # Translate friendly name → exe key
                                exe_key = self.audio_presets_map.get(display_name, display_name)
                                vol = int(v) / 1023.0
                                self.audio_worker.request(i, exe_key, vol)
                            except ValueError:
                                pass
            except Exception:
                pass

    # ── Close / Tray ──────────────────────────────────────────────
    def on_close(self):
        if self.bg_var.get():
            self.withdraw()
            self._show_tray_icon()
        else:
            self._full_exit()

    def _full_exit(self):
        self.running = False
        self.audio_worker.stop()
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.destroy()

    def _show_tray_icon(self):
        threading.Thread(target=self._tray_thread, daemon=True).start()

    def _tray_thread(self):
        user32  = ctypes.windll.user32
        shell32 = ctypes.windll.shell32

        WNDPROC = ctypes.WINFUNCTYPE(
            ctypes.c_long, ctypes.c_void_p,
            ctypes.c_uint, ctypes.c_uint, ctypes.c_long
        )

        def wnd_proc(hwnd, msg, wparam, lparam):
            if msg == WM_APP + 1:
                if lparam in (WM_RBUTTONUP, WM_LBUTTONDBLCLK):
                    self._tray_menu(hwnd)
            return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

        wnd_proc_cb = WNDPROC(wnd_proc)

        class WNDCLASS(ctypes.Structure):
            _fields_ = [
                ("style",         ctypes.c_uint),
                ("lpfnWndProc",   ctypes.c_void_p),
                ("cbClsExtra",    ctypes.c_int),
                ("cbWndExtra",    ctypes.c_int),
                ("hInstance",     ctypes.c_void_p),
                ("hIcon",         ctypes.c_void_p),
                ("hCursor",       ctypes.c_void_p),
                ("hbrBackground", ctypes.c_void_p),
                ("lpszMenuName",  ctypes.c_wchar_p),
                ("lpszClassName", ctypes.c_wchar_p),
            ]

        wc = WNDCLASS()
        wc.lpfnWndProc   = ctypes.cast(wnd_proc_cb, ctypes.c_void_p)
        wc.hInstance     = ctypes.windll.kernel32.GetModuleHandleW(None)
        wc.lpszClassName = "PRO_CTRL_TRAY"
        user32.RegisterClassW(ctypes.byref(wc))
        hwnd = user32.CreateWindowExW(
            0, "PRO_CTRL_TRAY", "Stream Deck",
            0, 0, 0, 0, 0, None, None, wc.hInstance, None
        )
        hicon = user32.LoadIconW(None, ctypes.c_wchar_p(IDI_APPLICATION))
        nid = NOTIFYICONDATA()
        nid.cbSize = ctypes.sizeof(NOTIFYICONDATA)
        nid.hWnd   = hwnd
        nid.uID    = 1
        nid.uFlags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid.uCallbackMessage = WM_APP + 1
        nid.hIcon  = hicon
        nid.szTip  = "Stream Deck"
        shell32.Shell_NotifyIconW(NIM_ADD, ctypes.byref(nid))
        MSG = ctypes.wintypes.MSG
        msg = MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0):
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
        shell32.Shell_NotifyIconW(NIM_DELETE, ctypes.byref(nid))

    def _tray_menu(self, hwnd):
        user32 = ctypes.windll.user32
        PT     = ctypes.wintypes.POINT
        pt     = PT()
        user32.GetCursorPos(ctypes.byref(pt))
        hmenu = user32.CreatePopupMenu()
        user32.AppendMenuW(hmenu, MF_STRING, 1, self.T["open"])
        user32.AppendMenuW(hmenu, MF_STRING, 2, self.T["exit"])
        user32.SetForegroundWindow(hwnd)
        cmd = user32.TrackPopupMenu(
            hmenu, TPM_RETURNCMD | TPM_NONOTIFY,
            pt.x, pt.y, 0, hwnd, None
        )
        user32.DestroyMenu(hmenu)
        if cmd == 1:
            self.after(0, self.deiconify)
            self.after(0, self.lift)
        elif cmd == 2:
            self.after(0, self._full_exit)


if __name__ == "__main__":
    app = PultoApp()
    app.mainloop()