# How to use Claude Design for Electify

1. Go to **https://claude.ai/design**
2. Click **"New design"**
3. Paste the prompt below into the chat
4. Iterate with comments on the canvas — refine colors, typography, spacing
5. Export the final designs and use them as a reference for future tweaks to the real site

---

## PROMPT TO PASTE INTO CLAUDE DESIGN

Design a polished, modern web app called **Electify** — a student-built directory of "easy electives" at the American University of Beirut (AUB). The site helps undergraduates find general-education courses that are well-taught, manageable, and rewarding. The unique twist is a live "community suggestions" section where any student can submit an easy elective they took, and when 3+ students suggest the same course it's promoted to the main list.

### Brand
- **Name:** Electify — tagline: "Easy AUB electives, picked by students"
- **Logo mark:** a small lightning bolt inside a rounded square in AUB red
- **Primary color:** AUB red `#7B1818` (use as accent)
- **Background:** warm off-white `#FAF7F2` with charcoal text `#1F1B16`
- **Ease score colors:** green `#2F7D32` (8-10 = "very easy"), amber `#C77700` (5-7 = "moderate"), red `#B33A3A` (1-4 = "harder")
- **Typography:** editorial serif for headings (Fraunces or Playfair), Inter for body
- **Vibe:** trustworthy, university-grade, slightly editorial — like a well-designed campus magazine, not a generic deals site

### Pages to design (desktop + mobile mockups)

**1. Home page**
- Top thin banner: "Student-sourced. Always verify with the official AUB catalogue before you register."
- Hero: large serif headline "Find an elective you'll actually enjoy.", subtitle explaining what Electify pulls together, a big search bar
- Two CTAs near hero: "+ Suggest an easy elective" and "See what other students suggested →"
- 6 attribute tiles: Cultures & Histories, Societies & Individuals, Understanding Communication, Understanding the World, Social Inequalities, Quantitative Reasoning — each with a course count
- "Top picks — easiest reported" — 6 course cards with ease score badges
- "Featured this semester" — curated picks for the current term
- Bottom CTA card (red gradient): "Took an easy elective lately? Add it to Electify in 30 seconds."

**2. Course detail page** (e.g., ECON 203)
- Course code + title in serif
- Big circular ease score badge (e.g., "9/10" colored green)
- Sections: About the course, Recommended professors (with per-term Spring/Summer chips), What students said (review cards), Quick takes, Sources row at the bottom
- "Report an inaccuracy" link

**3. Browse page**
- Filter row at top: search input, attribute dropdown, ease dropdown
- Grid of course cards (3 cols desktop, 2 cols tablet, 1 col mobile)

**4. Community suggestions page**
- Title "Community suggestions" + subtitle "Live picks submitted by AUB students. Not yet verified."
- "Trending — about to be promoted" section with cards showing courses that have 3+ student votes (with a "Trending · 3 votes" chip in red)
- "Fresh suggestions" section with cards showing single-vote suggestions (with a quieter "1 vote" chip)
- Each card shows: course code, title, average ease score, recommended professors, student tip quotes

**5. Suggest page**
- 3-step indicator: Submit → Appears in Community → Promoted at 3+ votes
- Embedded Google Form below

### Design rules
- Generous whitespace, 12px card radius, subtle shadows on hover
- Ease score is the visual anchor — clear at a glance from any list view
- Mobile-first — table collapses to cards on phones
- Trending chip is red/AUB-colored; fresh suggestion chip is muted gray

### Deliverables
- Home (desktop + mobile)
- Course detail (desktop + mobile)
- Browse with filters open
- Community suggestions (showing both Trending and Fresh sections)
- Suggest page with embedded form
- Component sheet: ease score badge in 3 states, course card, attribute tile, search input, primary/secondary buttons, "Trending" chip, footer
