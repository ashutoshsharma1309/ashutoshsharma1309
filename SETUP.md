# Profile README — Setup

This is a **special repo**: to show a profile README on your GitHub page, the repo
**must be named exactly `ashutoshsharma1309`** (same as your username) and be **public**.

## 1. Create the repo on GitHub

- New repo → name it `ashutoshsharma1309` → **Public** → don't add a README (this repo has one).

## 2. Push this folder

```bash
git add .
git commit -m "profile readme"
git branch -M main
git remote add origin https://github.com/ashutoshsharma1309/ashutoshsharma1309.git
git push -u origin main
```

## Editing the animated banner

The terminal banner is a self-contained SVG generated from two inputs:

- **`image.txt`** — the ASCII logo on the left (paste any ASCII art).
- **`assets/build_header.py`** — the info card, colors, and animation timeline.

After any change, regenerate and commit:

```bash
python3 assets/build_header.py      # rewrites assets/header.svg
git add image.txt assets/ && git commit -m "update banner" && git push
```

Useful knobs in `build_header.py`:

- **`card`** — the info-card rows (Focus, Roles, Lang, Contact, …).
- **`RED` / `ART` / `GREEN`** — accent, logo, and prompt colors.
- **`BOOT_END` / `LOGO_T` / `LOGO_STAG` / `CARD_STAG`** — the animation timing.

## Things you may want to edit

- **LeetCode / Codeforces** — the badges/links use the handle `agh0r`. Fix if different.
- **Card theme** — the two GitHub-stats cards use `tokyonight`; swap the `theme=` param
  in `README.md` for `dark`, `dracula`, `catppuccin_mocha`, etc. Accent is `ff6b6b`.
- **Project links** — the project cards have no repo links yet; wrap a title in
  `[**🔍 LGTM**](https://github.com/…)` once each repo is public.

Everything else pulls live from your GitHub — no maintenance needed.
