# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""PocketKode Radio in Korean: {English text in the code: Korean}. A text missing here stays English.
The shared parts (activation, removal, updates) are in lang_common.py."""

TEXTS = {
    # lists and counts
    "1 station": "방송국 1개", "{n} stations": "방송국 {n}개", "1 episode": "에피소드 1개", "{n} episodes": "에피소드 {n}개",
    "Nothing here yet.": "아직 아무것도 없습니다.",
    # home
    "Now playing": "재생 중", "Turn off the screen": "화면 끄기",
    "Keeps playing · press MENU to turn it back on": "계속 재생 · MENU를 누르면 화면이 켜집니다",
    "What's new · A to update": "새로운 점 · A로 업데이트", "Downloaded · restart to finish": "다운로드 완료 · 다시 시작하면 끝납니다",
    "Update available: {v}": "업데이트 있음: {v}",
    "Radio": "라디오", "Stations from around the world": "전 세계의 방송국",
    "Podcasts": "팟캐스트", "{n} subscribed": "{n}개 구독 중", "Search, subscribe, download": "검색, 구독, 다운로드",
    "Settings": "설정", "Your country, podcast region, downloads, language": "내 나라, 팟캐스트 지역, 다운로드, 언어",
    "About": "정보", "Version {v}": "버전 {v}", "Open": "열기", "Quit": "종료",
    # radio
    "Favourites": "즐겨찾기", "Recently played": "최근 재생", "Top stations": "인기 방송국", "Most played worldwide": "전 세계에서 가장 많이 듣는 방송국",
    "Stations in {country}": "{country}의 방송국", "Most played first": "많이 듣는 순",
    "By country": "국가별", "Choose a country": "국가 고르기", "By genre": "장르별", "Pop, rock, news, jazz, talk…": "팝, 록, 뉴스, 재즈, 토크…",
    "Search": "검색", "Find a station by name": "이름으로 방송국 찾기", "Countries": "국가", "Genres": "장르", "Search stations": "방송국 검색",
    "No favourites yet. Press Y on a station to add it.": "아직 즐겨찾기가 없습니다. 방송국에서 Y를 누르면 추가됩니다.",
    "Stations you play appear here.": "들은 방송국이 여기에 나타납니다.", "No stations found.": "방송국을 찾지 못했습니다.",
    "Play": "재생", "Favourite": "즐겨찾기", "Added to favourites": "즐겨찾기에 추가했습니다", "Removed from favourites": "즐겨찾기에서 뺐습니다",
    "My country": "내 나라", "{country} set as your country": "{country}을(를) 내 나라로 정했습니다",
    # podcasts
    "My podcasts": "내 팟캐스트", "Downloads": "다운로드",
    "1 episode on this handheld": "이 기기에 에피소드 1개", "{n} episodes on this handheld": "이 기기에 에피소드 {n}개",
    "Top podcasts": "인기 팟캐스트", "Charts: {region}": "차트: {region}", "Find a podcast by name or topic": "이름이나 주제로 팟캐스트 찾기",
    "Search podcasts": "팟캐스트 검색",
    "No subscriptions yet. Find a podcast in Search or Top podcasts and press Y to subscribe.":
        "아직 구독이 없습니다. 검색이나 인기 팟캐스트에서 팟캐스트를 찾아 Y를 눌러 구독하세요.",
    "No podcasts found.": "팟캐스트를 찾지 못했습니다.", "Episodes": "에피소드", "Subscribe": "구독",
    "Subscribed": "구독했습니다", "Unsubscribed": "구독을 취소했습니다", "✓ subscribed": "✓ 구독 중",
    "{m} min": "{m}분", "✓ played": "✓ 들음", "{t} left": "{t} 남음", "started": "듣는 중",
    "Download": "다운로드", "Played": "들음", "Delete download?": "다운로드를 삭제할까요?",
    "Download cancelled": "다운로드를 취소했습니다", "Downloading…": "다운로드 중…",
    "No downloads yet. In a podcast's episode list, press X to download an episode.":
        "아직 다운로드가 없습니다. 팟캐스트의 에피소드 목록에서 X를 누르면 에피소드를 내려받습니다.",
    "Delete": "삭제",
    # now playing
    "Sleep in {t}": "{t} 후 꺼짐", "Nothing playing": "재생 중인 것이 없습니다", "PODCAST": "팟캐스트", "RADIO": "라디오",
    "On air:": "방송 중:",
    "Stopped": "정지됨", "Paused": "일시정지됨", "Loading…": "불러오는 중…", "Playing": "재생 중", "★ favourite": "★ 즐겨찾기",
    "Volume {n}%": "볼륨 {n}%", "Pause": "일시정지", "Stop": "정지", "Volume": "볼륨", "Sleep": "취침 타이머",
    "Screen off (MENU wakes)": "화면 끄기(MENU로 켬)", "Speed": "속도", "Back (keeps playing)": "뒤로(계속 재생)",
    "MENU: open": "MENU: 열기",
    # confirm, keyboard, loading
    "Yes": "예", "No": "아니요", "Loading": "불러오는 중", "Something went wrong: {e}": "문제가 발생했습니다: {e}",
    "Type": "입력", "Del": "지우기", "Space": "공백", "Go": "확인", "Esc": "취소",
    # settings
    "Not set (choose in Radio > By country)": "설정 안 됨(라디오 > 국가별에서 선택)", "Podcast charts": "팟캐스트 차트",
    "Language": "언어", "Change": "변경", "Delete all downloads": "모든 다운로드 삭제", "Check for updates": "업데이트 확인",
    "On · a notice when a new version is out": "켬 · 새 버전이 나오면 알림", "Off": "끔", "Check now": "지금 확인",
    "You have version {v}": "현재 버전 {v}",
    "Delete all downloads?": "모든 다운로드를 삭제할까요?",
    "Downloaded episodes are removed from the handheld. Your subscriptions and listening progress are kept.":
        "내려받은 에피소드가 기기에서 삭제됩니다. 구독과 듣던 위치는 그대로 남습니다.",
    # podcast chart regions
    "United States": "미국", "United Kingdom": "영국", "Canada": "캐나다", "Australia": "호주", "India": "인도",
    "Japan": "일본", "Germany": "독일", "France": "프랑스", "Spain": "스페인", "Brazil": "브라질", "Mexico": "멕시코",
    "Italy": "이탈리아", "Netherlands": "네덜란드", "Sweden": "스웨덴",
    # about
    "Internet radio and podcasts for muOS handhelds. Stations come from the community Radio Browser directory "
    "(radio-browser.info). Podcast search and charts come from Apple's public podcast directory, and episodes from "
    "each show's own feed. Nothing is recorded or re-shared.":
        "muOS 휴대용 게임기를 위한 인터넷 라디오와 팟캐스트. 방송국은 커뮤니티가 운영하는 Radio Browser 디렉터리"
        "(radio-browser.info)에서, 팟캐스트 검색과 차트는 Apple의 공개 팟캐스트 디렉터리에서, 에피소드는 각 프로그램의 "
        "피드에서 가져옵니다. 아무것도 녹음하거나 재배포하지 않습니다.",
    "Privacy": "개인정보", "Scroll": "스크롤",
    # privacy
    "PocketKode Radio never reads or sends your files, and doesn't record anything.":
        "PocketKode Radio는 파일을 절대 읽거나 보내지 않으며, 아무것도 녹음하지 않습니다.",
    "Stations come from Radio Browser, podcasts from Apple's podcast directory, and the sound from each station or show "
    "itself. Your searches go to those services. When you play a station, Radio Browser is told that the station was "
    "played (an anonymous count that keeps its Top list up to date).":
        "방송국은 Radio Browser에서, 팟캐스트는 Apple의 팟캐스트 디렉터리에서, 소리는 각 방송국이나 프로그램에서 직접 옵니다. "
        "검색어는 그 서비스들로 보내집니다. 방송국을 재생하면 그 방송국이 재생되었다는 사실이 Radio Browser에 전달됩니다"
        "(인기 목록을 최신으로 유지하는 익명 집계).",
    "Your favourites, subscriptions and history stay on the handheld. No ads, no analytics, no tracking.":
        "즐겨찾기, 구독, 기록은 기기에 남습니다. 광고, 분석, 추적이 전혀 없습니다.",
    # notices
    "Updated": "업데이트됨", "Update undone": "업데이트 취소됨",
    "PocketKode Radio is now version {v}. Your stations, podcasts and settings were kept.": "PocketKode Radio가 버전 {v}이(가) 되었습니다. 방송국, 팟캐스트, 설정은 그대로입니다.",
    "Version {bad} didn't start, so PocketKode Radio went back to {v}. Please email feedback@pocketkode.com.":
        "버전 {bad}이(가) 시작되지 않아 PocketKode Radio가 {v}(으)로 돌아갔습니다. feedback@pocketkode.com으로 메일을 보내 주세요.",
    # messages made in net.py, player.py, podcasts.py, radio.py
    "The connection timed out. Check Wi-Fi and try again.": "연결 시간이 초과되었습니다. Wi-Fi를 확인하고 다시 시도하세요.",
    "That feed is too large to load.": "피드가 너무 커서 불러올 수 없습니다.",
    "The server sent something the app couldn't read.": "서버가 앱이 읽을 수 없는 내용을 보냈습니다.",
    "Radio directory unavailable.": "방송국 디렉터리를 사용할 수 없습니다.",
    "mpv isn't installed on this system.": "이 시스템에는 mpv가 설치되어 있지 않습니다.",
    "This couldn't be played. The station or episode may be offline.": "재생할 수 없습니다. 방송국이나 에피소드가 오프라인일 수 있습니다.",
    "This podcast's feed couldn't be read.": "이 팟캐스트의 피드를 읽지 못했습니다.",
    # about and privacy
    "Free and open source (MIT License). See LICENSE in the app folder.": "무료 오픈 소스입니다(MIT 라이선스). 앱 폴더의 LICENSE를 참고하세요.",
    "For updates it reads the latest release on GitHub (you can turn this off in Settings). It sends nothing about you or the handheld.": "업데이트를 위해 GitHub의 최신 릴리스를 확인합니다(설정에서 끌 수 있습니다). 사용자나 기기에 관한 정보는 아무것도 보내지 않습니다.",
}

PATTERNS = [
    (r"The server said no \(error (\d+)\)\. Try again later\.", r"서버가 거절했습니다(오류 \1). 나중에 다시 시도하세요."),
    (r"Connection problem: (.*)", r"연결 문제: \1"),
    (r"Couldn't start the player: (.*)", r"플레이어를 시작하지 못했습니다: \1"),
]
