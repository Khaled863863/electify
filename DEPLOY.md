# Electify — Step-by-step deployment

Time required: about 45 minutes total (15 of those waiting on Cloudflare/GitHub).

---

## STEP 1 — Preview locally first (2 min)

The site is already built into `dist/`. Spin up a local server to look at it:

```bash
cd "C:\Users\user\OneDrive - American University of Beirut\Desktop\electify\dist"
python -m http.server 8000
```

Open **http://localhost:8000** in your browser. You should see the Electify home page with 73 courses across 6 attributes. Click around: home → browse → a course detail → a category page → community → suggest.

If anything looks off, stop here and tell me what you see.

---

## STEP 2 — Push to GitHub (10 min)

You need a GitHub account. If you don't have one, sign up at https://github.com — use your AUB email (`@mail.aub.edu`) so you also qualify for the Student Pack in step 6.

1. Install Git for Windows if you don't have it: https://git-scm.com/download/win
2. Open a terminal in the project folder:

```bash
cd "C:\Users\user\OneDrive - American University of Beirut\Desktop\electify"
git init
git add .
git commit -m "Initial Electify site"
```

3. On GitHub, click "+" → "New repository". Name it `electify`, make it Public, **don't** add a README. Click Create.
4. Back in the terminal, paste the two commands GitHub shows you (they'll look like):

```bash
git remote add origin https://github.com/YOUR_USERNAME/electify.git
git branch -M main
git push -u origin main
```

You should now see all your files on github.com/YOUR_USERNAME/electify.

---

## STEP 3 — Deploy to Cloudflare Pages (10 min)

1. Sign up at https://dash.cloudflare.com/sign-up (free, no card needed). Use the same email if you want.
2. In the dashboard, go to **Workers & Pages** → **Create** → **Pages** tab → **Connect to Git**
3. Authorize Cloudflare to read your GitHub. Pick the `electify` repo.
4. **Build settings**:
   - Framework preset: **None**
   - Build command: *(leave blank — `dist/` is already built)*
   - Build output directory: `dist`
5. Click **Save and Deploy**.
6. Wait ~1 minute. You'll get a live URL like **https://electify.pages.dev** or **https://electify-abc.pages.dev**.

That URL is your live site. Share it with anyone.

> **Note:** Right now `dist/` is committed. To rebuild after editing data, run `python scripts/build_data.py && python scripts/build_site.py` and `git push`. Cloudflare auto-redeploys.

---

## STEP 4 — Set up the community-suggestions Google Form (10 min)

This is what makes the live "Community" section work.

1. Go to https://forms.new (Google Forms).
2. Title the form **"Suggest an Electify course"**. Add these fields, in order, **with these exact names** (the site's parser looks for these keywords):
   - **Course code** (short answer) — required. Help text: "e.g. ECON 203"
   - **Course title** (short answer) — optional
   - **Professor** (short answer) — optional. Help text: "Who taught it?"
   - **Ease score** (linear scale 1 to 10) — required
   - **Tip** (paragraph) — optional. Help text: "One thing future students should know"
3. Click **Send** (top-right) → the **`< >`** tab → copy the embed `<iframe src="...">` URL. You only need the part inside `src="..."`.
4. Click the **Responses** tab → green Sheets icon → **Create spreadsheet**. A Google Sheet opens.
5. In the Sheet: **File → Share → Publish to web** → publish the whole document as **CSV**. Copy the URL it gives you (looks like `https://docs.google.com/spreadsheets/d/e/.../pub?output=csv`).
6. Open `site.config.json` in the project and paste both URLs:

```json
{
  "form_embed_url": "PASTE THE FORM URL HERE",
  "sheet_csv_url": "PASTE THE PUBLISHED-CSV URL HERE"
}
```

7. Rebuild and push:

```bash
cd "C:\Users\user\OneDrive - American University of Beirut\Desktop\electify"
python scripts/build_site.py
git add -A
git commit -m "Wire up community suggestions form"
git push
```

Cloudflare redeploys in ~30 seconds. The Suggest page now embeds your Google Form, and the Community page reads submissions live from your Google Sheet.

> **How "promote to main" works:** when 3+ rows in the sheet share the same course code, the Community page tags the course as "Trending". To formally fold it into the main list, copy that course into `MASTER_LIST` at the bottom of `scripts/build_data.py`, then re-run `build_data.py && build_site.py && git push`.

---

## STEP 5 — Pick your custom domain (free options)

You'll already be live at `electify.pages.dev`. To get a nicer URL, pick one:

### Option A — `electify.is-a.dev` (free forever, ~1 day)
1. Fork https://github.com/is-a-dev/register
2. Add a JSON file `domains/electify.json` with:
   ```json
   {
     "owner": { "username": "YOUR_GITHUB_USERNAME", "email": "electify.site@outlook.com" },
     "record": { "CNAME": "electify.pages.dev" }
   }
   ```
3. Open a Pull Request. A bot reviews it; merged within ~24 hours.
4. In Cloudflare Pages → your site → **Custom domains** → **Set up a custom domain** → enter `electify.is-a.dev`.

### Option B — `electify.me` via GitHub Student Pack (free 1 year)
1. Apply at https://education.github.com/pack with your AUB email + a photo of your AUB ID. Approval: ~1 day.
2. Once approved, follow the Namecheap link in the Pack to claim a free `.me` domain.
3. In Namecheap, set the domain's nameservers to Cloudflare (Cloudflare → "Add a site" walks you through this).
4. In Cloudflare Pages → **Custom domains** → add `electify.me`.

### Option C — `electify.pages.dev` (already done, ugly but works)

My recommendation: do **A** today (instant), and **B** in parallel for the better domain in a few days.

---

## STEP 6 — Apply for GitHub Student Pack (do this now in parallel)

While Cloudflare is deploying, open https://education.github.com/pack in another tab and apply. AUB email + a photo of your AUB ID is usually enough. Approval takes about a day. Worth it: free `.me` domain, free Namecheap, free GitHub Pro, lots more.

---

## Maintenance: how to add/edit courses later

- **Edit master list inline:** open `scripts/build_data.py`, edit the `MASTER_LIST` Python list at the bottom, then run:
  ```bash
  python scripts/build_data.py && python scripts/build_site.py && git add -A && git commit -m "update courses" && git push
  ```
- **Re-extract from new PDFs:** drop new PDFs into `C:\Users\user\Downloads`, edit the file list at the top of `scripts/build_data.py`, then re-run as above.
- **Promote a community suggestion to main:** copy the row from the Google Sheet into `MASTER_LIST` and rebuild.

---

## Files in this project

```
electify/
├── DEPLOY.md                  ← this file
├── CLAUDE_DESIGN_PROMPT.md    ← paste into claude.ai/design for visual mockups
├── ARCHITECTURE.md            ← high-level architecture (in easy-electives-extract/)
├── site.config.json           ← Google Form + Sheet URLs (you fill these in step 4)
├── scripts/
│   ├── build_data.py          ← extracts PDFs+xlsx into courses.json
│   └── build_site.py          ← renders templates into dist/
├── templates/                 ← Jinja HTML templates
├── src/data/courses.json      ← consolidated 73-course dataset
└── dist/                      ← what gets deployed (regenerate with build_site.py)
```
