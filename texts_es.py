# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""PocketKode Radio in Spanish: {English text in the code: Spanish}. A text missing here stays English.
The shared parts (activation, removal, updates) are in lang_common.py."""

TEXTS = {
    # lists and counts
    "1 station": "1 emisora", "{n} stations": "{n} emisoras", "1 episode": "1 episodio", "{n} episodes": "{n} episodios",
    "Nothing here yet.": "Aún no hay nada aquí.",
    # home
    "Now playing": "Reproduciendo", "Turn off the screen": "Apagar la pantalla",
    "Keeps playing · press MENU to turn it back on": "Sigue sonando · pulsa MENU para encenderla",
    "What's new · A to update": "Novedades · A para actualizar", "Downloaded · restart to finish": "Descargada · reinicia para terminar",
    "Update available: {v}": "Actualización disponible: {v}",
    "Radio": "Radio", "Stations from around the world": "Emisoras de todo el mundo", 
    "Podcasts": "Pódcasts", "{n} subscribed": "{n} suscritos", "Search, subscribe, download": "Busca, suscríbete, descarga",
    "Settings": "Ajustes", "Your country, podcast region, downloads, language": "Tu país, región de pódcasts, descargas, idioma",
    "About": "Info", "Version {v}": "Versión {v}", "Open": "Abrir", "Quit": "Salir", 
    # full version features (activation screen)
    # radio
    "Favourites": "Favoritas", "Recently played": "Escuchadas recientemente", "Top stations": "Más escuchadas", "Most played worldwide": "Las más escuchadas del mundo",
    "Stations in {country}": "Emisoras de {country}", "Most played first": "Las más escuchadas primero",
    "By country": "Por país", "Choose a country": "Elige un país", "By genre": "Por género", "Pop, rock, news, jazz, talk…": "Pop, rock, noticias, jazz, tertulia…",
    "Search": "Buscar", "Find a station by name": "Busca una emisora por nombre", "Countries": "Países", "Genres": "Géneros", "Search stations": "Buscar emisoras",
    "No favourites yet. Press Y on a station to add it.": "Aún no hay favoritas. Pulsa Y en una emisora para añadirla.",
    "Stations you play appear here.": "Aquí aparecen las emisoras que escuchas.", "No stations found.": "No se encontraron emisoras.",
    "Play": "Escuchar", "Favourite": "Favorita", "Added to favourites": "Añadida a favoritas", "Removed from favourites": "Quitada de favoritas",
    "My country": "Mi país", "{country} set as your country": "{country} es ahora tu país",
    # podcasts
    "My podcasts": "Mis pódcasts", "Downloads": "Descargas",
    "1 episode on this handheld": "1 episodio en esta consola", "{n} episodes on this handheld": "{n} episodios en esta consola",
    "Top podcasts": "Pódcasts más populares", "Charts: {region}": "Listas: {region}", "Find a podcast by name or topic": "Busca un pódcast por nombre o tema",
    "Search podcasts": "Buscar pódcasts",
    "No subscriptions yet. Find a podcast in Search or Top podcasts and press Y to subscribe.":
        "Aún no tienes suscripciones. Busca un pódcast en Buscar o en Pódcasts más populares y pulsa Y para suscribirte.",
    "No podcasts found.": "No se encontraron pódcasts.", "Episodes": "Episodios", "Subscribe": "Suscribirse",
    "Subscribed": "Suscrito", "Unsubscribed": "Suscripción cancelada", "✓ subscribed": "✓ suscrito",
    "{m} min": "{m} min", "✓ played": "✓ escuchado", "{t} left": "quedan {t}", "started": "empezado",
    "Download": "Descargar", "Played": "Escuchado", "Delete download?": "¿Borrar la descarga?",
    "Download cancelled": "Descarga cancelada", "Downloading…": "Descargando…",
    "No downloads yet. In a podcast's episode list, press X to download an episode.":
        "Aún no hay descargas. En la lista de episodios de un pódcast, pulsa X para descargar un episodio.",
    "Delete": "Borrar",
    # now playing
    "Sleep in {t}": "Apagado en {t}", "Nothing playing": "No suena nada", "PODCAST": "PÓDCAST", "RADIO": "RADIO",
    "On air:": "En antena:",
    "Stopped": "Detenido", "Paused": "En pausa", "Loading…": "Cargando…", "Playing": "Sonando", "★ favourite": "★ favorita",
    "Volume {n}%": "Volumen {n}%", "Pause": "Pausa", "Stop": "Detener", "Volume": "Volumen", "Sleep": "Temporizador",
    "Screen off (MENU wakes)": "Pantalla apagada (MENU la enciende)", "Speed": "Velocidad", "Back (keeps playing)": "Atrás (sigue sonando)",
    "MENU: open": "MENU: abrir",
    # confirm, keyboard, loading
    "Yes": "Sí", "No": "No", "Loading": "Cargando", "Something went wrong: {e}": "Algo ha fallado: {e}",
    "Type": "Escribir", "Del": "Borrar", "Space": "Espacio", "Go": "Ir", "Esc": "Salir",
    # settings
    "Not set (choose in Radio > By country)": "Sin elegir (elígelo en Radio > Por país)", "Podcast charts": "Listas de pódcasts",
    "Language": "Idioma", "Change": "Cambiar", "Delete all downloads": "Borrar todas las descargas", "Check for updates": "Buscar actualizaciones",
    "On · a notice when a new version is out": "Sí · un aviso cuando salga una versión nueva", "Off": "No", "Check now": "Comprobar ahora",
    "You have version {v}": "Tienes la versión {v}", 
    "Delete all downloads?": "¿Borrar todas las descargas?",
    "Downloaded episodes are removed from the handheld. Your subscriptions and listening progress are kept.":
        "Los episodios descargados se borran de la consola. Tus suscripciones y tu progreso se conservan.",
    # podcast chart regions
    "United States": "Estados Unidos", "United Kingdom": "Reino Unido", "Canada": "Canadá", "Australia": "Australia", "India": "India",
    "Japan": "Japón", "Germany": "Alemania", "France": "Francia", "Spain": "España", "Brazil": "Brasil", "Mexico": "México",
    "Italy": "Italia", "Netherlands": "Países Bajos", "Sweden": "Suecia",
    # about
    "Internet radio and podcasts for muOS handhelds. Stations come from the community Radio Browser directory "
    "(radio-browser.info). Podcast search and charts come from Apple's public podcast directory, and episodes from "
    "each show's own feed. Nothing is recorded or re-shared.":
        "Radio por internet y pódcasts para consolas muOS. Las emisoras vienen del directorio comunitario Radio Browser "
        "(radio-browser.info). La búsqueda y las listas de pódcasts vienen del directorio público de Apple, y los episodios "
        "del feed de cada programa. No se graba ni se redistribuye nada.",
    "Privacy": "Privacidad", "Scroll": "Desplazar",
    # privacy
    "PocketKode Radio never reads or sends your files, and doesn't record anything.":
        "PocketKode Radio nunca lee ni envía tus archivos, y no graba nada.",
    "Stations come from Radio Browser, podcasts from Apple's podcast directory, and the sound from each station or show "
    "itself. Your searches go to those services. When you play a station, Radio Browser is told that the station was "
    "played (an anonymous count that keeps its Top list up to date).":
        "Las emisoras vienen de Radio Browser, los pódcasts del directorio de Apple, y el sonido de cada emisora o "
        "programa. Tus búsquedas van a esos servicios. Cuando escuchas una emisora, se avisa a Radio Browser de que se "
        "ha escuchado (un recuento anónimo que mantiene al día su lista de las más escuchadas).",
    "Your favourites, subscriptions and history stay on the handheld. No ads, no analytics, no tracking.":
        "Tus favoritas, suscripciones e historial se quedan en la consola. Sin anuncios, sin analíticas, sin rastreo.",
    # notices
    "Updated": "Actualizada", "Update undone": "Actualización deshecha", 
    "PocketKode Radio is now version {v}. Your stations, podcasts and settings were kept.": "PocketKode Radio ya es la versión {v}. Tus emisoras, pódcasts y ajustes se han conservado.",
    "Version {bad} didn't start, so PocketKode Radio went back to {v}. Please email feedback@pocketkode.com.":
        "La versión {bad} no arrancó, así que PocketKode Radio volvió a la {v}. Escribe a feedback@pocketkode.com.",
    # messages made in net.py, player.py, podcasts.py, radio.py
    "The connection timed out. Check Wi-Fi and try again.": "Se agotó el tiempo de conexión. Comprueba el Wi-Fi e inténtalo de nuevo.",
    "That feed is too large to load.": "Ese feed es demasiado grande para cargarlo.",
    "The server sent something the app couldn't read.": "El servidor envió algo que la app no pudo leer.",
    "Radio directory unavailable.": "El directorio de radio no está disponible.",
    "mpv isn't installed on this system.": "mpv no está instalado en este sistema.",
    "This couldn't be played. The station or episode may be offline.": "No se pudo reproducir. La emisora o el episodio puede estar desconectado.",
    "This podcast's feed couldn't be read.": "No se pudo leer el feed de este pódcast.",
    # full version free forever (2026-09-28)
    "Free and open source (MIT License). See LICENSE in the app folder.": "Gratis y de código abierto (licencia MIT). Consulta LICENSE en la carpeta de la app.",
    "For updates it reads the latest release on GitHub (you can turn this off in Settings). It sends nothing about you or the handheld.": "Para las actualizaciones consulta la última versión publicada en GitHub (puedes desactivarlo en Ajustes). No envía nada sobre ti ni sobre la consola.",
}

PATTERNS = [
    (r"The server said no \(error (\d+)\)\. Try again later\.", r"El servidor lo rechazó (error \1). Inténtalo más tarde."),
    (r"Connection problem: (.*)", r"Problema de conexión: \1"),
    (r"Couldn't start the player: (.*)", r"No se pudo iniciar el reproductor: \1"),
]
