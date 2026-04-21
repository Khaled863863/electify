"""
Clean courses.json:
  1. Validate each course's attributes against the official AUB GE list (ge_raw.txt).
  2. Strip/dedupe bad professor names (topics, list labels, prefix noise, comments).

Run:  python scripts/clean_data.py
"""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "src" / "data" / "courses.json"
GE = ROOT / "scripts" / "ge_raw.txt"

# Official AUB Fall-2023 GE attributes (10 total). Source:
# AUB's "Complete List of General Education Courses" PDF.
OFFICIAL_ATTRS = {
    "Community-Engaged Learning",
    "Cultures & Histories",
    "History of Ideas",
    "Human Values",
    "Quantitative Reasoning",
    "Social Inequalities",
    "Societies & Individuals",
    "Understanding Communication",
    "Understanding the World",
    "Writing in the Discipline",
}

# Map PDF forms to our canonical display form
PDF_TO_CANON = {
    "Cultures and Histories": "Cultures & Histories",
    "Societies and Individuals": "Societies & Individuals",
}
for a in OFFICIAL_ATTRS:
    PDF_TO_CANON[a] = a


def normalize(a: str) -> str:
    return PDF_TO_CANON.get(a.strip(), a.strip())


# ---- Parse ge_raw.txt into {code: {attrs}} -----------------------------------

def parse_ge() -> dict[str, set[str]]:
    text = GE.read_text(encoding="utf-8")
    # Identify attribute tokens that may appear at end of a line
    # (longer strings first so regex is greedy-correct)
    attr_tokens = sorted(
        list(OFFICIAL_ATTRS) + ["Cultures and Histories", "Societies and Individuals"],
        key=len, reverse=True,
    )
    attr_re = re.compile(r"(?:" + "|".join(re.escape(a) for a in attr_tokens) + r")\s*$")

    code_re = re.compile(r"^([A-Z]{3,5})\s+(\d{3}[A-Z]{0,3})\b")
    alt_re  = re.compile(r"/([A-Z]{3,5})\s*(\d{3}[A-Z]{0,3})")

    mapping: dict[str, set[str]] = {}
    current_codes: list[str] = []

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            current_codes = []
            continue
        m = code_re.match(line.strip())
        if m:
            primary = f"{m.group(1)} {m.group(2)}"
            codes = [primary]
            # pick up "CODE 123/DEPT 456" alternates
            for am in alt_re.finditer(line):
                codes.append(f"{am.group(1)} {am.group(2)}")
            current_codes = codes
            for c in codes:
                mapping.setdefault(c, set())
            am = attr_re.search(line)
            if am:
                attr = normalize(am.group(0))
                for c in codes:
                    mapping[c].add(attr)
        else:
            # Continuation line: if it ends with an attribute, it's a second attribute
            # for current_codes. Otherwise it's a title overflow — ignore.
            am = attr_re.search(line.strip())
            if am and current_codes:
                # Only accept if the entire stripped line *is* the attribute (no title overflow)
                if line.strip() == am.group(0).strip():
                    attr = normalize(am.group(0))
                    for c in current_codes:
                        mapping[c].add(attr)
    # Drop codes with no attrs found (noise)
    return {k: v for k, v in mapping.items() if v}


# ---- Professor name cleanup --------------------------------------------------

BAD_NAME_SUBSTRINGS = [
    "humanities list", "social sciences list", "natural sciences",
    "arabic communication", "communications skills",
    "financial accounting", "arab poetry", "arab stylistics",
    "the lexicon", "easy with", "must be with",
    "basic chemistry", "physical geology",
    "reading instruct",
]

# Leading topic-words that sometimes prefix a real name. Strip them to recover the name.
LEADING_TOPIC_PREFIXES = [
    "business ethics", "personal financial",
    "health awareness", "ethics",
    "critical", "victorian", "introductory",
    "understanding",
]

# Exact rewrites: bad_name_lower -> fixed_name
REWRITES = {
    "dr. rima rassi": "Rima Rassi",
    "riman rassi": "Rima Rassi",
    "najah atiyyah": "Najah Hawwa Attieh",
    "najah hawwa": "Najah Hawwa Attieh",
    "najah hawwa attiyeh": "Najah Hawwa Attieh",
    "hiba khodeib": "Hiba Khodr",
    "hiba khoder": "Hiba Khodr",
    "emily ard-keyser": "Emelye Ard-Keyser",
    "maher jarrar": "Maher Jarrar",
    "joelle garro el khoury": "Joelle Garro El Khoury",
    "joelle khoury": "Joelle Garro El Khoury",
    "christopher nassar": "Christopher Nassar",
}

