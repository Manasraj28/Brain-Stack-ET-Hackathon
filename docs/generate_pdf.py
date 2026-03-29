from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable

# ── COLORS ──
ET_RED    = colors.HexColor('#C0392B')
ET_GOLD   = colors.HexColor('#B8860B')
INK       = colors.HexColor('#0D0D0D')
DARK_GRAY = colors.HexColor('#2C2C2C')
MID_GRAY  = colors.HexColor('#555555')
LIGHT_BG  = colors.HexColor('#F4EFE6')
RULE      = colors.HexColor('#DDD5C0')
GREEN     = colors.HexColor('#1A6B3C')
BLUE      = colors.HexColor('#1A3A6B')
WHITE     = colors.white

W, H = A4

def build_styles():
    base = getSampleStyleSheet()
    s = {}

    s['cover_team'] = ParagraphStyle('cover_team',
        fontName='Helvetica-Bold', fontSize=13, textColor=ET_GOLD,
        alignment=TA_CENTER, spaceAfter=4, letterSpacing=3)

    s['cover_title'] = ParagraphStyle('cover_title',
        fontName='Helvetica-Bold', fontSize=28, textColor=WHITE,
        alignment=TA_CENTER, spaceAfter=8, leading=34)

    s['cover_sub'] = ParagraphStyle('cover_sub',
        fontName='Helvetica', fontSize=12, textColor=colors.HexColor('#CCCCCC'),
        alignment=TA_CENTER, spaceAfter=4)

    s['cover_hackathon'] = ParagraphStyle('cover_hackathon',
        fontName='Helvetica-Bold', fontSize=10, textColor=ET_RED,
        alignment=TA_CENTER, letterSpacing=2)

    s['section_num'] = ParagraphStyle('section_num',
        fontName='Helvetica-Bold', fontSize=8, textColor=ET_RED,
        spaceAfter=2, letterSpacing=2)

    s['section_title'] = ParagraphStyle('section_title',
        fontName='Helvetica-Bold', fontSize=16, textColor=INK,
        spaceBefore=6, spaceAfter=10, leading=20)

    s['sub_title'] = ParagraphStyle('sub_title',
        fontName='Helvetica-Bold', fontSize=11, textColor=INK,
        spaceBefore=10, spaceAfter=5, leading=14)

    s['body'] = ParagraphStyle('body',
        fontName='Helvetica', fontSize=10, textColor=DARK_GRAY,
        spaceAfter=6, leading=16, alignment=TA_JUSTIFY)

    s['bullet'] = ParagraphStyle('bullet',
        fontName='Helvetica', fontSize=10, textColor=DARK_GRAY,
        spaceAfter=4, leading=15, leftIndent=14, bulletIndent=0)

    s['caption'] = ParagraphStyle('caption',
        fontName='Helvetica-Oblique', fontSize=8, textColor=MID_GRAY,
        alignment=TA_CENTER, spaceAfter=6)

    s['quote'] = ParagraphStyle('quote',
        fontName='Helvetica-Oblique', fontSize=11, textColor=BLUE,
        leftIndent=20, rightIndent=20, spaceBefore=8, spaceAfter=8,
        leading=16, borderPad=8)

    s['tag'] = ParagraphStyle('tag',
        fontName='Helvetica-Bold', fontSize=7, textColor=WHITE,
        alignment=TA_CENTER, letterSpacing=1)

    s['mono'] = ParagraphStyle('mono',
        fontName='Courier', fontSize=9, textColor=DARK_GRAY,
        spaceAfter=3, leading=13, leftIndent=10)

    return s

def divider(color=RULE, thickness=0.5):
    return HRFlowable(width='100%', thickness=thickness, color=color, spaceAfter=10, spaceBefore=4)

def section_header(num, title, s):
    return [
        Spacer(1, 6*mm),
        Paragraph(f"0{num}  ——————", s['section_num']),
        Paragraph(title, s['section_title']),
        divider(ET_RED, 1.5),
    ]

