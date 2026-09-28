# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""The app's language: English, 日本語, Español, Français, Deutsch, Nederlands, Русский, 简体中文 or 한국어.

The choice ("auto" or a language code) is kept in data/language. Auto follows muOS's own language setting
(Configuration > Language); a language the app doesn't have means English.
Texts are written in English in the code: _("Text {n}", n=3) returns the translation when there is one.
tr() does the same for messages made elsewhere (updates, network errors), matching whole sentences or patterns.
Translations: the shared parts are in lang_common.py, the app's own texts in texts_<code>.py (loaded when needed).
A text missing from a translation stays English.
"""
import importlib
import os
import re
import time

MUOS_LANGUAGE = os.environ.get("PK_MUOS_LANGUAGE", "/opt/muos/config/settings/general/language")
LANGS = ("en", "ja", "es", "fr", "de", "nl", "ru", "zh", "ko")
CHOICES = ("auto",) + LANGS
NAMES = {"en": "English", "ja": "日本語", "es": "Español", "fr": "Français", "de": "Deutsch", "nl": "Nederlands",
         "ru": "Русский", "zh": "简体中文", "ko": "한국어"}
# muOS's language names (the files in /opt/muos/share/language) → ours
_MUOS = {"japanese": "ja", "spanish": "es", "french": "fr", "german": "de", "dutch": "nl", "russian": "ru",
         "chinese (simplified)": "zh", "korean": "ko"}
# the font each language is drawn with (fonts/, SIL Open Font License)
FONTS = {"zh": "NotoSansSC-Regular.otf", "ko": "NotoSansKR-Regular.otf"}
DEFAULT_FONT = "NotoSansJP-Regular.otf"  # Japanese, and the accented and Cyrillic letters of es/fr/de/nl/ru
_DATES = {"en": "%d %b %Y", "ja": "%Y/%m/%d", "zh": "%Y-%m-%d", "ko": "%Y. %m. %d.", "de": "%d.%m.%Y",
          "ru": "%d.%m.%Y", "nl": "%d-%m-%Y", "es": "%d/%m/%Y", "fr": "%d/%m/%Y"}

_state = {"choice": "auto", "lang": "en", "file": None, "texts": {}, "patterns": [], "bad": set(), "loaded": None}


def muos_language():
    """Our code for muOS's language setting, or 'en'."""
    try:
        with open(MUOS_LANGUAGE, encoding="utf-8") as f:
            return _MUOS.get(f.read().strip().lower(), "en")
    except OSError:
        return "en"


def font_file(code=None):
    return FONTS.get(code or _state["lang"], DEFAULT_FONT)


def setup(app_dir):
    """Load the saved choice (data/language in the app folder)."""
    _state["file"] = os.path.join(app_dir, "data", "language")
    try:
        with open(_state["file"], encoding="utf-8") as f:
            choice = f.read().strip()
        if choice in CHOICES:
            _state["choice"] = choice
    except OSError:
        pass
    _apply()


def _apply():
    c = _state["choice"]
    code = muos_language() if c == "auto" else c
    if code in _state["bad"]:
        code = "en"
    _state["lang"] = code
    if _state["loaded"] != code:
        _load(code)


def _load(code):
    texts, patterns = {}, []
    if code != "en":
        import lang_common
        texts.update(lang_common.COMMON.get(code, {}))
        patterns += lang_common.PATTERNS.get(code, [])
        try:
            mod = importlib.import_module("texts_" + code)
            texts.update(getattr(mod, "TEXTS", {}))
            patterns = list(getattr(mod, "PATTERNS", [])) + patterns
        except ImportError:
            pass
    _state["texts"] = texts
    _state["patterns"] = [(re.compile(p), r) for p, r in patterns]
    _state["loaded"] = code


def unavailable(code=None):
    """The font for this language couldn't be loaded: use English instead."""
    _state["bad"].add(code or _state["lang"])
    _apply()


def current():
    return _state["lang"]


def choice():
    return _state["choice"]


def set_choice(c):
    if c not in CHOICES:
        return _state["choice"]
    _state["choice"] = c
    _apply()
    try:
        os.makedirs(os.path.dirname(_state["file"]), exist_ok=True)
        with open(_state["file"], "w", encoding="utf-8") as f:
            f.write(c + "\n")
    except (OSError, TypeError):
        pass
    return c


def cycle(step=1):
    """Auto → English → 日本語 → … → 한국어 → Auto (step -1 goes back); saved for the next start."""
    return set_choice(CHOICES[(CHOICES.index(_state["choice"]) + step) % len(CHOICES)])


def label():
    """'Auto (English)', 'English', '日本語'…, for the settings line."""
    c = _state["choice"]
    return f"{_('Auto')} ({NAMES[_state['lang']]})" if c == "auto" else NAMES[c]


def date(ts):
    """A date in the language's usual form (the handheld's time zone)."""
    return time.strftime(_DATES.get(_state["lang"], _DATES["en"]), time.localtime(ts))


def _(text, **kw):
    if _state["lang"] != "en":
        text = _state["texts"].get(text, text)
    return text.format(**kw) if kw else text


def tr(msg):
    """A message made elsewhere (in English), in the app's language; unknown ones stay English."""
    if not msg or _state["lang"] == "en":
        return msg
    if msg in _state["texts"]:
        return _state["texts"][msg]
    for rx, out in _state["patterns"]:
        m = rx.fullmatch(msg)
        if m:  # the parts that were matched may be messages themselves (e.g. an error inside an error)
            return re.sub(r"\\(\d)", lambda g: tr(m.group(int(g.group(1))) or ""), out)
    return msg
