# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""PocketKode Radio in Russian: {English text in the code: Russian}. A text missing here stays English.
The shared parts (activation, removal, updates) are in lang_common.py. Counts use forms that fit any number."""

TEXTS = {
    # lists and counts
    "1 station": "1 станция", "{n} stations": "станций: {n}", "1 episode": "1 выпуск", "{n} episodes": "выпусков: {n}",
    "Nothing here yet.": "Здесь пока ничего нет.",
    # home
    "Now playing": "Сейчас играет", "Turn off the screen": "Выключить экран",
    "Keeps playing · press MENU to turn it back on": "Продолжает играть · MENU включит экран",
    "What's new · A to update": "Что нового · A — обновить", "Downloaded · restart to finish": "Скачано · перезапустите для завершения",
    "Update available: {v}": "Доступно обновление: {v}",
    "Radio": "Радио", "Stations from around the world": "Станции со всего мира", 
    "Podcasts": "Подкасты", "{n} subscribed": "подписок: {n}", "Search, subscribe, download": "Поиск, подписка, загрузка",
    "Settings": "Настройки", "Your country, podcast region, downloads, language": "Ваша страна, регион подкастов, загрузки, язык",
    "About": "О программе", "Version {v}": "Версия {v}", "Open": "Открыть", "Quit": "Выход", 
    # full version features (activation screen)
    # radio
    "Favourites": "Избранное", "Recently played": "Недавно прослушанные", "Top stations": "Популярные станции", "Most played worldwide": "Самые популярные в мире",
    "Stations in {country}": "Станции: {country}", "Most played first": "Сначала самые популярные",
    "By country": "По странам", "Choose a country": "Выберите страну", "By genre": "По жанрам", "Pop, rock, news, jazz, talk…": "Поп, рок, новости, джаз, разговорные…",
    "Search": "Поиск", "Find a station by name": "Найти станцию по названию", "Countries": "Страны", "Genres": "Жанры", "Search stations": "Поиск станций",
    "No favourites yet. Press Y on a station to add it.": "Избранного пока нет. Нажмите Y на станции, чтобы добавить её.",
    "Stations you play appear here.": "Здесь появятся станции, которые вы слушаете.", "No stations found.": "Станции не найдены.",
    "Play": "Слушать", "Favourite": "В избранное", "Added to favourites": "Добавлено в избранное", "Removed from favourites": "Убрано из избранного",
    "My country": "Моя страна", "{country} set as your country": "{country} — теперь ваша страна",
    # podcasts
    "My podcasts": "Мои подкасты", "Downloads": "Загрузки",
    "1 episode on this handheld": "1 выпуск на этой консоли", "{n} episodes on this handheld": "Выпусков на этой консоли: {n}",
    "Top podcasts": "Популярные подкасты", "Charts: {region}": "Чарты: {region}", "Find a podcast by name or topic": "Найти подкаст по названию или теме",
    "Search podcasts": "Поиск подкастов",
    "No subscriptions yet. Find a podcast in Search or Top podcasts and press Y to subscribe.":
        "Подписок пока нет. Найдите подкаст в «Поиске» или «Популярных подкастах» и нажмите Y, чтобы подписаться.",
    "No podcasts found.": "Подкасты не найдены.", "Episodes": "Выпуски", "Subscribe": "Подписаться",
    "Subscribed": "Вы подписались", "Unsubscribed": "Подписка отменена", "✓ subscribed": "✓ подписка",
    "{m} min": "{m} мин", "✓ played": "✓ прослушано", "{t} left": "осталось {t}", "started": "начато",
    "Download": "Скачать", "Played": "Прослушано", "Delete download?": "Удалить загрузку?",
    "Download cancelled": "Загрузка отменена", "Downloading…": "Загрузка…",
    "No downloads yet. In a podcast's episode list, press X to download an episode.":
        "Загрузок пока нет. В списке выпусков подкаста нажмите X, чтобы скачать выпуск.",
    "Delete": "Удалить",
    # now playing
    "Sleep in {t}": "Сон через {t}", "Nothing playing": "Ничего не играет", "PODCAST": "ПОДКАСТ", "RADIO": "РАДИО",
    "On air:": "В эфире:",
    "Stopped": "Остановлено", "Paused": "Пауза", "Loading…": "Загрузка…", "Playing": "Играет", "★ favourite": "★ в избранном",
    "Volume {n}%": "Громкость {n}%", "Pause": "Пауза", "Stop": "Стоп", "Volume": "Громкость", "Sleep": "Таймер сна",
    "Screen off (MENU wakes)": "Экран выкл. (MENU включит)", "Speed": "Скорость", "Back (keeps playing)": "Назад (играет дальше)",
    "MENU: open": "MENU: открыть",
    # confirm, keyboard, loading
    "Yes": "Да", "No": "Нет", "Loading": "Загрузка", "Something went wrong: {e}": "Что-то пошло не так: {e}",
    "Type": "Ввод", "Del": "Стер.", "Space": "Пр.", "Go": "ОК", "Esc": "Отм.",
    # settings
    "Not set (choose in Radio > By country)": "Не выбрана (выберите в Радио > По странам)", "Podcast charts": "Чарты подкастов",
    "Language": "Язык", "Change": "Изменить", "Delete all downloads": "Удалить все загрузки", "Check for updates": "Проверять обновления",
    "On · a notice when a new version is out": "Вкл. · уведомление о новой версии", "Off": "Выкл.", "Check now": "Проверить сейчас",
    "You have version {v}": "У вас версия {v}", 
    "Delete all downloads?": "Удалить все загрузки?",
    "Downloaded episodes are removed from the handheld. Your subscriptions and listening progress are kept.":
        "Скачанные выпуски будут удалены с консоли. Подписки и прогресс прослушивания сохранятся.",
    # podcast chart regions
    "United States": "США", "United Kingdom": "Великобритания", "Canada": "Канада", "Australia": "Австралия", "India": "Индия",
    "Japan": "Япония", "Germany": "Германия", "France": "Франция", "Spain": "Испания", "Brazil": "Бразилия", "Mexico": "Мексика",
    "Italy": "Италия", "Netherlands": "Нидерланды", "Sweden": "Швеция",
    # about
    "Internet radio and podcasts for muOS handhelds. Stations come from the community Radio Browser directory "
    "(radio-browser.info). Podcast search and charts come from Apple's public podcast directory, and episodes from "
    "each show's own feed. Nothing is recorded or re-shared.":
        "Интернет-радио и подкасты для консолей с muOS. Станции берутся из общественного каталога Radio Browser "
        "(radio-browser.info). Поиск и чарты подкастов — из публичного каталога подкастов Apple, а выпуски — из ленты "
        "каждой передачи. Ничего не записывается и не распространяется повторно.",
    "Privacy": "Конфиденциальность", "Scroll": "Прокрутка",
    # privacy
    "PocketKode Radio never reads or sends your files, and doesn't record anything.":
        "PocketKode Radio никогда не читает и не отправляет ваши файлы и ничего не записывает.",
    "Stations come from Radio Browser, podcasts from Apple's podcast directory, and the sound from each station or show "
    "itself. Your searches go to those services. When you play a station, Radio Browser is told that the station was "
    "played (an anonymous count that keeps its Top list up to date).":
        "Станции берутся из Radio Browser, подкасты — из каталога Apple, а звук идёт от самой станции или передачи. "
        "Ваши поисковые запросы уходят в эти сервисы. Когда вы включаете станцию, Radio Browser узнаёт, что её "
        "слушали (анонимный подсчёт, чтобы список популярных был актуальным).",
    "Your favourites, subscriptions and history stay on the handheld. No ads, no analytics, no tracking.":
        "Избранное, подписки и история хранятся на консоли. Без рекламы, аналитики и слежки.",
    # notices
    "Updated": "Обновлено", "Update undone": "Обновление отменено", 
    "PocketKode Radio is now version {v}. Your stations, podcasts and settings were kept.": "PocketKode Radio обновлён до версии {v}. Станции, подкасты и настройки сохранены.",
    "Version {bad} didn't start, so PocketKode Radio went back to {v}. Please email feedback@pocketkode.com.":
        "Версия {bad} не запустилась, поэтому PocketKode Radio вернулся к {v}. Напишите на feedback@pocketkode.com.",
    # messages made in net.py, player.py, podcasts.py, radio.py
    "The connection timed out. Check Wi-Fi and try again.": "Время ожидания истекло. Проверьте Wi-Fi и попробуйте снова.",
    "That feed is too large to load.": "Эта лента слишком большая для загрузки.",
    "The server sent something the app couldn't read.": "Сервер прислал то, что приложение не смогло прочитать.",
    "Radio directory unavailable.": "Каталог радиостанций недоступен.",
    "mpv isn't installed on this system.": "В этой системе не установлен mpv.",
    "This couldn't be played. The station or episode may be offline.": "Не удалось воспроизвести. Возможно, станция или выпуск недоступны.",
    "This podcast's feed couldn't be read.": "Не удалось прочитать ленту этого подкаста.",
    # full version free forever (2026-09-28)
    "Free and open source (MIT License). See LICENSE in the app folder.": "Бесплатное приложение с открытым исходным кодом (лицензия MIT). См. LICENSE в папке приложения.",
    "For updates it reads the latest release on GitHub (you can turn this off in Settings). It sends nothing about you or the handheld.": "Для обновлений приложение читает последний выпуск на GitHub (это можно выключить в настройках). Оно ничего не отправляет о вас или о консоли.",
}

PATTERNS = [
    (r"The server said no \(error (\d+)\)\. Try again later\.", r"Сервер отказал (ошибка \1). Попробуйте позже."),
    (r"Connection problem: (.*)", r"Проблема с подключением: \1"),
    (r"Couldn't start the player: (.*)", r"Не удалось запустить плеер: \1"),
]