def colored_table(data, col_widths, header_bg=INK, row_bg=LIGHT_BG):
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), header_bg),
        ('TEXTCOLOR',  (0,0), (-1,0), WHITE),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,0), 9),
        ('ALIGN',      (0,0), (-1,0), 'LEFT'),
        ('TOPPADDING', (0,0), (-1,0), 7),
        ('BOTTOMPADDING',(0,0),(-1,0), 7),
        ('LEFTPADDING',(0,0),(-1,-1), 10),
        ('RIGHTPADDING',(0,0),(-1,-1), 10),
        ('BACKGROUND', (0,1), (-1,-1), row_bg),
        ('FONTNAME',   (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',   (0,1), (-1,-1), 9),
        ('TOPPADDING', (0,1), (-1,-1), 6),
        ('BOTTOMPADDING',(0,1),(-1,-1), 6),
        ('GRID',       (0,0), (-1,-1), 0.3, RULE),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE, LIGHT_BG]),
        ('VALIGN',     (0,0), (-1,-1), 'TOP'),
    ])
    t = Table(data, colWidths=col_widths)
    t.setStyle(style)
    return t

def highlight_box(text, s, bg=LIGHT_BG, border=ET_RED):
    data = [[Paragraph(text, s['body'])]]
    t = Table(data, colWidths=[W - 40*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LINEBEFORE', (0,0), (0,-1), 3, border),
        ('LINEBELOW', (0,-1), (-1,-1), 0.3, RULE),
    ]))
    return t

# ─────────────────────────────────────────────
#  PAGE TEMPLATES
# ─────────────────────────────────────────────

