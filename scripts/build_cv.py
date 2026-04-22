"""Build Khaled Rabah's CV as a clean one-page PDF."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

OUT = r"C:\Users\user\Downloads\Khaled_Rabah_CV.pdf"

INK   = HexColor('#111111')
SOFT  = HexColor('#333333')
MUTED = HexColor('#777777')
LINE  = HexColor('#cccccc')
LINK  = HexColor('#1f4eb8')

doc = SimpleDocTemplate(
    OUT,
    pagesize=letter,
    leftMargin=0.65 * inch,
    rightMargin=0.65 * inch,
    topMargin=0.55 * inch,
    bottomMargin=0.55 * inch,
    title="Khaled Rabah - CV",
    author="Khaled Rabah",
)

S = {
    'name':     ParagraphStyle('name',     fontName='Helvetica-Bold', fontSize=24, leading=28, textColor=INK,   spaceAfter=2),
    'headline': ParagraphStyle('headline', fontName='Helvetica',      fontSize=11, leading=14, textColor=SOFT,  spaceAfter=5),
    'contact':  ParagraphStyle('contact',  fontName='Helvetica',      fontSize=9.5,leading=12, textColor=MUTED, spaceAfter=8),
    'section':  ParagraphStyle('section',  fontName='Helvetica-Bold', fontSize=9.5,leading=11, textColor=INK,   spaceBefore=12, spaceAfter=2),
    'role':     ParagraphStyle('role',     fontName='Helvetica-Bold', fontSize=10.5,leading=13,textColor=INK,   spaceAfter=1),
    'meta':     ParagraphStyle('meta',     fontName='Helvetica-Oblique',fontSize=9.5,leading=12,textColor=MUTED,spaceAfter=4),
    'para':     ParagraphStyle('para',     fontName='Helvetica',      fontSize=10, leading=13.5,textColor=INK,  spaceAfter=2),
    'bullet':   ParagraphStyle('bullet',   fontName='Helvetica',      fontSize=10, leading=13.5,textColor=INK,  spaceAfter=2, leftIndent=12),
    'skills':   ParagraphStyle('skills',   fontName='Helvetica',      fontSize=10.5,leading=14, textColor=INK,  spaceAfter=2),
}

def section(title):
    return Paragraph(title.upper(), S['section'])

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=LINE, spaceBefore=1, spaceAfter=5)

def link(url, text=None, color=LINK):
    text = text or url
    hex_color = '#%02x%02x%02x' % (int(color.red*255), int(color.green*255), int(color.blue*255))
    return f'<link href="{url}" color="{hex_color}">{text}</link>'

story = []

# ===== HEADER =====
story.append(Paragraph("Khaled Rabah", S['name']))
story.append(Paragraph("CS @ AUB &middot; Building Electify &middot; Java / Python / React", S['headline']))
story.append(Paragraph(
    "khaledrabah863@outlook.com &middot; Beirut, Lebanon &middot; "
    + link("https://linkedin.com/in/khaled-rabah-kr741", "linkedin.com/in/khaled-rabah-kr741")
    + " &middot; "
    + link("https://github.com/Khaled863863", "github.com/Khaled863863"),
    S['contact']
))

# ===== PROJECTS =====
story.append(section("Projects"))
story.append(hr())
story.append(Paragraph(
    "<b>Electify</b> &nbsp;&middot;&nbsp; "
    + link("https://electify.pages.dev", "electify.pages.dev")
    + " &nbsp;&middot;&nbsp; "
    + link("https://github.com/Khaled863863/electify", "github.com/Khaled863863/electify"),
    S['role']
))
story.append(Paragraph(
    "Static directory of 68+ easy AUB general-education electives. Solo build using Python "
    "and Jinja2 for the static site generator, Tailwind CSS for styling, deployed on Cloudflare Pages. "
    "Custom data pipeline (cleaning, deduping, ease scoring), Google Forms intake for crowdsourced "
    "suggestions, command-K search palette, light and dark theming. Live at electify.pages.dev.",
    S['para']
))

# ===== EDUCATION =====
story.append(section("Education"))
story.append(hr())

story.append(Paragraph("American University of Beirut", S['role']))
story.append(Paragraph("BS Computer Science &nbsp;&middot;&nbsp; Beirut, Lebanon &nbsp;&middot;&nbsp; Sep 2025 to May 2028", S['meta']))
story.append(Paragraph("&bull;&nbsp; HES Scholarship recipient (formerly USAID-funded)", S['bullet']))
story.append(Paragraph("&bull;&nbsp; Relevant coursework: Programming Fundamentals, Software Development, Math 201", S['bullet']))

story.append(Spacer(1, 7))
story.append(Paragraph("Lebanese Baccalaureate, General Sciences", S['role']))
story.append(Paragraph("Jeb Janine Public High School &nbsp;&middot;&nbsp; Oct 2022 to Jul 2025", S['meta']))
story.append(Paragraph("&bull;&nbsp; Graduated with distinction", S['bullet']))

# ===== EXPERIENCE =====
story.append(section("Experience"))
story.append(hr())

story.append(Paragraph("HES Scholarship Ambassador and Presenter", S['role']))
story.append(Paragraph("Various Schools, Lebanon &nbsp;&middot;&nbsp; Dec 2025 to Present", S['meta']))
story.append(Paragraph("&bull;&nbsp; Presented the HES Scholarship program to prospective applicants at partner schools across Lebanon", S['bullet']))
story.append(Paragraph("&bull;&nbsp; Walked students through the application process and answered questions one-on-one", S['bullet']))
story.append(Paragraph("&bull;&nbsp; Represented AUB and the scholarship program in public-facing settings", S['bullet']))

story.append(Spacer(1, 7))
story.append(Paragraph("Community Volunteer", S['role']))
story.append(Paragraph("Medical Center and Local Community, Bekaa &nbsp;&middot;&nbsp; Sep 2025 to Present", S['meta']))
story.append(Paragraph(
    "&bull;&nbsp; Coordinated patient flow during clinic hours to keep waiting times short and appointments on schedule",
    S['bullet']
))
story.append(Paragraph(
    "&bull;&nbsp; Supported the front-desk team with daily appointment management and patient check-in",
    S['bullet']
))

# ===== SKILLS =====
story.append(section("Skills"))
story.append(hr())
story.append(Paragraph(
    "<b>Languages and tools:</b> &nbsp; Java &nbsp;&middot;&nbsp; Python &nbsp;&middot;&nbsp; React &nbsp;&middot;&nbsp; Git &nbsp;&middot;&nbsp; HTML/CSS &nbsp;&middot;&nbsp; SQL",
    S['skills']
))
story.append(Paragraph(
    "<b>Languages spoken:</b> &nbsp; English (fluent) &nbsp;&middot;&nbsp; Arabic (native)",
    S['skills']
))

doc.build(story)
print(f"Built CV: {OUT}")
