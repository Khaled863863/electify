"""
Electify - static site generator.

Reads src/data/courses.json + site.config.json, renders templates/, writes dist/.
"""
from __future__ import annotations
import json, shutil
from pathlib import Path
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "src" / "data" / "courses.json"
CONFIG = ROOT / "site.config.json"
TPL = ROOT / "templates"
DIST = ROOT / "dist"


def attr_slug(name: str) -> str:
    return name.lower().replace(" & ", "-").replace(" ", "-")


def prof_slug(name: str) -> str:
    return (
        name.lower()
        .replace(".", "")
        .replace(",", "")
        .replace("'", "")
        .replace("  ", " ")
        .strip()
        .replace(" ", "-")
    )


def _rm_retry(func, path, exc):
    import time, stat, os
    try:
        os.chmod(path, stat.S_IWRITE)
        time.sleep(0.5)
        func(path)
    except Exception:
        pass


def main() -> None:
    if DIST.exists():
        for attempt in range(5):
            try:
                shutil.rmtree(DIST, onexc=_rm_retry)
                break
            except (PermissionError, OSError):
                import time
                time.sleep(1)
        else:
            print("Could not clean dist/. Pause OneDrive sync and retry.")
            return
    DIST.mkdir(exist_ok=True)
    (DIST / "course").mkdir(exist_ok=True)
    (DIST / "attribute").mkdir(exist_ok=True)
    (DIST / "professor").mkdir(exist_ok=True)

    payload = json.loads(DATA.read_text(encoding="utf-8"))
    courses = payload["courses"]
    generated_at = payload["generated_at"][:10]

    config = {}
    if CONFIG.exists():
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
    form_embed_url = config.get("form_embed_url", "") or ""
    sheet_csv_url = config.get("sheet_csv_url", "") or ""
    cf_token = config.get("cloudflare_analytics_token", "") or ""
    ga4_id = config.get("ga4_measurement_id", "") or ""

    by_attr: dict[str, list] = defaultdict(list)
    for c in courses:
        for a in c.get("attributes", []):
            by_attr[a].append(c)
    for v in by_attr.values():
        v.sort(key=lambda x: (-(x.get("ease_score") or 0), x["code"]))

    attributes = [
        {"name": a, "slug": attr_slug(a), "count": len(v)}
        for a, v in sorted(by_attr.items())
    ]

    rated = [c for c in courses if c.get("ease_score")]
    rated.sort(key=lambda x: (-(x["ease_score"]), x["code"]))
    top = rated[:6]

    spring_codes = {c["code"] for c in courses if "ccs_spring" in c.get("sources", [])}
    featured = [c for c in courses if c["code"] in spring_codes][:6]

    existing_codes = sorted({c["code"] for c in courses})
    existing_courses = {
        c["code"]: {
            "slug": c["slug"],
            "title": c.get("title", ""),
            "attributes": c.get("attributes", []) or [],
            "ease": c.get("ease_score") or 0,
        }
        for c in courses
    }

    env = Environment(
        loader=FileSystemLoader(str(TPL)),
        autoescape=select_autoescape(["html"]),
    )
    env.globals["generated_at"] = generated_at
    env.globals["cloudflare_analytics_token"] = cf_token
    env.globals["ga4_measurement_id"] = ga4_id

    def write(path: Path, html: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")

    write(DIST / "index.html", env.get_template("index.html").render(
        rel="", attributes=attributes, count=len(courses), top=top, featured=featured,
    ))
    write(DIST / "browse.html", env.get_template("browse.html").render(
        rel="", attributes=attributes, count=len(courses),
        courses=sorted(courses, key=lambda x: x["code"]),
    ))
    write(DIST / "methodology.html", env.get_template("methodology.html").render(rel=""))
    write(DIST / "suggest.html", env.get_template("suggest.html").render(
        rel="", form_embed_url=form_embed_url, count=len(courses),
    ))
    write(DIST / "suggestions.html", env.get_template("suggestions.html").render(
        rel="", sheet_csv_url=sheet_csv_url,
        existing_codes=existing_codes, existing_courses=existing_courses,
    ))

    for a, list_ in by_attr.items():
        write(DIST / "attribute" / f"{attr_slug(a)}.html", env.get_template("attribute.html").render(
            rel="../", attribute=a, courses=list_,
        ))

    for c in courses:
        write(DIST / "course" / f"{c['slug']}.html", env.get_template("course.html").render(
            rel="../", c=c,
        ))

    # Professor pages
    by_prof: dict[str, list] = defaultdict(list)
    for c in courses:
        for p in c.get("professors", []) or []:
            name = (p.get("name") or "").strip()
            if name:
                by_prof[name].append(c)
    for name, list_ in by_prof.items():
        list_.sort(key=lambda x: (-(x.get("ease_score") or 0), x["code"]))
        write(DIST / "professor" / f"{prof_slug(name)}.html", env.get_template("professor.html").render(
            rel="../", prof_name=name, courses=list_,
        ))

    # Shortlist & compare (client-rendered from courses.json)
    write(DIST / "shortlist.html", env.get_template("shortlist.html").render(rel=""))
    write(DIST / "compare.html", env.get_template("compare.html").render(rel=""))

    # courses.json payload consumed by palette/random/shortlist/compare
    courses_json = [
        {
            "code": c["code"],
            "slug": c["slug"],
            "title": c.get("title") or c["code"],
            "ease": c.get("ease_score"),
            "attrs": c.get("attributes", []),
            "profs": [p.get("name") for p in (c.get("professors") or []) if p.get("name")],
            "grading": c.get("grading"),
            "recommended": c.get("recommended", True),
        }
        for c in courses
    ]
    (DIST / "courses.json").write_text(json.dumps(courses_json, ensure_ascii=False), encoding="utf-8")

    (DIST / "_redirects").write_text("/  /index.html  200\n", encoding="utf-8")

    print(f"Built {len(courses)} courses + {len(by_attr)} attributes + {len(by_prof)} profs -> {DIST}")
    if not form_embed_url:
        print("  (form_embed_url not set in site.config.json - suggest page shows placeholder)")
    if not sheet_csv_url:
        print("  (sheet_csv_url not set in site.config.json - suggestions page shows empty state)")


if __name__ == "__main__":
    main()