def clean_prof_name(raw: str) -> str | None:
    if not raw:
        return None
    n = raw.strip()
    low = n.lower()

    # Drop comments after comma
    if "," in n:
        head = n.split(",", 1)[0].strip()
        if head and head.lower() not in ("dr", "prof"):
            n = head
            low = n.lower()

    # Drop parenthetical comments
    n = re.sub(r"\s*\(.*\)$", "", n).strip()
    low = n.lower()

    # Strip common noise prefixes
    for prefix in ("dr. ", "dr ", "prof. ", "prof "):
        if low.startswith(prefix):
            n = n[len(prefix):].strip()
            low = n.lower()

    # Strip topic-prefix ("Ethics Zeinab Sabra" -> "Zeinab Sabra")
    for tp in LEADING_TOPIC_PREFIXES:
        if low.startswith(tp + " "):
            n = n[len(tp):].strip()
            low = n.lower()
            break

    # Reject anything containing a known bad substring
    for bad in BAD_NAME_SUBSTRINGS:
        if bad in low:
            return None

    # Reject obvious non-names
    if len(n) < 3 or len(n) > 50:
        return None
    if not re.search(r"[A-Za-z]", n):
        return None

    # Title-case individual lowercase words (keep "el"/"al"/"bin"/"bou"/"de" lowercase if mid-name)
    PARTICLES = {"el", "al", "bin", "bou", "de", "van", "der", "and"}
    fixed = []
    for i, w in enumerate(n.split()):
        if w.lower() in PARTICLES and i > 0:
            fixed.append(w.lower())
        elif w.isupper() and len(w) > 1:
            fixed.append(w)  # preserve real acronyms
        elif w == w.lower() or w == w.upper():
            fixed.append(w.capitalize())
        else:
            fixed.append(w)
    n = " ".join(fixed)

    # Apply rewrites
    key = n.lower()
    if key in REWRITES:
        return REWRITES[key]
    return n


def dedupe_profs(profs: list[dict]) -> list[dict]:
    """Merge entries whose cleaned names match (or are strict prefixes)."""
    out: dict[str, dict] = {}
    order: list[str] = []
    for p in profs or []:
        raw = (p.get("name") or "").strip()
        clean = clean_prof_name(raw)
        if not clean:
            continue
        key = clean.lower()
        if key not in out:
            merged = dict(p)
            merged["name"] = clean
            out[key] = merged
            order.append(key)
        else:
            tgt = out[key]
            for fld in ("notes", "terms"):
                a = list(tgt.get(fld) or [])
                for x in (p.get(fld) or []):
                    if x not in a:
                        a.append(x)
                if a:
                    tgt[fld] = a

    # Prefix dedupe: if "Maya" and "Maya Kanaan" both exist, drop "Maya"
    names = list(out.keys())
    drop = set()
    for i, a in enumerate(names):
        for b in names:
            if a == b: continue
            # a is a single-word prefix of b -> drop a
            if (" " not in a) and (b.startswith(a + " ") or b == a):
                drop.add(a)
                break
    final_order = [k for k in order if k not in drop]
    return [out[k] for k in final_order]


# ---- Main --------------------------------------------------------------------

def main():
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    ge_map = parse_ge()
    print(f"Parsed {len(ge_map)} codes from GE list")

    changed_attrs = 0
    dropped_attrs = 0
    added_attrs = 0
    changed_profs = 0
    dropped_profs = 0

    for c in payload["courses"]:
        code = c["code"]

        # --- Attributes: use official map when available ---
        existing = set(c.get("attributes") or [])
        official = ge_map.get(code, set())
        if official:
            # Authoritative: replace with official, preserving display order
            ordered = sorted(official)
            if set(ordered) != existing:
                changed_attrs += 1
                added_attrs += len(set(ordered) - existing)
                dropped_attrs += len(existing - set(ordered))
            c["attributes"] = ordered
        else:
            # Not in official list: keep only entries that match canonical set
            cleaned = [a for a in (c.get("attributes") or []) if a in OFFICIAL_ATTRS]
            if set(cleaned) != existing:
                changed_attrs += 1
                dropped_attrs += len(existing - set(cleaned))
            c["attributes"] = cleaned

        # --- Professors ---
        before = len(c.get("professors") or [])
        c["professors"] = dedupe_profs(c.get("professors") or [])
        after = len(c["professors"])
        if after != before:
            changed_profs += 1
            dropped_profs += (before - after)

    payload["courses"].sort(key=lambda x: x["code"])
    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Attrs: {changed_attrs} courses changed  (+{added_attrs} added, -{dropped_attrs} dropped)")
    print(f"Profs: {changed_profs} courses changed  (-{dropped_profs} entries removed)")

    # Report courses with no attrs now
    missing = [c["code"] for c in payload["courses"] if not c.get("attributes")]
    if missing:
        print(f"Courses with no attributes after cleanup ({len(missing)}):")
        for m in missing:
            print(f"  {m}")


if __name__ == "__main__":
    main()