def on_first_page(canvas, doc):
    canvas.saveState()
    # Full black background
    canvas.setFillColor(INK)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # Red top bar
    canvas.setFillColor(ET_RED)
    canvas.rect(0, H-14*mm, W, 14*mm, fill=1, stroke=0)
    # ET Logo text
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica-Bold', 22)
    canvas.drawString(20*mm, H-10*mm, 'ET')
    canvas.setFont('Helvetica', 9)
    canvas.drawString(38*mm, H-9.5*mm, 'ECONOMIC TIMES')
    # Gold text right
    canvas.setFillColor(ET_GOLD)
    canvas.setFont('Helvetica-Bold', 7)
    canvas.drawRightString(W-20*mm, H-9.5*mm, 'GEN AI HACKATHON 2026')
    # Bottom bar
    canvas.setFillColor(ET_RED)
    canvas.rect(0, 0, W, 10*mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica', 8)
    canvas.drawCentredString(W/2, 3.5*mm, 'CONFIDENTIAL — TEAM BRAIN STACK — ET GEN AI HACKATHON 2026')
    canvas.restoreState()

def on_later_pages(canvas, doc):
    canvas.saveState()
    # Top thin red line
    canvas.setStrokeColor(ET_RED)
    canvas.setLineWidth(2)
    canvas.line(20*mm, H-12*mm, W-20*mm, H-12*mm)
    # Header
    canvas.setFillColor(ET_RED)
    canvas.setFont('Helvetica-Bold', 8)
    canvas.drawString(20*mm, H-9*mm, 'ET AI-NATIVE NEWS EXPERIENCE')
    canvas.setFillColor(MID_GRAY)
    canvas.setFont('Helvetica', 8)
    canvas.drawRightString(W-20*mm, H-9*mm, 'TEAM BRAIN STACK')
    # Bottom line
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(20*mm, 12*mm, W-20*mm, 12*mm)
    # Page number
    canvas.setFillColor(MID_GRAY)
    canvas.setFont('Helvetica', 8)
    canvas.drawCentredString(W/2, 7*mm, f'Page {doc.page}')
    canvas.restoreState()

# ─────────────────────────────────────────────
#  BUILD DOCUMENT
# ─────────────────────────────────────────────

def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=20*mm, bottomMargin=20*mm
    )
    s = build_styles()
    story = []

    # ══════════════════════════════════════
    # COVER PAGE
    # ══════════════════════════════════════
    story.append(Spacer(1, 35*mm))
    story.append(Paragraph("TEAM BRAIN STACK", s['cover_team']))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("ET AI-Native<br/>News Experience", s['cover_title']))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("A Multi-Agent System for Intelligent News Delivery", s['cover_sub']))
    story.append(Spacer(1, 8*mm))

    # Divider line
    hr = HRFlowable(width='60%', thickness=1, color=ET_RED, hAlign='CENTER', spaceAfter=8)
    story.append(hr)
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("ECONOMIC TIMES  ·  GEN AI HACKATHON 2026", s['cover_hackathon']))
    story.append(Spacer(1, 30*mm))

    # Cover info box
    s['cover_val'] = ParagraphStyle('cover_val', fontName='Helvetica', fontSize=9, textColor=WHITE, leading=13)
    s['cover_key'] = ParagraphStyle('cover_key', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE, leading=13)
    cover_data = [
        [Paragraph('Submitted by', s['cover_key']), Paragraph('Team Brain Stack', s['cover_val'])],
        [Paragraph('Event', s['cover_key']), Paragraph('ET Gen AI Hackathon 2026', s['cover_val'])],
        [Paragraph('Track', s['cover_key']), Paragraph('Problem Statement #8 — AI-Native News Experience', s['cover_val'])],
        [Paragraph('Solution', s['cover_key']), Paragraph('Multi-Agent AI News System (5 Agents)', s['cover_val'])],
        [Paragraph('Technology', s['cover_key']), Paragraph('Python · FastAPI · Groq API · LLaMA 3.3 70B', s['cover_val'])],
    ]
    cover_table = Table(cover_data, colWidths=[50*mm, 110*mm])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#1a1a1a')),
        ('TEXTCOLOR', (0,0), (0,-1), WHITE),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor('#222222')),
        ('TEXTCOLOR', (1,0), (1,-1), WHITE),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#333333')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(cover_table)
    story.append(PageBreak())

    # ══════════════════════════════════════
    # SECTION 1 — PROJECT OVERVIEW
    # ══════════════════════════════════════
    story += section_header(1, "Project Overview", s)

    story.append(highlight_box(
        '"Business news in 2026 is still delivered like it\'s 2005 — static text articles, '
        'one-size-fits-all homepage, same format for everyone. We built something that makes '
        'people say: I can\'t go back to reading news the old way."',
        s, bg=colors.HexColor('#FFF8F0'), border=ET_GOLD
    ))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("What We Built", s['sub_title']))
    story.append(Paragraph(
        "Team Brain Stack has developed an <b>AI-Native News Experience</b> — a multi-agent system "
        "that fundamentally reimagines how business news is consumed. Rather than displaying the same "
        "static content to every reader, our system uses five specialized AI agents that work together "
        "to personalize, synthesize, translate, track, and transform news content in real time.",
        s['body']
    ))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("The Five Agents at a Glance", s['sub_title']))
    agents_data = [
        [Paragraph('<b>Agent</b>', s['body']), Paragraph('<b>Name</b>', s['body']), Paragraph('<b>What it does</b>', s['body'])],
        [Paragraph('Agent 1', s['body']), Paragraph('Personalization Agent', s['body']),
         Paragraph('Ranks and filters news based on user role, interests, and reading context', s['body'])],
        [Paragraph('Agent 2', s['body']), Paragraph('Briefing Agent', s['body']),
         Paragraph('Synthesizes multiple articles on one topic into a single intelligent briefing', s['body'])],
        [Paragraph('Agent 3', s['body']), Paragraph('Story Arc Tracker', s['body']),
         Paragraph('Builds timelines, tracks sentiment shifts, and predicts what happens next', s['body'])],
        [Paragraph('Agent 4', s['body']), Paragraph('Vernacular Agent', s['body']),
         Paragraph('Culturally adapts news into Hindi, Tamil, Telugu, Bengali — not literal translation', s['body'])],
        [Paragraph('Agent 5', s['body']), Paragraph('Video Script Agent', s['body']),
         Paragraph('Transforms any article into a broadcast-quality 60–120 second video script', s['body'])],
    ]
    story.append(colored_table(agents_data, [20*mm, 45*mm, 95*mm]))
    story.append(PageBreak())

    # ══════════════════════════════════════
    # SECTION 2 — PROBLEM STATEMENT
    # ══════════════════════════════════════
    story += section_header(2, "Problem Statement", s)

    story.append(Paragraph("Why Today's News Delivery is Broken", s['sub_title']))
    story.append(Paragraph(
        "Despite massive advances in AI and personalization technology, most business news platforms "
        "in 2026 still operate on a fundamentally outdated model. The same homepage is served to every "
        "reader regardless of who they are, what they do, or what language they think in. "
        "This creates a massive gap between the information available and the information that actually "
        "reaches and benefits readers.",
        s['body']
    ))
    story.append(Spacer(1, 3*mm))

    problems = [
        ("1. No Personalization", "A mutual fund investor and a rural farmer see the exact same news feed. "
         "There is no mechanism to rank, filter, or adapt content based on the reader's profession, "
         "interests, or context."),
        ("2. Information Fragmentation", "A major event like the Union Budget generates 15-20 separate articles. "
         "Readers must spend 30+ minutes reading all of them to form a complete picture. "
         "There is no system to synthesize this into one coherent briefing."),
        ("3. English-Only Barrier", "Over 90% of India thinks and communicates in regional languages, yet "
         "business news is almost exclusively in English. Existing translation tools provide literal "
         "translations that fail to convey financial concepts meaningfully to regional audiences."),
        ("4. No Narrative Intelligence", "Ongoing stories like corporate controversies, policy changes, or "
         "market movements span months or years. No platform helps readers track the arc of these stories — "
         "how sentiment has shifted, who the key players are, and what to expect next."),
        ("5. Static Format", "News is delivered only as text articles. There is no automated mechanism to "
         "transform breaking news into video scripts, briefings, or other formats that suit different "
         "consumption patterns."),
    ]

    for title, desc in problems:
        story.append(KeepTogether([
            Paragraph(f"<b>{title}</b>", s['sub_title']),
            Paragraph(desc, s['body']),
        ]))

    story.append(Spacer(1, 3*mm))
    story.append(highlight_box(
        '<b>Core Insight:</b> The problem is not a lack of content — India has abundant quality journalism. '
        'The problem is that content delivery has not evolved. Our system builds the intelligence layer '
        'that sits on top of existing content and makes it work for every individual reader.',
        s, bg=colors.HexColor('#F0F7FF'), border=BLUE
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════
    # SECTION 3 — ARCHITECTURE
    # ══════════════════════════════════════
    story += section_header(3, "System Architecture & Agent Design", s)

    story.append(Paragraph("Multi-Agent Architecture Overview", s['sub_title']))
    story.append(Paragraph(
        "Our system follows a multi-agent architecture where each agent is an independent, "
        "specialized AI module with its own system prompt, input schema, and output format. "
        "Agents can be called independently or orchestrated together for complex tasks. "
        "All agents are powered by LLaMA 3.3 70B via the Groq API.",
        s['body']
    ))
    story.append(Spacer(1, 3*mm))

    # Architecture flow
    arch_data = [
        [Paragraph('<b>Layer</b>', s['body']), Paragraph('<b>Component</b>', s['body']), Paragraph('<b>Role</b>', s['body'])],
        [Paragraph('Input', s['body']), Paragraph('User Interface (HTML/JS)', s['body']),
         Paragraph('Accepts user inputs: profile, articles, topic, language preference', s['body'])],
        [Paragraph('Orchestration', s['body']), Paragraph('FastAPI Backend', s['body']),
         Paragraph('Routes requests to appropriate agents, runs agents in parallel where possible', s['body'])],
        [Paragraph('Intelligence', s['body']), Paragraph('5 Specialized AI Agents', s['body']),
         Paragraph('Each agent has a unique system prompt defining its role and output schema', s['body'])],
        [Paragraph('AI Engine', s['body']), Paragraph('Groq API + LLaMA 3.3 70B', s['body']),
         Paragraph('Processes all agent requests, returns structured JSON responses', s['body'])],
        [Paragraph('Output', s['body']), Paragraph('Rendered UI Cards', s['body']),
         Paragraph('Parsed JSON rendered as interactive news cards, timelines, scripts', s['body'])],
    ]
    story.append(colored_table(arch_data, [25*mm, 50*mm, 85*mm]))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Agent Design Details", s['sub_title']))

    agent_details = [
        ("Agent 1 — Personalization Agent",
         "Input: User profile (name, role, interests) + list of articles\n"
         "Process: Scores each article against user profile using semantic matching\n"
         "Output: Ranked articles with relevance score (0-100) and personalized explanation\n"
         "Key innovation: Role-aware ranking — a CFO and a student see completely different feeds"),

        ("Agent 2 — News Navigator / Briefing Agent",
         "Input: Topic name + multiple articles (up to 10)\n"
         "Process: Synthesizes all articles, extracts key sections, identifies players and sentiment\n"
         "Output: Single briefing with headline, TL;DR, insights, contrarian view, follow-up questions\n"
         "Key innovation: Replaces 8 articles with 1 explorable briefing — saves 25+ minutes"),

        ("Agent 3 — Story Arc Tracker",
         "Input: Story name + chronological list of events/articles\n"
         "Process: Builds narrative arc, tracks sentiment shift, identifies story phase\n"
         "Output: Timeline, sentiment arc, contrarian perspectives, predictions\n"
         "Key innovation: Turns months of coverage into a single navigable story map"),

        ("Agent 4 — Vernacular Agent",
         "Input: Article title + content + target language + reader context\n"
         "Process: Cultural adaptation using local analogies, idioms, and context-specific impact\n"
         "Output: Translated title, adapted article, local analogy, key terms explained\n"
         "Key innovation: Adapts financial concepts using local metaphors (farming, local markets)"),

        ("Agent 5 — Video Script Agent",
         "Input: Article title + content + target duration (60-120 seconds)\n"
         "Process: Structures content into broadcast segments with visual directions\n"
         "Output: Hook, timestamped segments, narration, visual directions, closing line, stats\n"
         "Key innovation: Any article becomes a broadcast-ready script in under 10 seconds"),
    ]

    for title, detail in agent_details:
        lines = detail.split('\n')
        story.append(KeepTogether([
            Paragraph(f"<b>{title}</b>", s['sub_title']),
            *[Paragraph(f"• {line.strip()}", s['bullet']) for line in lines if line.strip()],
            Spacer(1, 2*mm),
        ]))

    story.append(PageBreak())

    # ══════════════════════════════════════
    # SECTION 4 — TECH STACK
    # ══════════════════════════════════════
    story += section_header(4, "Technology Stack", s)

    story.append(Paragraph("Core Technologies", s['sub_title']))

    tech_data = [
        [Paragraph('<b>Category</b>', s['body']), Paragraph('Technology', s['cover_key']), Paragraph('<b>Purpose</b>', s['body'])],
        [Paragraph('AI Engine', s['body']), Paragraph('Groq API + LLaMA 3.3 70B', s['body']),
         Paragraph('Powers all 5 agents — fast inference, free tier available', s['body'])],
        [Paragraph('Backend', s['body']), Paragraph('Python + FastAPI', s['body']),
         Paragraph('REST API layer, agent orchestration, parallel execution with asyncio', s['body'])],
        [Paragraph('Frontend', s['body']), Paragraph('HTML5 + CSS3 + Vanilla JS', s['body']),
         Paragraph('Single-file demo UI with 5 tabbed agent interfaces', s['body'])],
        [Paragraph('Data Format', s['body']), Paragraph('JSON (structured outputs)', s['body']),
         Paragraph('All agent responses are structured JSON — easy to parse and render', s['body'])],
        [Paragraph('Fonts', s['body']), Paragraph('Google Fonts (Playfair Display, IBM Plex Mono)', s['body']),
         Paragraph('Editorial aesthetic matching ET brand identity', s['body'])],
        [Paragraph('Deployment', s['body']), Paragraph('Browser-based (no server needed for demo)', s['body']),
         Paragraph('Single HTML file runs entirely in the browser for hackathon demo', s['body'])],
    ]
    story.append(colored_table(tech_data, [30*mm, 50*mm, 80*mm]))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Why Groq + LLaMA 3.3 70B?", s['sub_title']))
    reasons = [
        "Free tier with generous rate limits — suitable for hackathon and prototyping",
        "LLaMA 3.3 70B produces high-quality structured JSON outputs reliably",
        "Extremely low latency (typically under 2 seconds per agent call)",
        "Open-weight model — can be self-hosted for production deployment",
        "Supports all Indian languages required for the Vernacular Agent",
    ]
    for r in reasons:
        story.append(Paragraph(f"• {r}", s['bullet']))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("System Requirements", s['sub_title']))
    req_data = [
        [Paragraph('<b>Requirement</b>', s['body']), Paragraph('<b>Specification</b>', s['body'])],
        [Paragraph('Python Version', s['body']), Paragraph('Python 3.10+', s['body'])],
        [Paragraph('Key Dependencies', s['body']), Paragraph('fastapi, uvicorn, groq, pydantic, httpx', s['body'])],
        [Paragraph('API Key', s['body']), Paragraph('Groq API Key (free at console.groq.com)', s['body'])],
        [Paragraph('Browser', s['body']), Paragraph('Any modern browser (Chrome, Firefox, Edge)', s['body'])],
        [Paragraph('Internet', s['body']), Paragraph('Required for API calls to Groq', s['body'])],
    ]
    story.append(colored_table(req_data, [50*mm, 110*mm]))
    story.append(PageBreak())

    # ══════════════════════════════════════
    # SECTION 5 — DIFFERENTIATION
    # ══════════════════════════════════════
    story += section_header(5, "How We Are Different", s)

    story.append(Paragraph("Traditional News Platform vs. Our System", s['sub_title']))

    comparison_data = [
        [Paragraph('<b>Feature</b>', s['body']),
         Paragraph('<b>Traditional Platform</b>', s['body']),
         Paragraph('<b>Our AI System</b>', s['body'])],
        [Paragraph('News Feed', s['body']),
         Paragraph('Same for all users', s['body']),
         Paragraph('Personalized by role + interests', s['body'])],
        [Paragraph('Multiple articles on 1 topic', s['body']),
         Paragraph('Read all 8 separately', s['body']),
         Paragraph('1 synthesized briefing with insights', s['body'])],
        [Paragraph('Language', s['body']),
         Paragraph('English only', s['body']),
         Paragraph('4 regional languages, culturally adapted', s['body'])],
        [Paragraph('Story tracking', s['body']),
         Paragraph('Manual — read 50 articles', s['body']),
         Paragraph('Auto timeline + sentiment arc + predictions', s['body'])],
        [Paragraph('Content formats', s['body']),
         Paragraph('Text articles only', s['body']),
         Paragraph('Articles + Briefings + Video scripts', s['body'])],
        [Paragraph('User intelligence', s['body']),
         Paragraph('No understanding of reader', s['body']),
         Paragraph('Role-aware, context-aware delivery', s['body'])],
        [Paragraph('Regional coverage', s['body']),
         Paragraph('Same national content', s['body']),
         Paragraph('Local impact explained per reader type', s['body'])],
        [Paragraph('Data usage', s['body']),
         Paragraph('Stores data only', s['body']),
         Paragraph('Uses data to generate intelligence', s['body'])],
    ]

    t = Table(comparison_data, colWidths=[45*mm, 60*mm, 55*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), INK),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BACKGROUND', (1,1), (1,-1), colors.HexColor('#FFF0F0')),
        ('BACKGROUND', (2,1), (2,-1), colors.HexColor('#F0FFF4')),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.3, RULE),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (0,-1), [LIGHT_BG, WHITE]),
        ('TEXTCOLOR', (0,0), (0,-1), DARK_GRAY),
        ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
    ]))
    story.append(t)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("Key Differentiators", s['sub_title']))

    differentiators = [
        ("Cultural Intelligence, Not Just Translation",
         "Our Vernacular Agent does not use dictionary-based translation. It uses LLaMA 3.3 70B to "
         "understand the financial concept, then re-explains it using analogies familiar to the target "
         "reader — a farmer understands repo rate through crop loan analogies, not banking terminology."),

        ("Agent Specialization for Quality",
         "Each of our 5 agents has a unique, carefully crafted system prompt that makes it an expert "
         "in its specific task. This specialization produces significantly higher quality outputs than "
         "a single general-purpose AI prompt."),

        ("Real-Time Synthesis at Scale",
         "Our Briefing Agent can synthesize up to 10 articles into a single coherent briefing in under "
         "5 seconds. This is not summarization — it extracts cross-article insights, identifies "
         "contrarian views, and generates intelligent follow-up questions."),

        ("Narrative Intelligence",
         "The Story Arc Tracker is unique in the news industry. It understands stories as living "
         "narratives with phases (emerging → developing → peak → resolving → resolved), tracks "
         "how sentiment has shifted over time, and surfaces perspectives that mainstream coverage misses."),
    ]

    for title, desc in differentiators:
        story.append(KeepTogether([
            Paragraph(f"<b>{title}</b>", s['sub_title']),
            Paragraph(desc, s['body']),
        ]))

    story.append(PageBreak())

    # ══════════════════════════════════════
    # SECTION 6 — FUTURE SCOPE
    # ══════════════════════════════════════
    story += section_header(6, "Future Scope & Roadmap", s)

    story.append(Paragraph(
        "The current implementation is a proof-of-concept demonstrating the core multi-agent "
        "architecture. The following enhancements are planned for production deployment:",
        s['body']
    ))
    story.append(Spacer(1, 3*mm))

    roadmap_data = [
        [Paragraph('<b>Phase</b>', s['body']), Paragraph('<b>Feature</b>', s['body']), Paragraph('<b>Description</b>', s['body'])],
        [Paragraph('Phase 2', s['body']), Paragraph('Live ET Article Integration', s['body']),
         Paragraph('Connect directly to ET RSS feeds and APIs for real-time news processing', s['body'])],
        [Paragraph('Phase 2', s['body']), Paragraph('User Profile Learning', s['body']),
         Paragraph('Track reading history to improve personalization over time', s['body'])],
        [Paragraph('Phase 3', s['body']), Paragraph('Recommendation Engine', s['body']),
         Paragraph('ML-based book/article recommendation using user borrowing and review data', s['body'])],
        [Paragraph('Phase 3', s['body']), Paragraph('Audio Briefings', s['body']),
         Paragraph('Convert text briefings to audio using TTS for commute listening', s['body'])],
        [Paragraph('Phase 4', s['body']), Paragraph('Actual Video Generation', s['body']),
         Paragraph('Use AI video tools to generate actual news videos from scripts', s['body'])],
        [Paragraph('Phase 4', s['body']), Paragraph('More Regional Languages', s['body']),
         Paragraph('Expand to Marathi, Gujarati, Kannada, Malayalam, Punjabi', s['body'])],
    ]
    story.append(colored_table(roadmap_data, [20*mm, 48*mm, 92*mm]))
    story.append(Spacer(1, 5*mm))

    story.append(highlight_box(
        '<b>Vision:</b> Every person in India — regardless of their language, profession, or level of '
        'financial literacy — deserves access to business news that is relevant, understandable, and '
        'actionable for their specific life. Our multi-agent system is the foundation for that vision.',
        s, bg=colors.HexColor('#F0F7FF'), border=BLUE
    ))
    story.append(Spacer(1, 5*mm))

    # Closing
    story.append(divider(ET_RED, 1.5))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Team Brain Stack  ·  ET Gen AI Hackathon 2026", ParagraphStyle(
        'closing', fontName='Helvetica-Bold', fontSize=10,
        textColor=ET_RED, alignment=TA_CENTER, spaceAfter=4
    )))
    story.append(Paragraph(
        "Thank you for the opportunity to reimagine how India reads business news.",
        ParagraphStyle('closing2', fontName='Helvetica-Oblique', fontSize=9,
                       textColor=MID_GRAY, alignment=TA_CENTER)
    ))

    # BUILD
    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    print(f"PDF saved: {output_path}")

build_pdf('/mnt/user-data/outputs/BrainStack_ET_Hackathon_Submission.pdf')
