# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""PocketKode Radio in Simplified Chinese: {English text in the code: Chinese}. A text missing here stays English.
The shared parts (activation, removal, updates) are in lang_common.py."""

TEXTS = {
    # lists and counts
    "1 station": "1 个电台", "{n} stations": "{n} 个电台", "1 episode": "1 集", "{n} episodes": "{n} 集",
    "Nothing here yet.": "这里还没有内容。",
    # home
    "Now playing": "正在播放", "Turn off the screen": "关闭屏幕",
    "Keeps playing · press MENU to turn it back on": "继续播放 · 按 MENU 重新点亮屏幕",
    "What's new · A to update": "新内容 · 按 A 更新", "Downloaded · restart to finish": "已下载 · 重启以完成",
    "Update available: {v}": "有可用更新：{v}",
    "Radio": "电台", "Stations from around the world": "来自世界各地的电台", 
    "Podcasts": "播客", "{n} subscribed": "已订阅 {n} 个", "Search, subscribe, download": "搜索、订阅、下载",
    "Settings": "设置", "Your country, podcast region, downloads, language": "你的国家、播客地区、下载、语言",
    "About": "关于", "Version {v}": "版本 {v}", "Open": "打开", "Quit": "退出", 
    # full version features (activation screen)
    # radio
    "Favourites": "收藏", "Recently played": "最近收听", "Top stations": "热门电台", "Most played worldwide": "全球收听最多",
    "Stations in {country}": "{country}的电台", "Most played first": "按收听次数排序",
    "By country": "按国家", "Choose a country": "选择国家", "By genre": "按类型", "Pop, rock, news, jazz, talk…": "流行、摇滚、新闻、爵士、谈话…",
    "Search": "搜索", "Find a station by name": "按名称查找电台", "Countries": "国家", "Genres": "类型", "Search stations": "搜索电台",
    "No favourites yet. Press Y on a station to add it.": "还没有收藏。在电台上按 Y 即可收藏。",
    "Stations you play appear here.": "你收听过的电台会显示在这里。", "No stations found.": "没有找到电台。",
    "Play": "播放", "Favourite": "收藏", "Added to favourites": "已加入收藏", "Removed from favourites": "已取消收藏",
    "My country": "我的国家", "{country} set as your country": "已将{country}设为你的国家",
    # podcasts
    "My podcasts": "我的播客", "Downloads": "下载",
    "1 episode on this handheld": "掌机上有 1 集", "{n} episodes on this handheld": "掌机上有 {n} 集",
    "Top podcasts": "热门播客", "Charts: {region}": "排行榜：{region}", "Find a podcast by name or topic": "按名称或话题查找播客",
    "Search podcasts": "搜索播客",
    "No subscriptions yet. Find a podcast in Search or Top podcasts and press Y to subscribe.":
        "还没有订阅。在“搜索”或“热门播客”中找到播客，按 Y 订阅。",
    "No podcasts found.": "没有找到播客。", "Episodes": "单集", "Subscribe": "订阅",
    "Subscribed": "已订阅", "Unsubscribed": "已取消订阅", "✓ subscribed": "✓ 已订阅",
    "{m} min": "{m} 分钟", "✓ played": "✓ 已听", "{t} left": "剩余 {t}", "started": "已开始",
    "Download": "下载", "Played": "已听", "Delete download?": "删除下载？",
    "Download cancelled": "已取消下载", "Downloading…": "正在下载…",
    "No downloads yet. In a podcast's episode list, press X to download an episode.":
        "还没有下载。在播客的单集列表中按 X 即可下载单集。",
    "Delete": "删除",
    # now playing
    "Sleep in {t}": "{t} 后停止", "Nothing playing": "没有在播放", "PODCAST": "播客", "RADIO": "电台",
    "On air:": "正在播出：",
    "Stopped": "已停止", "Paused": "已暂停", "Loading…": "加载中…", "Playing": "播放中", "★ favourite": "★ 已收藏",
    "Volume {n}%": "音量 {n}%", "Pause": "暂停", "Stop": "停止", "Volume": "音量", "Sleep": "定时",
    "Screen off (MENU wakes)": "熄屏（按 MENU 点亮）", "Speed": "倍速", "Back (keeps playing)": "返回（继续播放）",
    "MENU: open": "MENU：打开",
    # confirm, keyboard, loading
    "Yes": "是", "No": "否", "Loading": "加载中", "Something went wrong: {e}": "出错了：{e}",
    "Type": "输入", "Del": "删除", "Space": "空格", "Go": "确定", "Esc": "取消",
    # settings
    "Not set (choose in Radio > By country)": "未设置（在 电台 > 按国家 中选择）", "Podcast charts": "播客排行榜",
    "Language": "语言", "Change": "更改", "Delete all downloads": "删除所有下载", "Check for updates": "检查更新",
    "On · a notice when a new version is out": "开 · 有新版本时提醒", "Off": "关", "Check now": "立即检查",
    "You have version {v}": "当前版本 {v}", 
    "Delete all downloads?": "删除所有下载？",
    "Downloaded episodes are removed from the handheld. Your subscriptions and listening progress are kept.":
        "已下载的单集会从掌机上删除。你的订阅和收听进度都会保留。",
    # podcast chart regions
    "United States": "美国", "United Kingdom": "英国", "Canada": "加拿大", "Australia": "澳大利亚", "India": "印度",
    "Japan": "日本", "Germany": "德国", "France": "法国", "Spain": "西班牙", "Brazil": "巴西", "Mexico": "墨西哥",
    "Italy": "意大利", "Netherlands": "荷兰", "Sweden": "瑞典",
    # about
    "Internet radio and podcasts for muOS handhelds. Stations come from the community Radio Browser directory "
    "(radio-browser.info). Podcast search and charts come from Apple's public podcast directory, and episodes from "
    "each show's own feed. Nothing is recorded or re-shared.":
        "适用于 muOS 掌机的网络电台和播客。电台来自社区维护的 Radio Browser 目录（radio-browser.info）。播客搜索和排行榜"
        "来自 Apple 公开的播客目录，单集来自各节目自己的订阅源。不录制、不转发任何内容。",
    "Privacy": "隐私", "Scroll": "滚动",
    # privacy
    "PocketKode Radio never reads or sends your files, and doesn't record anything.":
        "PocketKode Radio 从不读取或发送你的文件，也不录制任何内容。",
    "Stations come from Radio Browser, podcasts from Apple's podcast directory, and the sound from each station or show "
    "itself. Your searches go to those services. When you play a station, Radio Browser is told that the station was "
    "played (an anonymous count that keeps its Top list up to date).":
        "电台来自 Radio Browser，播客来自 Apple 的播客目录，声音来自各电台或节目本身。你的搜索会发送给这些服务。"
        "当你播放某个电台时，Radio Browser 会得知该电台被收听了（这是匿名计数，用于保持热门列表的更新）。",
    "Your favourites, subscriptions and history stay on the handheld. No ads, no analytics, no tracking.":
        "你的收藏、订阅和历史记录都保存在掌机上。没有广告、没有统计分析、没有跟踪。",
    # notices
    "Updated": "已更新", "Update undone": "更新已撤销", 
    "PocketKode Radio is now version {v}. Your stations, podcasts and settings were kept.": "PocketKode Radio 现在是 {v} 版。你的电台、播客和设置都已保留。",
    "Version {bad} didn't start, so PocketKode Radio went back to {v}. Please email feedback@pocketkode.com.":
        "{bad} 版无法启动，因此 PocketKode Radio 已恢复到 {v} 版。请发邮件至 feedback@pocketkode.com。",
    # messages made in net.py, player.py, podcasts.py, radio.py
    "The connection timed out. Check Wi-Fi and try again.": "连接超时。请检查 Wi-Fi 后重试。",
    "That feed is too large to load.": "该订阅源太大，无法加载。",
    "The server sent something the app couldn't read.": "服务器返回了应用无法读取的内容。",
    "Radio directory unavailable.": "电台目录不可用。",
    "mpv isn't installed on this system.": "此系统没有安装 mpv。",
    "This couldn't be played. The station or episode may be offline.": "无法播放。电台或单集可能已下线。",
    "This podcast's feed couldn't be read.": "无法读取该播客的订阅源。",
    # full version free forever (2026-09-28)
    "Free and open source (MIT License). See LICENSE in the app folder.": "免费开源（MIT 许可证）。请参阅应用文件夹中的 LICENSE。",
    "For updates it reads the latest release on GitHub (you can turn this off in Settings). It sends nothing about you or the handheld.": "为了更新，它会读取 GitHub 上的最新版本（可在设置中关闭）。它不会发送任何关于你或掌机的信息。",
}

PATTERNS = [
    (r"The server said no \(error (\d+)\)\. Try again later\.", r"服务器拒绝了请求（错误 \1）。请稍后再试。"),
    (r"Connection problem: (.*)", r"连接问题：\1"),
    (r"Couldn't start the player: (.*)", r"无法启动播放器：\1"),
]
