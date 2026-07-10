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

## 3. Turn on the snake animation

The contribution-graph snake needs the GitHub Action to run once to create the images:

1. Go to the repo → **Actions** tab → enable workflows if prompted.
2. Open **"Generate Snake Animation"** → **Run workflow**.
3. It generates the SVGs and pushes them to an `output` branch — the README already points there.
   After the first run (and every 12h after), the snake will render.

## Things you may want to edit

- **LeetCode username** — the badge/link assumes `ashutoshsharma1309`. Fix if different.
- **Card theme** — all cards use `tokyonight`. Swap the `theme=` param in `README.md`
  for `radical`, `dark`, `dracula`, `catppuccin_mocha`, etc.
- **Accent color** — currently `7AA2F7` (blue). Find/replace to recolor typing header + cards.
- **Project links** — the project cards have no repo links yet; wrap the titles in
  `[### 🔍 LGTM](https://github.com/...)` style links once repos are public.

Everything else pulls live from your GitHub — no maintenance needed.
