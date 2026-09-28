# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""PocketKode Radio in Japanese: {English text in the code: Japanese}. A text missing here stays English.
The shared parts (activation, removal, updates) are in lang_common.py."""

TEXTS = {
    # lists and counts
    "1 station": "1 局", "{n} stations": "{n} 局", "1 episode": "1 エピソード", "{n} episodes": "{n} エピソード",
    "Nothing here yet.": "まだ何もありません。",
    # home
    "Now playing": "再生中", "Turn off the screen": "画面を消す",
    "Keeps playing · press MENU to turn it back on": "再生は続きます · MENU で画面がつきます",
    "What's new · A to update": "新しい点 · A でアップデート", "Downloaded · restart to finish": "ダウンロード済み · 再起動して完了",
    "Update available: {v}": "アップデートがあります：{v}",
    "Radio": "ラジオ", "Stations from around the world": "世界中のラジオ局", 
    "Podcasts": "ポッドキャスト", "{n} subscribed": "{n} 番組を購読中", "Search, subscribe, download": "検索、購読、ダウンロード",
    "Settings": "設定", "Your country, podcast region, downloads, language": "国、ポッドキャストの地域、ダウンロード、言語",
    "About": "情報", "Version {v}": "バージョン {v}", "Open": "開く", "Quit": "終了", 
    # full version features (activation screen)
    # radio
    "Favourites": "お気に入り", "Recently played": "最近聴いた局", "Top stations": "人気局", "Most played worldwide": "世界で最も聴かれている局",
    "Stations in {country}": "{country}のラジオ局", "Most played first": "よく聴かれている順",
    "By country": "国別", "Choose a country": "国を選ぶ", "By genre": "ジャンル別", "Pop, rock, news, jazz, talk…": "ポップ、ロック、ニュース、ジャズ、トーク…",
    "Search": "検索", "Find a station by name": "名前でラジオ局を探す", "Countries": "国", "Genres": "ジャンル", "Search stations": "ラジオ局を検索",
    "No favourites yet. Press Y on a station to add it.": "お気に入りはまだありません。ラジオ局で Y を押すと追加されます。",
    "Stations you play appear here.": "聴いたラジオ局がここに表示されます。", "No stations found.": "ラジオ局が見つかりませんでした。",
    "Play": "再生", "Favourite": "お気に入り", "Added to favourites": "お気に入りに追加しました", "Removed from favourites": "お気に入りから削除しました",
    "My country": "自分の国", "{country} set as your country": "{country}を自分の国にしました",
    # podcasts
    "My podcasts": "マイポッドキャスト", "Downloads": "ダウンロード",
    "1 episode on this handheld": "この携帯ゲーム機に 1 エピソード", "{n} episodes on this handheld": "この携帯ゲーム機に {n} エピソード",
    "Top podcasts": "人気のポッドキャスト", "Charts: {region}": "ランキング：{region}", "Find a podcast by name or topic": "名前や話題でポッドキャストを探す",
    "Search podcasts": "ポッドキャストを検索",
    "No subscriptions yet. Find a podcast in Search or Top podcasts and press Y to subscribe.":
        "購読している番組はまだありません。検索か人気のポッドキャストで番組を探し、Y で購読してください。",
    "No podcasts found.": "ポッドキャストが見つかりませんでした。", "Episodes": "エピソード", "Subscribe": "購読",
    "Subscribed": "購読しました", "Unsubscribed": "購読をやめました", "✓ subscribed": "✓ 購読中",
    "{m} min": "{m} 分", "✓ played": "✓ 再生済み", "{t} left": "残り {t}", "started": "途中まで",
    "Download": "ダウンロード", "Played": "再生済み", "Delete download?": "ダウンロードを削除しますか？",
    "Download cancelled": "ダウンロードを中止しました", "Downloading…": "ダウンロード中…",
    "No downloads yet. In a podcast's episode list, press X to download an episode.":
        "ダウンロードはまだありません。ポッドキャストのエピソード一覧で X を押すとダウンロードできます。",
    "Delete": "削除",
    # now playing
    "Sleep in {t}": "スリープまで {t}", "Nothing playing": "何も再生していません", "PODCAST": "ポッドキャスト", "RADIO": "ラジオ",
    "On air:": "放送中：",
    "Stopped": "停止", "Paused": "一時停止", "Loading…": "読み込み中…", "Playing": "再生中", "★ favourite": "★ お気に入り",
    "Volume {n}%": "音量 {n}%", "Pause": "一時停止", "Stop": "停止", "Volume": "音量", "Sleep": "スリープ",
    "Screen off (MENU wakes)": "画面オフ（MENU で復帰）", "Speed": "速度", "Back (keeps playing)": "戻る（再生は続く）",
    "MENU: open": "MENU：開く",
    # confirm, keyboard, loading
    "Yes": "はい", "No": "いいえ", "Loading": "読み込み中", "Something went wrong: {e}": "エラーが発生しました：{e}",
    "Type": "入力", "Del": "削除", "Space": "スペース", "Go": "決定", "Esc": "やめる",
    # settings
    "Not set (choose in Radio > By country)": "未設定（ラジオ > 国別 で選択）", "Podcast charts": "ポッドキャストのランキング",
    "Language": "言語", "Change": "変更", "Delete all downloads": "すべてのダウンロードを削除", "Check for updates": "アップデートの確認",
    "On · a notice when a new version is out": "オン · 新しいバージョンが出たら通知", "Off": "オフ", "Check now": "今すぐ確認",
    "You have version {v}": "現在のバージョン {v}", 
    "Delete all downloads?": "すべてのダウンロードを削除しますか？",
    "Downloaded episodes are removed from the handheld. Your subscriptions and listening progress are kept.":
        "ダウンロードしたエピソードを携帯ゲーム機から削除します。購読と再生位置は残ります。",
    # podcast chart regions
    "United States": "アメリカ", "United Kingdom": "イギリス", "Canada": "カナダ", "Australia": "オーストラリア", "India": "インド",
    "Japan": "日本", "Germany": "ドイツ", "France": "フランス", "Spain": "スペイン", "Brazil": "ブラジル", "Mexico": "メキシコ",
    "Italy": "イタリア", "Netherlands": "オランダ", "Sweden": "スウェーデン",
    # about
    "Internet radio and podcasts for muOS handhelds. Stations come from the community Radio Browser directory "
    "(radio-browser.info). Podcast search and charts come from Apple's public podcast directory, and episodes from "
    "each show's own feed. Nothing is recorded or re-shared.":
        "muOS 携帯ゲーム機のためのネットラジオとポッドキャスト。ラジオ局はコミュニティの Radio Browser ディレクトリ（radio-browser.info）から、"
        "ポッドキャストの検索とランキングは Apple の公開ポッドキャストディレクトリから、エピソードは各番組のフィードから取得します。"
        "録音や再配布は一切しません。",
    "Privacy": "プライバシー", "Scroll": "スクロール",
    # privacy
    "PocketKode Radio never reads or sends your files, and doesn't record anything.":
        "PocketKode Radio があなたのファイルを読み取ったり送信したりすることはなく、何も録音しません。",
    "Stations come from Radio Browser, podcasts from Apple's podcast directory, and the sound from each station or show "
    "itself. Your searches go to those services. When you play a station, Radio Browser is told that the station was "
    "played (an anonymous count that keeps its Top list up to date).":
        "ラジオ局は Radio Browser から、ポッドキャストは Apple のポッドキャストディレクトリから、音声は各ラジオ局や番組から届きます。"
        "検索はそれらのサービスに送られます。ラジオ局を再生すると、その局が再生されたことが Radio Browser に伝えられます"
        "（人気局の一覧を最新に保つための匿名のカウントです）。",
    "Your favourites, subscriptions and history stay on the handheld. No ads, no analytics, no tracking.":
        "お気に入り、購読、履歴は携帯ゲーム機に保存されます。広告、アクセス解析、トラッキングは一切ありません。",
    # notices
    "Updated": "アップデートしました", "Update undone": "アップデートを取り消しました", 
    "PocketKode Radio is now version {v}. Your stations, podcasts and settings were kept.": "PocketKode Radio はバージョン {v} になりました。ラジオ局、ポッドキャスト、設定はそのままです。",
    "Version {bad} didn't start, so PocketKode Radio went back to {v}. Please email feedback@pocketkode.com.":
        "バージョン {bad} が起動しなかったため、PocketKode Radio は {v} に戻りました。feedback@pocketkode.com までメールしてください。",
    # messages made in net.py, player.py, podcasts.py, radio.py
    "The connection timed out. Check Wi-Fi and try again.": "接続がタイムアウトしました。Wi-Fi を確認してもう一度お試しください。",
    "That feed is too large to load.": "このフィードは大きすぎて読み込めません。",
    "The server sent something the app couldn't read.": "サーバーから読み取れないデータが届きました。",
    "Radio directory unavailable.": "ラジオ局のディレクトリを利用できません。",
    "mpv isn't installed on this system.": "このシステムには mpv がインストールされていません。",
    "This couldn't be played. The station or episode may be offline.": "再生できませんでした。ラジオ局かエピソードがオフラインの可能性があります。",
    "This podcast's feed couldn't be read.": "このポッドキャストのフィードを読み取れませんでした。",
    # full version free forever (2026-09-28)
    "Free and open source (MIT License). See LICENSE in the app folder.": "無料のオープンソースです（MIT ライセンス）。アプリのフォルダーの LICENSE をご覧ください。",
    "For updates it reads the latest release on GitHub (you can turn this off in Settings). It sends nothing about you or the handheld.": "アップデートのために GitHub の最新リリースを読み込みます（設定でオフにできます）。あなたや携帯ゲーム機についての情報は何も送りません。",
}

PATTERNS = [
    (r"The server said no \(error (\d+)\)\. Try again later\.", r"サーバーに拒否されました（エラー \1）。しばらくしてからお試しください。"),
    (r"Connection problem: (.*)", r"接続の問題：\1"),
    (r"Couldn't start the player: (.*)", r"プレーヤーを起動できませんでした：\1"),
]
