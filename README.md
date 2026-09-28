# PocketKode Radio

**Internet radio and podcasts for muOS handhelds**, with the screen off to save battery. Free and open source
([MIT License](LICENSE)). No account, no ads, no tracking.

Tested on the Anbernic RG40XXH with muOS 2601.0 Jacaranda. Other muOS devices with Wi-Fi may work: reports are welcome.

## Install

Download `PocketKodeRadio-<version>.muxapp` from the [latest release](https://github.com/mahamudul87/pocketkode-radio/releases/latest),
copy it to the `ARCHIVE` folder on SD card 1, then open **Applications → Archive Manager** and install it. Turn on
**Wi-Fi**, then open **Applications → PocketKode Radio**.

## Radio

Thousands of stations from around the world, from the community-run [Radio Browser](https://www.radio-browser.info) directory.

- **Top stations**, **By country**, **By genre** and **Search**.
- Press **Y** on a station to add it to **Favourites**. **Recently played** remembers your last 15.
- In **By country**, press **Y** to make a country **My country**: its stations then get their own entry in the Radio menu.
- Many stations show the song or show that's **on air**.

## Podcasts

- **Search** or browse **Top podcasts** (Apple's public charts; choose the country in Settings).
- Press **Y** to **subscribe**; your shows are in **My podcasts**.
- In a show's episode list: **A** play, **X** download (again to cancel, or to delete a download), **Y** mark as played, **START** subscribe.
- While an episode plays (**Now playing**), **START** downloads it; the progress shows on the screen.
- **Downloads** play without Wi-Fi. Where you stopped is remembered for every episode.

## Now playing

| Button | Radio | Podcast |
|---|---|---|
| A | Pause / play | Pause / play |
| ◀ / ▶ | | Back 15 s / forward 30 s |
| L1 / R1 | | Slower / faster (0.75x to 2x) |
| ▲ / ▼ | Volume | Volume |
| START | Favourite | |
| Y | Sleep timer (15, 30, 45, 60, 90 min, off) | Sleep timer |
| SELECT | **Screen off** (only **MENU** turns it back on, so a button pressed in a bag doesn't) | Screen off |
| X | Stop | Stop |
| B | Back; keeps playing | Back; keeps playing |

While something plays, a bar at the bottom of every screen shows it; press **MENU** to open Now playing.

## Settings

- **My country**, **Podcast charts** country, **Language**, **Delete all downloads** (subscriptions and progress are
  kept) and **Check for updates** (on or off).

## Language

English, 日本語 (Japanese), Español, Français, Deutsch, Nederlands, Русский, 简体中文 (Simplified Chinese) or 한국어
(Korean). The app follows muOS's language (**Configuration > Language**); any other language means English. To choose
yourself, open **Settings → Language** and press **A** or **◀ ▶** (Auto → English → 日本語 → … → 한국어); the choice is kept.
English uses the app's own pixel font; the other languages use the Noto Sans JP, SC and KR fonts (see
[Third-party](#third-party)).

## Notes

- Radio and streaming need **Wi-Fi**. Downloaded episodes don't.
- In English, station and podcast names use the app's pixel font (accented letters appear without accents); names in
  other scripts, such as Japanese, Chinese, Korean or Cyrillic, use the Noto fonts.
- Nothing is recorded or re-shared. Streams and episodes belong to their broadcasters and creators.

## Privacy

PocketKode Radio never reads or sends your files, and doesn't record anything.

For updates it reads the latest release on GitHub (you can turn this off in **Settings**). It sends nothing about you
or the handheld.

Stations come from **Radio Browser**, podcasts from **Apple's podcast directory**, and the sound from each station or
show itself. Your searches go to those services. When you play a station, Radio Browser is told that the station was
played (an anonymous count that keeps its Top list up to date).

Your favourites, subscriptions and history stay on the handheld. No ads, no analytics, no tracking.

## Updates

When the handheld is online, the app reads `update.json` from this repository's latest release (at start and once a
day) and shows **Update available** with what's new. Nothing is installed unless you choose **Update**. The download
is checked (its SHA-256 and PocketKode's Ed25519 signature, public key in `updater.py`) before anything changes, and
the new version is installed when the app restarts (**Restart now**); your stations, podcasts and settings stay. If an
updated version doesn't start, the app goes back to the previous one by itself. Turn it off in
**Settings → Check for updates**.

## Troubleshooting

- **"No internet connection":** turn on Wi-Fi in **Configuration → Network**.
- **"Secure connection failed":** the handheld's date and time are wrong. Fix them in muOS's settings.
- **A station doesn't play:** some stations go offline or change address; try another. Logs: `logs/app.log` and
  `logs/mpv.log` in the app folder.

## Building

Needs bash, zip, unzip, curl, shasum and Python 3.

```sh
./build.sh
```

This makes `dist/PocketKodeRadio.muxapp`. The app is plain Python 3 and uses the Python, SDL2, SDL2_ttf and mpv that
come with muOS; the build only adds the Noto fonts (downloaded and checked against their SHA-256). To try a change
quickly, copy the source files over the installed app in `/mnt/mmc/MUOS/application/PocketKodeRadio/` and start it
again.

A build of your own can't install PocketKode's updates over itself unless it's signed with PocketKode's key, so for a
fork change `REPO` and `UPDATE_KEY` in `updater.py`, or turn updates off.

## Contributing

Bug reports, station or podcast problems, translations and pull requests are welcome: open an
[issue](https://github.com/mahamudul87/pocketkode-radio/issues), or email **feedback@pocketkode.com**.

- Every text shown on screen is wrapped in `_("English text")`; translations are in `texts_<code>.py` (the app's own
  texts) and `lang_common.py` (updates and network messages). A missing translation stays English.
- Please test on a handheld before sending a pull request, and say which device and muOS version you used.

## Third-party

- **Noto Sans JP, SC and KR** ([noto-cjk](https://github.com/notofonts/noto-cjk)), © Adobe and Google, SIL Open Font
  License 1.1: bundled unmodified in the package (`fonts/`, licences in `licenses/`).
- **Radio Browser** ([radio-browser.info](https://www.radio-browser.info)): the community station directory (open data).
- **Apple's podcast directory**: podcast search and charts. Episodes come from each podcast's own feed.

Stations and podcasts belong to their broadcasters and creators. PocketKode Radio is an independent app and is not
affiliated with Radio Browser, Apple, any broadcaster or podcast, muOS or Anbernic.

## License

[MIT](LICENSE) © 2026 PocketKode
