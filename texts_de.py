# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""PocketKode Radio in German: {English text in the code: German}. A text missing here stays English.
The shared parts (activation, removal, updates) are in lang_common.py."""

TEXTS = {
    # lists and counts
    "1 station": "1 Sender", "{n} stations": "{n} Sender", "1 episode": "1 Folge", "{n} episodes": "{n} Folgen",
    "Nothing here yet.": "Hier ist noch nichts.",
    # home
    "Now playing": "Läuft gerade", "Turn off the screen": "Display ausschalten",
    "Keeps playing · press MENU to turn it back on": "Spielt weiter · MENU schaltet es wieder ein",
    "What's new · A to update": "Neu · A zum Aktualisieren", "Downloaded · restart to finish": "Heruntergeladen · zum Abschluss neu starten",
    "Update available: {v}": "Update verfügbar: {v}",
    "Radio": "Radio", "Stations from around the world": "Sender aus aller Welt", 
    "Podcasts": "Podcasts", "{n} subscribed": "{n} abonniert", "Search, subscribe, download": "Suchen, abonnieren, herunterladen",
    "Settings": "Einstellungen", "Your country, podcast region, downloads, language": "Dein Land, Podcast-Region, Downloads, Sprache",
    "About": "Info", "Version {v}": "Version {v}", "Open": "Öffnen", "Quit": "Beenden", 
    # full version features (activation screen)
    # radio
    "Favourites": "Favoriten", "Recently played": "Zuletzt gehört", "Top stations": "Top-Sender", "Most played worldwide": "Weltweit am meisten gehört",
    "Stations in {country}": "Sender in {country}", "Most played first": "Meistgehörte zuerst",
    "By country": "Nach Land", "Choose a country": "Land wählen", "By genre": "Nach Genre", "Pop, rock, news, jazz, talk…": "Pop, Rock, Nachrichten, Jazz, Talk…",
    "Search": "Suche", "Find a station by name": "Sender nach Namen suchen", "Countries": "Länder", "Genres": "Genres", "Search stations": "Sender suchen",
    "No favourites yet. Press Y on a station to add it.": "Noch keine Favoriten. Drück Y auf einem Sender, um ihn hinzuzufügen.",
    "Stations you play appear here.": "Hier erscheinen die Sender, die du hörst.", "No stations found.": "Keine Sender gefunden.",
    "Play": "Abspielen", "Favourite": "Favorit", "Added to favourites": "Zu Favoriten hinzugefügt", "Removed from favourites": "Aus Favoriten entfernt",
    "My country": "Mein Land", "{country} set as your country": "{country} ist jetzt dein Land",
    # podcasts
    "My podcasts": "Meine Podcasts", "Downloads": "Downloads",
    "1 episode on this handheld": "1 Folge auf diesem Handheld", "{n} episodes on this handheld": "{n} Folgen auf diesem Handheld",
    "Top podcasts": "Top-Podcasts", "Charts: {region}": "Charts: {region}", "Find a podcast by name or topic": "Podcast nach Name oder Thema suchen",
    "Search podcasts": "Podcasts suchen",
    "No subscriptions yet. Find a podcast in Search or Top podcasts and press Y to subscribe.":
        "Noch keine Abos. Finde einen Podcast unter Suche oder Top-Podcasts und drück Y zum Abonnieren.",
    "No podcasts found.": "Keine Podcasts gefunden.", "Episodes": "Folgen", "Subscribe": "Abonnieren",
    "Subscribed": "Abonniert", "Unsubscribed": "Abo beendet", "✓ subscribed": "✓ abonniert",
    "{m} min": "{m} Min.", "✓ played": "✓ gehört", "{t} left": "noch {t}", "started": "angefangen",
    "Download": "Herunterladen", "Played": "Gehört", "Delete download?": "Download löschen?",
    "Download cancelled": "Download abgebrochen", "Downloading…": "Lade herunter…",
    "No downloads yet. In a podcast's episode list, press X to download an episode.":
        "Noch keine Downloads. Drück in der Folgenliste eines Podcasts X, um eine Folge herunterzuladen.",
    "Delete": "Löschen",
    # now playing
    "Sleep in {t}": "Aus in {t}", "Nothing playing": "Nichts läuft", "PODCAST": "PODCAST", "RADIO": "RADIO",
    "On air:": "Läuft gerade:",
    "Stopped": "Gestoppt", "Paused": "Pausiert", "Loading…": "Lädt…", "Playing": "Läuft", "★ favourite": "★ Favorit",
    "Volume {n}%": "Lautstärke {n} %", "Pause": "Pause", "Stop": "Stopp", "Volume": "Lautstärke", "Sleep": "Sleep-Timer",
    "Screen off (MENU wakes)": "Display aus (MENU weckt)", "Speed": "Tempo", "Back (keeps playing)": "Zurück (spielt weiter)",
    "MENU: open": "MENU: öffnen",
    # confirm, keyboard, loading
    "Yes": "Ja", "No": "Nein", "Loading": "Lädt", "Something went wrong: {e}": "Etwas ist schiefgelaufen: {e}",
    "Type": "Tippen", "Del": "Entf", "Space": "Leer", "Go": "Los", "Esc": "Abbr.",
    # settings
    "Not set (choose in Radio > By country)": "Nicht festgelegt (unter Radio > Nach Land wählen)", "Podcast charts": "Podcast-Charts",
    "Language": "Sprache", "Change": "Ändern", "Delete all downloads": "Alle Downloads löschen", "Check for updates": "Nach Updates suchen",
    "On · a notice when a new version is out": "An · Hinweis, wenn eine neue Version erscheint", "Off": "Aus", "Check now": "Jetzt prüfen",
    "You have version {v}": "Du hast Version {v}", 
    "Delete all downloads?": "Alle Downloads löschen?",
    "Downloaded episodes are removed from the handheld. Your subscriptions and listening progress are kept.":
        "Heruntergeladene Folgen werden vom Handheld gelöscht. Deine Abos und dein Hörfortschritt bleiben erhalten.",
    # podcast chart regions
    "United States": "USA", "United Kingdom": "Vereinigtes Königreich", "Canada": "Kanada", "Australia": "Australien", "India": "Indien",
    "Japan": "Japan", "Germany": "Deutschland", "France": "Frankreich", "Spain": "Spanien", "Brazil": "Brasilien", "Mexico": "Mexiko",
    "Italy": "Italien", "Netherlands": "Niederlande", "Sweden": "Schweden",
    # about
    "Internet radio and podcasts for muOS handhelds. Stations come from the community Radio Browser directory "
    "(radio-browser.info). Podcast search and charts come from Apple's public podcast directory, and episodes from "
    "each show's own feed. Nothing is recorded or re-shared.":
        "Internetradio und Podcasts für muOS-Handhelds. Die Sender stammen aus dem Community-Verzeichnis Radio Browser "
        "(radio-browser.info). Podcast-Suche und Charts kommen aus Apples öffentlichem Podcast-Verzeichnis, die Folgen "
        "aus dem Feed der jeweiligen Sendung. Nichts wird aufgezeichnet oder weiterverbreitet.",
    "Privacy": "Datenschutz", "Scroll": "Scrollen",
    # privacy
    "PocketKode Radio never reads or sends your files, and doesn't record anything.":
        "PocketKode Radio liest oder sendet nie deine Dateien und zeichnet nichts auf.",
    "Stations come from Radio Browser, podcasts from Apple's podcast directory, and the sound from each station or show "
    "itself. Your searches go to those services. When you play a station, Radio Browser is told that the station was "
    "played (an anonymous count that keeps its Top list up to date).":
        "Sender kommen von Radio Browser, Podcasts aus Apples Podcast-Verzeichnis und der Ton vom jeweiligen Sender oder "
        "der Sendung selbst. Deine Suchen gehen an diese Dienste. Wenn du einen Sender hörst, erfährt Radio Browser, "
        "dass er gehört wurde (eine anonyme Zählung, die die Top-Liste aktuell hält).",
    "Your favourites, subscriptions and history stay on the handheld. No ads, no analytics, no tracking.":
        "Deine Favoriten, Abos und dein Verlauf bleiben auf dem Handheld. Keine Werbung, keine Analyse, kein Tracking.",
    # notices
    "Updated": "Aktualisiert", "Update undone": "Update rückgängig gemacht", 
    "PocketKode Radio is now version {v}. Your stations, podcasts and settings were kept.": "PocketKode Radio ist jetzt Version {v}. Deine Sender, Podcasts und Einstellungen blieben erhalten.",
    "Version {bad} didn't start, so PocketKode Radio went back to {v}. Please email feedback@pocketkode.com.":
        "Version {bad} ist nicht gestartet, daher ist PocketKode Radio zu {v} zurückgekehrt. Bitte schreib an feedback@pocketkode.com.",
    # messages made in net.py, player.py, podcasts.py, radio.py
    "The connection timed out. Check Wi-Fi and try again.": "Zeitüberschreitung der Verbindung. Prüfe das WLAN und versuch es erneut.",
    "That feed is too large to load.": "Dieser Feed ist zu groß zum Laden.",
    "The server sent something the app couldn't read.": "Der Server hat etwas gesendet, das die App nicht lesen konnte.",
    "Radio directory unavailable.": "Senderverzeichnis nicht erreichbar.",
    "mpv isn't installed on this system.": "mpv ist auf diesem System nicht installiert.",
    "This couldn't be played. The station or episode may be offline.": "Das ließ sich nicht abspielen. Der Sender oder die Folge ist vielleicht offline.",
    "This podcast's feed couldn't be read.": "Der Feed dieses Podcasts konnte nicht gelesen werden.",
    # full version free forever (2026-09-28)
    "Free and open source (MIT License). See LICENSE in the app folder.": "Kostenlos und Open Source (MIT-Lizenz). Siehe LICENSE im App-Ordner.",
    "For updates it reads the latest release on GitHub (you can turn this off in Settings). It sends nothing about you or the handheld.": "Für Updates liest es die neueste Version auf GitHub (das kannst du in den Einstellungen ausschalten). Es sendet nichts über dich oder das Handheld.",
}

PATTERNS = [
    (r"The server said no \(error (\d+)\)\. Try again later\.", r"Der Server hat abgelehnt (Fehler \1). Versuch es später erneut."),
    (r"Connection problem: (.*)", r"Verbindungsproblem: \1"),
    (r"Couldn't start the player: (.*)", r"Der Player konnte nicht gestartet werden: \1"),
]
