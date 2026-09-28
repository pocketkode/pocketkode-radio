# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""PocketKode Radio in French: {English text in the code: French}. A text missing here stays English.
The shared parts (activation, removal, updates) are in lang_common.py."""

TEXTS = {
    # lists and counts
    "1 station": "1 station", "{n} stations": "{n} stations", "1 episode": "1 épisode", "{n} episodes": "{n} épisodes",
    "Nothing here yet.": "Rien ici pour l’instant.",
    # home
    "Now playing": "En cours de lecture", "Turn off the screen": "Éteindre l’écran",
    "Keeps playing · press MENU to turn it back on": "La lecture continue · MENU pour le rallumer",
    "What's new · A to update": "Nouveautés · A pour mettre à jour", "Downloaded · restart to finish": "Téléchargée · redémarrez pour terminer",
    "Update available: {v}": "Mise à jour disponible : {v}",
    "Radio": "Radio", "Stations from around the world": "Des stations du monde entier",
    "Podcasts": "Podcasts", "{n} subscribed": "{n} abonnements", "Search, subscribe, download": "Chercher, s’abonner, télécharger",
    "Settings": "Réglages", "Your country, podcast region, downloads, language": "Votre pays, région des podcasts, téléchargements, langue",
    "About": "Infos", "Version {v}": "Version {v}", "Open": "Ouvrir", "Quit": "Quitter",
    # radio
    "Favourites": "Favoris", "Recently played": "Écoutées récemment", "Top stations": "Stations populaires", "Most played worldwide": "Les plus écoutées au monde",
    "Stations in {country}": "Stations : {country}", "Most played first": "Les plus écoutées d’abord",
    "By country": "Par pays", "Choose a country": "Choisissez un pays", "By genre": "Par genre", "Pop, rock, news, jazz, talk…": "Pop, rock, info, jazz, talk…",
    "Search": "Rechercher", "Find a station by name": "Trouver une station par son nom", "Countries": "Pays", "Genres": "Genres", "Search stations": "Rechercher des stations",
    "No favourites yet. Press Y on a station to add it.": "Pas encore de favoris. Appuyez sur Y sur une station pour l’ajouter.",
    "Stations you play appear here.": "Les stations que vous écoutez apparaissent ici.", "No stations found.": "Aucune station trouvée.",
    "Play": "Écouter", "Favourite": "Favori", "Added to favourites": "Ajoutée aux favoris", "Removed from favourites": "Retirée des favoris",
    "My country": "Mon pays", "{country} set as your country": "{country} est maintenant votre pays",
    # podcasts
    "My podcasts": "Mes podcasts", "Downloads": "Téléchargements",
    "1 episode on this handheld": "1 épisode sur cette console", "{n} episodes on this handheld": "{n} épisodes sur cette console",
    "Top podcasts": "Podcasts populaires", "Charts: {region}": "Classement : {region}", "Find a podcast by name or topic": "Trouver un podcast par nom ou sujet",
    "Search podcasts": "Rechercher des podcasts",
    "No subscriptions yet. Find a podcast in Search or Top podcasts and press Y to subscribe.":
        "Pas encore d’abonnement. Trouvez un podcast dans Rechercher ou Podcasts populaires et appuyez sur Y pour vous abonner.",
    "No podcasts found.": "Aucun podcast trouvé.", "Episodes": "Épisodes", "Subscribe": "S’abonner",
    "Subscribed": "Abonné", "Unsubscribed": "Désabonné", "✓ subscribed": "✓ abonné",
    "{m} min": "{m} min", "✓ played": "✓ écouté", "{t} left": "{t} restant", "started": "commencé",
    "Download": "Télécharger", "Played": "Écouté", "Delete download?": "Supprimer le téléchargement ?",
    "Download cancelled": "Téléchargement annulé", "Downloading…": "Téléchargement…",
    "No downloads yet. In a podcast's episode list, press X to download an episode.":
        "Pas encore de téléchargement. Dans la liste des épisodes d’un podcast, appuyez sur X pour télécharger un épisode.",
    "Delete": "Supprimer",
    # now playing
    "Sleep in {t}": "Arrêt dans {t}", "Nothing playing": "Rien en lecture", "PODCAST": "PODCAST", "RADIO": "RADIO",
    "On air:": "À l’antenne :",
    "Stopped": "Arrêté", "Paused": "En pause", "Loading…": "Chargement…", "Playing": "Lecture", "★ favourite": "★ favori",
    "Volume {n}%": "Volume {n} %", "Pause": "Pause", "Stop": "Arrêter", "Volume": "Volume", "Sleep": "Minuterie",
    "Screen off (MENU wakes)": "Écran éteint (MENU le rallume)", "Speed": "Vitesse", "Back (keeps playing)": "Retour (la lecture continue)",
    "MENU: open": "MENU : ouvrir",
    # confirm, keyboard, loading
    "Yes": "Oui", "No": "Non", "Loading": "Chargement", "Something went wrong: {e}": "Une erreur s’est produite : {e}",
    "Type": "Saisir", "Del": "Eff.", "Space": "Esp.", "Go": "OK", "Esc": "Ann.",
    # settings
    "Not set (choose in Radio > By country)": "Non défini (à choisir dans Radio > Par pays)", "Podcast charts": "Classement des podcasts",
    "Language": "Langue", "Change": "Changer", "Delete all downloads": "Supprimer tous les téléchargements", "Check for updates": "Vérifier les mises à jour",
    "On · a notice when a new version is out": "Oui · un avis quand une nouvelle version sort", "Off": "Non", "Check now": "Vérifier maintenant",
    "You have version {v}": "Vous avez la version {v}",
    "Delete all downloads?": "Supprimer tous les téléchargements ?",
    "Downloaded episodes are removed from the handheld. Your subscriptions and listening progress are kept.":
        "Les épisodes téléchargés sont supprimés de la console. Vos abonnements et votre progression sont conservés.",
    # podcast chart regions
    "United States": "États-Unis", "United Kingdom": "Royaume-Uni", "Canada": "Canada", "Australia": "Australie", "India": "Inde",
    "Japan": "Japon", "Germany": "Allemagne", "France": "France", "Spain": "Espagne", "Brazil": "Brésil", "Mexico": "Mexique",
    "Italy": "Italie", "Netherlands": "Pays-Bas", "Sweden": "Suède",
    # about
    "Internet radio and podcasts for muOS handhelds. Stations come from the community Radio Browser directory "
    "(radio-browser.info). Podcast search and charts come from Apple's public podcast directory, and episodes from "
    "each show's own feed. Nothing is recorded or re-shared.":
        "Radio en ligne et podcasts pour les consoles muOS. Les stations viennent de l’annuaire communautaire Radio "
        "Browser (radio-browser.info). La recherche et les classements de podcasts viennent de l’annuaire public "
        "d’Apple, et les épisodes du flux de chaque émission. Rien n’est enregistré ni rediffusé.",
    "Privacy": "Confidentialité", "Scroll": "Défiler",
    # privacy
    "PocketKode Radio never reads or sends your files, and doesn't record anything.":
        "PocketKode Radio ne lit ni n’envoie jamais vos fichiers, et n’enregistre rien.",
    "Stations come from Radio Browser, podcasts from Apple's podcast directory, and the sound from each station or show "
    "itself. Your searches go to those services. When you play a station, Radio Browser is told that the station was "
    "played (an anonymous count that keeps its Top list up to date).":
        "Les stations viennent de Radio Browser, les podcasts de l’annuaire d’Apple, et le son de chaque station ou "
        "émission. Vos recherches vont à ces services. Quand vous écoutez une station, Radio Browser est informé "
        "qu’elle a été écoutée (un comptage anonyme qui tient à jour son classement).",
    "Your favourites, subscriptions and history stay on the handheld. No ads, no analytics, no tracking.":
        "Vos favoris, abonnements et historique restent sur la console. Pas de publicité, pas de statistiques, pas de pistage.",
    # notices
    "Updated": "Mise à jour effectuée", "Update undone": "Mise à jour annulée",
    "PocketKode Radio is now version {v}. Your stations, podcasts and settings were kept.": "PocketKode Radio est maintenant en version {v}. Vos stations, podcasts et réglages ont été conservés.",
    "Version {bad} didn't start, so PocketKode Radio went back to {v}. Please email feedback@pocketkode.com.":
        "La version {bad} n’a pas démarré, PocketKode Radio est donc revenue à la {v}. Écrivez à feedback@pocketkode.com.",
    # messages made in net.py, player.py, podcasts.py, radio.py
    "The connection timed out. Check Wi-Fi and try again.": "La connexion a expiré. Vérifiez le Wi-Fi et réessayez.",
    "That feed is too large to load.": "Ce flux est trop volumineux pour être chargé.",
    "The server sent something the app couldn't read.": "Le serveur a envoyé quelque chose que l’app n’a pas pu lire.",
    "Radio directory unavailable.": "Annuaire des radios indisponible.",
    "mpv isn't installed on this system.": "mpv n’est pas installé sur ce système.",
    "This couldn't be played. The station or episode may be offline.": "Lecture impossible. La station ou l’épisode est peut-être hors ligne.",
    "This podcast's feed couldn't be read.": "Le flux de ce podcast n’a pas pu être lu.",
    # about and privacy
    "Free and open source (MIT License). See LICENSE in the app folder.": "Gratuite et open source (licence MIT). Voir LICENSE dans le dossier de l’app.",
    "For updates it reads the latest release on GitHub (you can turn this off in Settings). It sends nothing about you or the handheld.": "Pour les mises à jour, elle lit la dernière version publiée sur GitHub (vous pouvez désactiver cela dans Réglages). Elle n’envoie rien sur vous ni sur la console.",
}

PATTERNS = [
    (r"The server said no \(error (\d+)\)\. Try again later\.", r"Le serveur a refusé (erreur \1). Réessayez plus tard."),
    (r"Connection problem: (.*)", r"Problème de connexion : \1"),
    (r"Couldn't start the player: (.*)", r"Impossible de démarrer le lecteur : \1"),
]
