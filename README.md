# PocketKode Radio

**Internet radio and podcasts for muOS handhelds**, with the screen off to save battery. Free. No account, no ads, no tracking.

| | |
|---|---|
| ![Home screen](screenshots/home.png) | ![Radio menu](screenshots/radio.png) |
| ![Top stations](screenshots/top-stations.png) | ![Now playing](screenshots/now-playing.png) |
| ![Podcasts](screenshots/podcasts.png) | ![Podcast search](screenshots/podcast-search.png) |
| ![A podcast's episodes, with progress](screenshots/episodes.png) | ![Stations by genre](screenshots/genres.png) |

- **Radio:** thousands of stations from around the world (top stations, by country, by genre, search), favourites and
  **My country**.
- **Podcasts:** search and charts, subscriptions, downloads that play without Wi-Fi, and where you stopped in every episode.
- **Screen off** while it keeps playing, a **sleep timer**, and 9 languages.

## Guide

How to install and use PocketKode Radio (stations, podcasts, Now playing, the screen off and the sleep timer) is on
**[pocketkode.com/apps/pocketkode-radio](https://pocketkode.com/apps/pocketkode-radio/)**. Downloads come only from there.

## Privacy

PocketKode Radio never reads or sends your files, and doesn't record anything.

For updates it reads the latest release on GitHub (you can turn this off in **Settings**), and an update you choose to install is downloaded from pocketkode.com. It sends nothing about you
or the handheld.

Stations come from **Radio Browser**, podcasts from **Apple's podcast directory**, and the sound from each station or
show itself. Your searches go to those services. When you play a station, Radio Browser is told that the station was
played (an anonymous count that keeps its Top list up to date).

Your favourites, subscriptions and history stay on the handheld. No ads, no analytics, no tracking.

## Build

`bash build.sh` (needs bash, curl, unzip, zip, shasum and python3) produces `dist/PocketKodeRadio.muxapp`: the app's
Python source as it is, plus the Noto Sans JP, SC and KR fonts. The app uses the Python 3, SDL2, SDL2_ttf and mpv that
come with muOS.

## Third-party

- **Noto Sans JP, SC and KR** ([noto-cjk](https://github.com/notofonts/noto-cjk)), © Adobe and Google, SIL Open Font
  License 1.1: bundled unmodified in the package (`fonts/`, licences in `licenses/`).
- **Radio Browser** ([radio-browser.info](https://www.radio-browser.info)): the community station directory (open data).
- **Apple's podcast directory**: podcast search and charts. Episodes come from each podcast's own feed.

Stations and podcasts belong to their broadcasters and creators. PocketKode Radio is an independent app and is not
affiliated with Radio Browser, Apple, any broadcaster or podcast, muOS or Anbernic.

## License

© 2026 PocketKode. All rights reserved. Bundled third-party parts keep their own licenses (see the `licenses/` folder).
Bug reports and ideas: **feedback@pocketkode.com**.
