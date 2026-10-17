# DualSense Hub

A small Windows app for the PS5 DualSense and DualSense Edge. Works over USB and Bluetooth, no drivers, no admin rights.

- Battery level right in the tray, with history and a time-left estimate
- Adaptive triggers: 86 ready effects plus an editor you can feel live
- Game support:
  - 88 games with their own trigger support. The app steps aside and lets them work.
  - 15 games where the app adds the triggers itself: Elden Ring, Bloodborne, Dark Souls 1–3, Sekiro, Lies of P and the Devil May Cry series.
  - 32 profiles for popular games without trigger support, like GTA V, RDR2, Forza, CS2 and Skyrim.
  - Your own profile for any .exe
- Light bar colour, player LEDs and a button test

## Download

Grab `DualSenseHub.exe` from [Releases](../../releases/latest) and run it. It's a single file and needs nothing else installed.

The app updates itself. New versions download in the background and install the next time you restart it. You can turn this off in Settings.

## Share your setup

Every trigger feel can be tuned on the game's page. If you get one just right, hit **Share**. You can send it as a short code or a file, or publish it to the **Community** tab, where anyone can try it with one click. Before an import, your current settings are backed up.

## Found a bug? Have an idea?

Use **Send feedback** in Settings or the tray menu, or **Feel off? Tell me** on any game's page. The app fills in the report for you and shows exactly what it attaches.

## Good to know

- Steam keeps working alongside the app.
- Elden Ring reads your weapon and every attack from memory only when Easy Anti-Cheat is off. **Play offline** on its page starts the game through Steam without EAC, and the controller keeps working. With EAC on, it follows your D-pad instead and never touches the game.
- Many games only send their own trigger effects over USB. On Bluetooth the app fills in a matching feel for them.
- No vibration in a game on Bluetooth? The Vibration tab shows what to switch on in Steam.

## Windows shows a warning?

Windows may show SmartScreen for a new app that few people have run yet. Click **More info → Run anyway**. Only download the app from this page.

## Credits

The controller photo is by Chris Woodrich (Wikimedia Commons, CC BY-SA 4.0). The controller artwork is by AL2009man from [VSCView](https://github.com/Nielk1/VSCView) (MIT). Game offsets are based on libeldenring, TGA CT, fromsoftware-rs, Erd-Tools, ASNH0's Bloodborne menu and the GoldHEN cheats. Full details are in the app under Settings → Credits.

DualSense and PlayStation are trademarks of Sony Interactive Entertainment. This project isn't affiliated with Sony.

## License

DualSense Hub is free to download and use for personal, non-commercial purposes. Everything else is reserved: the app and its source may not be copied, modified, redistributed or sold. See [LICENSE](LICENSE).
