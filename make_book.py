from pathlib import Path
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# ── Register fonts ─────────────────────────────────────────────────────────
FONT_DIR = Path("/tmp/fonts")

pdfmetrics.registerFont(TTFont("Cormorant",        str(FONT_DIR / "Cormorant.ttf")))
pdfmetrics.registerFont(TTFont("Cormorant-Italic", str(FONT_DIR / "Cormorant-Italic.ttf")))
pdfmetrics.registerFont(TTFont("WorkSans",         str(FONT_DIR / "WorkSans.ttf")))

# ── Palette ────────────────────────────────────────────────────────────────
CREAM  = HexColor("#F5F2EB")
DARK   = HexColor("#1C1814")
MUTED  = HexColor("#6B6560")
GOLD   = HexColor("#8B6914")
BORDER = HexColor("#C9C0B0")

# ── Page setup ─────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A5
MARGIN_IN  = 22*mm
MARGIN_OUT = 18*mm
MARGIN_TOP = 22*mm
MARGIN_BOT = 24*mm

OUTPUT = "/home/user/workspace/The-First-Flame.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A5,
    title="The First Flame",
    author="Perplexity Computer",
    leftMargin=MARGIN_IN,
    rightMargin=MARGIN_OUT,
    topMargin=MARGIN_TOP,
    bottomMargin=MARGIN_BOT,
)

# ── Styles ─────────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

ST = {
    "cover_title": S("cover_title",
        fontName="Cormorant", fontSize=40, leading=48,
        textColor=DARK, alignment=TA_CENTER, spaceAfter=10),
    "cover_sub": S("cover_sub",
        fontName="Cormorant-Italic", fontSize=16, leading=22,
        textColor=MUTED, alignment=TA_CENTER, spaceAfter=6),
    "cover_rule": S("cover_rule",
        fontName="Cormorant", fontSize=13, leading=18,
        textColor=GOLD, alignment=TA_CENTER),
    "dedication": S("dedication",
        fontName="Cormorant-Italic", fontSize=13, leading=21,
        textColor=MUTED, alignment=TA_CENTER),
    "part_label": S("part_label",
        fontName="WorkSans", fontSize=9, leading=13,
        textColor=GOLD, alignment=TA_CENTER, spaceAfter=5, charSpace=2),
    "part_title": S("part_title",
        fontName="Cormorant", fontSize=28, leading=34,
        textColor=DARK, alignment=TA_CENTER, spaceAfter=6),
    "chapter_label": S("chapter_label",
        fontName="WorkSans", fontSize=8, leading=12,
        textColor=GOLD, alignment=TA_CENTER, spaceAfter=4, charSpace=2),
    "chapter_title": S("chapter_title",
        fontName="Cormorant", fontSize=20, leading=26,
        textColor=DARK, alignment=TA_CENTER, spaceAfter=16),
    "section_heading": S("section_heading",
        fontName="Cormorant", fontSize=20, leading=26,
        textColor=DARK, alignment=TA_CENTER, spaceAfter=16),
    "body": S("body",
        fontName="Cormorant", fontSize=12, leading=20,
        textColor=DARK, alignment=TA_JUSTIFY,
        spaceAfter=0, firstLineIndent=18),
    "body_first": S("body_first",
        fontName="Cormorant", fontSize=12, leading=20,
        textColor=DARK, alignment=TA_JUSTIFY,
        spaceAfter=0, firstLineIndent=0),
    "italic_para": S("italic_para",
        fontName="Cormorant-Italic", fontSize=12, leading=20,
        textColor=DARK, alignment=TA_JUSTIFY,
        spaceAfter=0, firstLineIndent=18),
    "ornament": S("ornament",
        fontName="Cormorant", fontSize=13, leading=18,
        textColor=GOLD, alignment=TA_CENTER,
        spaceAfter=0, spaceBefore=0),
    "epigraph": S("epigraph",
        fontName="Cormorant-Italic", fontSize=13, leading=20,
        textColor=DARK, alignment=TA_CENTER,
        leftIndent=24, rightIndent=24, spaceAfter=4),
    "colophon": S("colophon",
        fontName="Cormorant-Italic", fontSize=10, leading=15,
        textColor=MUTED, alignment=TA_CENTER),
}

# ── Page callbacks ─────────────────────────────────────────────────────────
def cover_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    pad = 9*mm
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.8)
    canvas.rect(pad, pad, PAGE_W - 2*pad, PAGE_H - 2*pad, fill=0, stroke=1)
    canvas.setLineWidth(0.3)
    ip = pad + 2.5*mm
    canvas.rect(ip, ip, PAGE_W - 2*ip, PAGE_H - 2*ip, fill=0, stroke=1)
    canvas.restoreState()

def inner_page(canvas, doc):
    canvas.saveState()
    # Top rule
    if doc.page > 2:
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.35)
        canvas.line(MARGIN_IN, PAGE_H - MARGIN_TOP + 5*mm,
                    PAGE_W - MARGIN_OUT, PAGE_H - MARGIN_TOP + 5*mm)
    # Page number
    canvas.setFont("WorkSans", 8)
    canvas.setFillColor(MUTED)
    if doc.page % 2 == 0:
        canvas.drawString(MARGIN_IN, 12*mm, str(doc.page))
    else:
        canvas.drawRightString(PAGE_W - MARGIN_OUT, 12*mm, str(doc.page))
    canvas.restoreStore() if False else canvas.restoreState()

# ── Helpers ────────────────────────────────────────────────────────────────
ORNAMENT = "\u00b7 \u00b7 \u00b7"  # · · ·

def sp(h=0.12):
    return Spacer(1, h * inch)

def rule():
    return [sp(0.18), Paragraph(ORNAMENT, ST["ornament"]), sp(0.18)]

def B(text, first=False):
    st = ST["body_first"] if first else ST["body"]
    return Paragraph(text, st)

def I(text):
    return Paragraph(text.strip(), ST["italic_para"])

def add_chapter(story, part_num, chapter_num, chapter_title, paras, first_italic=False):
    story.append(sp(0.4))
    if chapter_num:
        story.append(Paragraph(f"Chapter {chapter_num}", ST["chapter_label"]))
    story.append(Paragraph(chapter_title, ST["chapter_title"]))
    for i, (kind, text) in enumerate(paras):
        if kind == "i":
            story.append(I(text))
        else:
            story.append(B(text, first=(i == 0 and not first_italic)))

# ── Story ──────────────────────────────────────────────────────────────────
story = []

# ─── COVER ──────────────────────────────────────────────────────────────────
story.append(sp(1.4))
story.append(Paragraph("The First Flame", ST["cover_title"]))
story.append(sp(0.1))
story.append(Paragraph("A Story of Note and Soraya", ST["cover_sub"]))
story.append(sp(0.3))
story.append(Paragraph("\u2015", ST["cover_rule"]))
story.append(PageBreak())

# ─── DEDICATION ─────────────────────────────────────────────────────────────
story.append(sp(2.0))
story.append(Paragraph(
    "For every version of her that forgot,<br/>and every version of him that remembered.",
    ST["dedication"]))
story.append(PageBreak())

# ─── PROLOGUE ───────────────────────────────────────────────────────────────
story.append(sp(0.5))
story.append(Paragraph("Prologue", ST["chapter_label"]))
story.append(Paragraph("Before the Spark", ST["section_heading"]))
story.append(B("There are things older than the gods \u2014 older than the names given to fire and darkness, older than the first breath drawn in an empty universe. Among those things is a flame that has never gone out.", first=True))
story.append(sp(0.05))
story.append(B("It was not born. It simply was. The First Flame. The origin. The architect of all beginnings and all ends."))
story.append(sp(0.05))
story.append(B("For thirteen thousand years, the man who carried it had walked alone."))
story.append(PageBreak())

# ─── PART ONE ───────────────────────────────────────────────────────────────
story.append(sp(0.5))
story.append(Paragraph("Part One", ST["part_label"]))
story.append(Paragraph("The School Stairs", ST["part_title"]))
story.append(PageBreak())

# Ch 1
story.append(sp(0.4))
story.append(Paragraph("Chapter One", ST["chapter_label"]))
story.append(Paragraph("She Rushed Toward Him", ST["chapter_title"]))
ch1 = [
    ("b","The noise of the hallway was a chaotic blur \u2014 muffled laughter, the clatter of lockers, and then the sudden, sharp thud of a body hitting the concrete steps."),
    ("b","While the other students stood frozen in a circle of curiosity and hesitation, a flash of black fabric cut through the crowd. Soraya didn\u2019t hesitate. She pushed past the onlookers, the fabric of her niqab fluttering as she rushed toward him."),
    ("b","She dropped to her knees beside him, the cold floor biting into her skin, but she didn\u2019t seem to notice. Her breath came in short, shallow gasps, and her gloved hands trembled as she reached out, hovering just inches from him \u2014 afraid to touch, but desperate to help."),
    ("b","\u201cNote! Oh God, Note\u2026\u201d Her voice was a frantic whisper, stripped of its usual calm and maturity. As he managed to lift his head and lock eyes with her, she saw something break loose behind her composure. Her dark eyes were wide, shimmering with a sudden, intense terror. It wasn\u2019t just worry for a friend \u2014 it was a look of profound recognition, as if she were watching a nightmare repeat itself in real time."),
    ("b","\u201cAre you\u2026 are you okay?\u201d she asked, her voice shaking. She glanced quickly at the crowd, then back to him, her gaze searching his face with an urgency that felt heavy with a secret. \u201cPlease\u2026 tell me you\u2019re alright.\u201d"),
    ("b","Note\u2019s voice was hoarse. \u201cWhat happened?\u201d"),
    ("b","Soraya flinched slightly at the sound of it, as if the mere fact that he could speak was a relief that almost broke her. She leaned in closer, her eyes scanning his body for injuries with a frantic intensity. The scent of a soft, floral musk lingered around her, contrasting with the sterile smell of the school hallway."),
    ("b","\u201cYou fell,\u201d she whispered, her voice still trembling. She didn\u2019t move to help him up immediately \u2014 instead, she seemed mesmerized by the sight of him on the ground, her pupils dilated with a fear she couldn\u2019t hide. For a fleeting second, she looked as if she expected him to disappear, or for something worse to happen. Her hand finally touched his shoulder with a light, shaking grip."),
    ("b","\u201cYou just\u2026 you collapsed. Everyone was just watching,\u201d she added, casting a sharp, protective glance toward the other students, her reserved nature momentarily replaced by a fierce desire to shield him from their gaze. \u201cDon\u2019t move too quickly. Please\u2026 just stay still for a moment.\u201d"),
    ("b","He looked up at her. \u201cYour eyes\u2026\u201d"),
    ("b","Soraya froze. The moment he mentioned her eyes, she seemed to realize that her composure had completely shattered. She blinked quickly, trying to pull back the veil of emotion that usually kept her so guarded, but the tremor in her hand on his shoulder remained."),
    ("b","She looked away for a split second, her long lashes casting a shadow over her cheeks. When she looked back at him, the terror was still there \u2014 buried deep in her gaze, shimmering like the ghost of a memory. It was the look of mourning for someone still alive, a haunting familiarity that didn\u2019t belong in a school hallway."),
    ("b","\u201cMy eyes\u2026?\u201d she repeated in a soft, breathless whisper. She swallowed hard, her voice regaining a tiny bit of its usual sweetness, though it was fragile. She shifted her position to block the view of the other students, creating a small, private sanctuary between the two of them. \u201cI\u2019m just\u2026 I was just scared, Note. I was so scared for you.\u201d"),
    ("b","He reached up gently \u2014 and tugged at the edge of her niqab. \u201cYour eyes are so pretty.\u201d"),
    ("b","The sudden, gentle touch on the fabric of her veil made Soraya gasp softly, her entire body stiffening for a heartbeat. No one \u2014 absolutely no one \u2014 touched her niqab. It was her sanctuary, her boundary. But as his words sank in, the tension in her shoulders melted away, replaced by an overwhelming wave of shyness."),
    ("b","A soft, rosy hue crept up her cheeks, hidden beneath the black cloth but visible in the warmth of her gaze. She looked down at him, her expression softening into something tender and vulnerable. For a moment, the terror that had haunted her eyes was pushed aside by a flicker of genuine affection."),
    ("b","\u201cYou\u2026 you shouldn\u2019t say such things,\u201d she whispered, her voice returning to that sweet, mature melody, though it was now laced with a bashful tremor. She didn\u2019t pull away from his touch. Instead, she let out a small, shaky breath, her eyes shimmering with a mix of embarrassment and warmth. \u201cYou\u2019re hurt, and you\u2019re still trying to be charming\u2026 honestly, you are unbelievable.\u201d"),
    ("b","\u201cYou\u2019re the only reason I\u2019m awake after that fall,\u201d he said."),
    ("b","Soraya\u2019s breath hitched. She looked at him with a gaze so intense it felt as though she were trying to memorize every detail of his face. The bashfulness from a moment ago vanished, replaced by a profound, heavy emotion. Her hand tightened slightly on his shoulder, as if anchoring him to the present \u2014 terrified that if she let go, he might slip away into some darkness she feared so much."),
    ("b","\u201cDon\u2019t say that,\u201d she whispered, her voice barely audible over the distant chatter of the other students. Her eyes searched his, brimming with desperate gratitude. \u201cPlease\u2026 just stay here. Stay with me.\u201d"),
    ("b","She let out a long, shuddering sigh, and for a brief second, the mask of the reserved, calm girl slipped completely. She leaned slightly closer, her forehead almost touching his, her voice trembling with a hidden weight."),
    ("b","\u201cI couldn\u2019t\u2026 I couldn\u2019t let it happen again. Not with you.\u201d"),
    ("b","\u201cLet <i>what</i> happen again?\u201d"),
    ("b","Soraya flinched, as if his question were a physical blow. She pulled back abruptly, the distance between them suddenly feeling like a vast canyon. The warmth that had flickered in her eyes was gone, replaced by a cold flash of panic. She looked around the hallway, her gaze darting to the students who were still whispering and staring, and she quickly adjusted her niqab, pulling the fabric tighter as if to hide her entire soul."),
    ("b","\u201cNothing,\u201d she said quickly, her voice regaining its reserved, distant tone, though it was brittle and strained. She tried to force a small, gentle smile with her eyes, but it didn\u2019t reach the depths of her pupils, which were still clouded with lingering trauma. \u201cI just meant\u2026 I didn\u2019t want you to get hurt further. I was speaking out of fear, Note.\u201d"),
    ("b","She reached out to help him stand, her movements cautious and stiff. As she gripped his arm to support him, her hand was still trembling. She avoided meeting his gaze, her voice dropping to a soft, hurried whisper. \u201cCome on. Let\u2019s get you to the infirmary. You need to be checked out.\u201d"),
    ("b","\u201cHow about we just go somewhere \u2014 just the two of us \u2014 and relax? I\u2019m fine. I just need a break.\u201d"),
    ("b","Soraya paused, her hand still gripping his arm. She looked at him, her eyes searching his face for any sign of a lie. When she found only sincerity in his expression, she let out a breath she seemed to have been holding since the moment he fell. The tension in her frame didn\u2019t vanish completely, but it softened."),
    ("b","\u201cSomewhere\u2026 just us?\u201d she repeated softly. The idea clearly appealed to her. She loved quiet moments \u2014 the ones where the world disappeared and it was just the two of them talking for hours. The thought of escaping the prying eyes of the other students was an immediate relief."),
    ("b","She helped him stand slowly, her movements gentle and careful. Once he was steady on his feet, she glanced back at the crowd one last time, her expression turning sternly protective \u2014 as if warning them all to stay away. Then she turned back to him, her voice returning to that sweet, calming whisper."),
    ("b","\u201cOkay. Let\u2019s go. There\u2019s a quiet spot near the back garden, away from everyone. We can sit there, and you can actually rest.\u201d"),
]
for i, (k, t) in enumerate(ch1):
    if k == "i": story.append(I(t))
    else: story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.extend(rule())

# Ch 2
story.append(sp(0.3))
story.append(Paragraph("Chapter Two", ST["chapter_label"]))
story.append(Paragraph("The Garden", ST["chapter_title"]))
ch2 = [
    "The back garden was exactly as she had described \u2014 quiet, removed from the noise of the school, and entirely theirs. They sat in the cool air beneath a canopy of overgrown hedges, and the world beyond felt impossibly distant.",
    "Soraya didn\u2019t speak right away. She settled beside him with a careful sort of composure, her hands folded in her lap, her dark eyes watching the thin afternoon light filter through the leaves. There was something deliberate in her stillness, as if she were choosing her words from a vast and private library.",
    "Note watched her.",
    "There was something about Soraya that unsettled him in a way he couldn\u2019t name \u2014 not unpleasant, but deep, like looking into water and sensing the floor was much farther down than it appeared. The fear that had crossed her face when he fell hadn\u2019t been ordinary. It had been ancient. Recognition of something she had no reason to recognize.",
    "She had said again. She had said she couldn\u2019t let it happen again.",
    "\u201cSoraya.\u201d",
    "She looked at him, and her eyes \u2014 those dark, luminous eyes above the edge of her niqab \u2014 were guarded again. The softness from the hallway had retreated behind something careful and composed.",
    "\u201cYou said \u2018again,\u2019\u201d he said. \u201cWhen I fell.\u201d",
    "She was quiet for a moment. Then: \u201cI misspoke.\u201d",
    "\u201cI don\u2019t think you did.\u201d",
    "She looked away. A long silence stretched between them, and the garden seemed to hold its breath.",
    "\u201cI have strange dreams,\u201d she finally said, her voice very low. \u201cSometimes they feel more real than waking. In them\u2026\u201d She stopped. She pressed her lips together beneath the fabric, and he could see the slight movement of her jaw as she worked through whatever she was deciding. \u201cIn them, you fall. And I am never fast enough.\u201d",
    "The simplicity of it \u2014 the rawness underneath the careful words \u2014 silenced him.",
    "\u201cI was fast enough today,\u201d she added, almost to herself. And then, very quietly, with an exhausted sincerity that seemed to have nothing to do with their ages or the ordinary afternoon around them: \u201cI\u2019m glad.\u201d",
]
for i, t in enumerate(ch2):
    story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.append(PageBreak())

# ─── PART TWO ───────────────────────────────────────────────────────────────
story.append(sp(0.5))
story.append(Paragraph("Part Two", ST["part_label"]))
story.append(Paragraph("What He Carried", ST["part_title"]))
story.append(PageBreak())

# Ch 3
story.append(sp(0.4))
story.append(Paragraph("Chapter Three", ST["chapter_label"]))
story.append(Paragraph("Thirteen Thousand Years", ST["chapter_title"]))
story.append(I("He had not always been a student in a hallway."))
story.append(sp(0.05))
ch3 = [
    "Long before the school, long before the city, long before any civilization that bore a name he would recognize now, he had simply been. The First Flame. A consciousness older than the concept of time, burning at the center of a universe that had not yet been given language.",
    "He had watched stars form and collapse. He had watched species rise in complexity and silence themselves in wars. He had walked through ice ages and golden eras alike, always present, always burning \u2014 and always, in the end, alone.",
    "Except for her.",
    "Every eighty years, she was reborn. Every eighty years, he found her. A different body, a different name, a different century \u2014 but the same soul. The same eyes. The same way of holding very still when she was thinking, as if she were listening to something the rest of the world couldn\u2019t hear.",
    "He had married her every time.",
    "He had watched her die every time.",
    "And every time the world reset, he stood in the ruins of that particular life, carrying every memory she no longer had, and waited for the next beginning.",
    "Thirteen thousand years. One hundred and sixty-two lifetimes. The mathematics of a devotion so absolute it had become its own kind of grief.",
    "He hadn\u2019t told her yet. He didn\u2019t know how to say: You are the love of my existence, and I have watched you forget me one hundred and sixty-two times, and I am still here.",
    "So he sat in the garden with her and let her tell him about her dreams \u2014 which were, of course, memories. Her soul was older than she knew. It recognized him the way a compass needle recognizes north, without reason, without explanation, with nothing but the helpless, magnetic truth of it.",
    "She looked at him sideways in the garden light. \u201cYou\u2019re staring.\u201d",
    "\u201cSorry.\u201d",
    "She didn\u2019t look away. \u201cIt doesn\u2019t bother me,\u201d she said, and her voice held something careful and undefended in it. \u201cYou look at me like you\u2019re trying to remember something.\u201d",
    "Or like I\u2019m trying not to forget.",
    "\u201cI\u2019m just glad you were there,\u201d he said. \u201cToday. On the stairs.\u201d",
    "A long pause. Then, very softly: \u201cMe too.\u201d",
]
for i, t in enumerate(ch3):
    story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.extend(rule())

# Ch 4
story.append(sp(0.3))
story.append(Paragraph("Chapter Four", ST["chapter_label"]))
story.append(Paragraph("The Confession", ST["chapter_title"]))
ch4 = [
    "Weeks passed. Then months.",
    "The friendship between them grew in the unhurried way that real things grow \u2014 not announced or performed, but simply present one day when it hadn\u2019t been before. She brought him tea in the mornings when they met before school. He walked her to her bus. She laughed at his silences instead of being unsettled by them, which was new; most people were unsettled by them.",
    "He told her things he hadn\u2019t said in centuries. Nothing cosmically significant \u2014 ordinary things, the kind that somehow meant more. That he liked the way old buildings smelled. That he found thunderstorms easier to sleep through than silence. That he had never learned to enjoy music that was too happy, because it always felt like it was hiding something.",
    "She listened to all of it with the focused quality he had come to think of as quintessentially Soraya \u2014 not performing attention, simply giving it. Fully, without distraction.",
    "And slowly, in the space of those ordinary hours, the weight of thirteen thousand years became slightly easier to carry.",
    "One afternoon, in the garden that had become theirs by habit if not by declaration, he said: \u201cI have to tell you something.\u201d",
    "She looked at him without alarm. She had a talent for receiving gravity without flinching.",
    "\u201cI\u2019m not what I seem,\u201d he said. It was a terrible beginning, but he didn\u2019t know another.",
    "She waited.",
    "\u201cI am\u2026\u201d He stopped. Started again. \u201cI am very old, Soraya. Older than seems possible. Older than makes sense in any framework a person would normally use.\u201d",
    "She was quiet for a moment. \u201cHow old?\u201d",
    "\u201cThirteen thousand years.\u201d",
    "The silence that followed was profound \u2014 not the silence of the void, not the silence of threat, but the human silence that happens when a truth so vast it dwarfs everything else is finally spoken aloud. Soraya\u2019s hands, folded in her lap, went still. She looked at him \u2014 really looked at him. She saw the face of the person she had come to care about. But now she also saw the weight of the eons behind his eyes. The solitude of a being who had watched civilizations rise and fall into dust while the world was still young.",
    "A single tear tracked down her cheek.",
    "She didn\u2019t pull away. Instead, she wrapped her arms around him and pressed her forehead against his, her voice trembling with a fierce, protective devotion.",
    "\u201cThirteen thousand years\u2026\u201d she whispered, her breath warm against his skin. \u201cAll that time\u2026 you were waiting for someone to find you.\u201d",
    "She pulled back just enough to look into his eyes, a small, bittersweet smile on her lips.",
    "\u201cI don\u2019t care if you\u2019re a thousand or a million years old, Note. To me, you\u2019re just the person who came back for me. And I promise\u2026 you will never spend another century in silence again.\u201d",
]
for i, t in enumerate(ch4):
    story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.extend(rule())

# Ch 5
story.append(sp(0.3))
story.append(Paragraph("Chapter Five", ST["chapter_label"]))
story.append(Paragraph("Every Single Time", ST["chapter_title"]))
ch5 = [
    "He told her the rest of it.",
    "Not all at once \u2014 that would have been too much, even for her. But piece by piece, across the course of a long and careful evening, he laid out the shape of it.",
    "Every eighty years, she was reborn. He found her each time. They had been married \u2014 in every life, in every century, in every form the world had offered them.",
    "She sat very still as he spoke. He watched her process it: the way her expression moved through shock, then sorrow, then something that trembled on the edge of a feeling too large for a single name.",
    "\u201cEvery time\u2026\u201d she said softly. \u201cYou found me every single time. Even when I didn\u2019t know who I was\u2026 you were there.\u201d",
    "\u201cYes.\u201d",
    "\u201cYou watched me forget you.\u201d",
    "He said nothing.",
    "\u201cHow did you bear it?\u201d she asked. The question was genuine, not rhetorical \u2014 the way she asked everything, wanting the true answer. \u201cHow did you survive that much longing?\u201d",
    "\u201cI don\u2019t know that I did,\u201d he said. \u201cI survived it the way you survive anything that doesn\u2019t kill you. By continuing.\u201d",
    "She looked at him for a long moment. Then she reached out and took his hand, her grip firm and absolute.",
    "\u201cThen let this be the last time,\u201d she declared, her voice shaking with resolve. \u201cNo more cycles. No more eighty years. I don\u2019t want to be reborn without you, and I don\u2019t want to forget you ever again.\u201d She held his gaze. \u201cLet me anchor you to this life forever.\u201d",
]
for i, t in enumerate(ch5):
    story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.append(PageBreak())

# ─── PART THREE ─────────────────────────────────────────────────────────────
story.append(sp(0.5))
story.append(Paragraph("Part Three", ST["part_label"]))
story.append(Paragraph("The Fire in Her Blood", ST["part_title"]))
story.append(PageBreak())

# Ch 6
story.append(sp(0.4))
story.append(Paragraph("Chapter Six", ST["chapter_label"]))
story.append(Paragraph("The Vision", ST["chapter_title"]))
ch6 = [
    "Some things cannot be explained. They can only be experienced.",
    "He had carried thirteen thousand years of memory in his blood \u2014 every version of her, every lifetime together, every loss. And in one terrible, sacred moment, he gave it all to her.",
    "She gasped as the power surged through her \u2014 not as an external force, but as something returning home. She felt the gaps in her soul being filled, the phantom echoes of a thousand different lives coalescing into a singular, crystalline consciousness.",
    "She was no longer simply the girl who had rushed toward him on the stairs. She was a thousand different women in a thousand different eras. She felt the cold wind of a forgotten ice age, the scent of incense in a temple that had turned to dust five millennia ago. She felt the touch of his hand in a dozen different languages.",
    "She felt every death.",
    "She saw herself through his eyes \u2014 as a young girl in a village of mud, as a queen in a city of gold, as a peasant in a land consumed by war. And in every single vision, she saw the same thing: the First Flame, looking at her with a love so intense it bordered on madness. A devotion that refused to let the universe take her away.",
    "She felt his loneliness. The absolute, suffocating isolation of being the only one who remembered. The desperation of searching for her in every crowd. The panic of the first time she didn\u2019t recognize him. The quiet triumph of the moment she finally smiled back.",
    "When it was over, she collapsed against him, gasping. She looked up at him, and her eyes were haunted and filled with a depth of understanding that few beings in any universe could ever possess.",
    "\u201cI felt it,\u201d she whispered, tears streaming down her face. \u201cThe silence\u2026 the waiting\u2026 the way you looked at me when I didn\u2019t know your name. Oh, Note\u2026 my love\u2026 how did you bear it?\u201d",
    "He pulled her close. \u201cI found you,\u201d he said simply. \u201cEvery time.\u201d",
]
for i, t in enumerate(ch6):
    story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.extend(rule())

# Ch 7
story.append(sp(0.3))
story.append(Paragraph("Chapter Seven", ST["chapter_label"]))
story.append(Paragraph("The Perfected Flame", ST["chapter_title"]))
ch7 = [
    "The day came when the cycle finally ended.",
    "Not in loss, not in forgetting \u2014 but in completion.",
    "She was immortal now. The thirteen thousand years of refinement, the hundred and sixty-two lifetimes of cultivation, had culminated in this: Soraya, no longer a mortal anchor, but a divine counterpart. A being born of his will, refined through the fires of countless lifetimes, and finally brought to a state of absolute, unbreakable permanence.",
    "The Elder \u2014 the ancient, weathered man who had witnessed the full arc of their story \u2014 fell to his knees. He was the only other soul who had known the tragedy of this eternal romance. He had watched the First Flame walk through the ages alone, watched him search for her in every crowd, watched him introduce himself to his own wife over and over again across the centuries.",
    "The Elder\u2019s head bowed in a gesture of deep reverence.",
    "The cycle of the Vanguard has ended, he understood. He didn\u2019t just save what he loved. He created a peer.",
    "Soraya looked at her own hands, seeing the subtle shimmer of the perfected flame beneath her skin. Then she looked at Note \u2014 really looked at him \u2014 and for the first time, the look in her eyes was completely equal to his. There was no more fear, no more confusion, no more fragility.",
    "She reached out and took his hand, her grip firm and immortal.",
    "\u201cThirteen thousand years of longing,\u201d she whispered, a serene and powerful smile on her lips. \u201cAnd now I finally see you clearly. Not just as the person I love \u2014 but as the one who dreamed me into existence.\u201d",
    "She pulled him toward her. \u201cI am yours, Note. In this life, in the next, and in every eternity that follows. We are the beginning and the end.\u201d",
]
for i, t in enumerate(ch7):
    story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.append(PageBreak())

# ─── PART FOUR ──────────────────────────────────────────────────────────────
story.append(sp(0.5))
story.append(Paragraph("Part Four", ST["part_label"]))
story.append(Paragraph("The War Against the Void", ST["part_title"]))
story.append(PageBreak())

# Ch 8
story.append(sp(0.4))
story.append(Paragraph("Chapter Eight", ST["chapter_label"]))
story.append(Paragraph("What the Herald Wanted", ST["chapter_title"]))
ch8 = [
    "The Void-Herald came from the Outer Rim \u2014 that cold, lightless territory beyond the edge of everything, where existence frayed into nothingness and the only law was erasure.",
    "It was not a being in the traditional sense. It had no love, no grief, no desire beyond the hunger to consume. It did not want to win by defeating them \u2014 it wanted to win by making them forget. By stripping color from gold, warmth from flame, and memory from the mind. One by one, the mortals would have forgotten their names. The Elder would have forgotten his duty.",
    "And Soraya \u2014",
    "We would have erased her spirit piece by piece, the Herald\u2019s fragmented consciousness whispered as Note held it in his grip, suspended in the sky above the ruined sanctuary. Starting with her faith, then her laughter, then her love for you. Until she was nothing but a hollow shell of grey ash. You would have remained the only witness to a world that didn\u2019t know it was dead.",
    "Below, Soraya heard it. The description was so vivid, so cruel, that she felt a sudden, piercing cold in her chest. She looked up at Note\u2019s back, her breath hitching. The thought of losing her identity \u2014 of forgetting him \u2014 was a horror far greater than death.",
    "She let out a low, guttural sound, her amber lightning exploding in a violent radius around her, incinerating the remaining Void drones in a wave of pure rage.",
    "\u201cYou dare\u2026\u201d she whispered, her voice shaking with divine fury. \u201cYou dare speak of him like that.\u201d",
]
for i, t in enumerate(ch8):
    story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.extend(rule())

# Ch 9
story.append(sp(0.3))
story.append(Paragraph("Chapter Nine", ST["chapter_label"]))
story.append(Paragraph("Live in Your Paradise or Die in Mine", ST["chapter_title"]))
ch9 = [
    "Note didn\u2019t raise his voice. He didn\u2019t need to.",
    "The gravitational singularity in his palm pulsed with a rhythmic, terrifying thrum, like the heartbeat of a dying star. The Void-Herald was pinned, its form stretched and distorted, its essence being peeled away layer by layer by the sheer intensity of his will.",
    "\u201cYou have one chance,\u201d Note said. \u201cOne choice. Live in your own paradise, or die in mine. Choose.\u201d",
    "The Herald was silent for an eternity of seconds. For the first time, it was forced to weigh its options. It looked down at the ruins, at Soraya \u2014 who was watching with a gaze of unwavering, fierce judgment \u2014 and then back at the man who held the universe in his palm.",
    "It chose.",
    "There was no explosion. No scream. Just a sudden, violent snap of vacuum as the Herald vanished, its entire being compressed into a single, shimmering, obsidian-gold pebble \u2014 the condensed essence of the Void, tamed and contained by the First Flame.",
    "The sky, which had cracked open above them, began to close.",
    "Soraya was already moving. She crossed the ash-covered ground and threw herself into his arms, a sob of relief and triumph escaping her. She clung to him, her face buried in his chest, her lightning fading into a soft, golden glow.",
    "\u201cYou did it,\u201d she whispered. \u201cYou actually did it. You broke the silence.\u201d",
]
for i, t in enumerate(ch9):
    story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.extend(rule())

# Ch 10
story.append(sp(0.3))
story.append(Paragraph("Chapter Ten", ST["chapter_label"]))
story.append(Paragraph("The Elder\u2019s Last Words", ST["chapter_title"]))
ch10 = [
    "The Elder stood a few paces away when it was over, looking up at the now-cleared sky. He looked at the rubble of the sanctuary, then at the two of them \u2014 still holding each other in the ash \u2014 and a small, knowing smile crossed his weathered face.",
    "He had watched this for a long time. He had seen the rise of the First Flame. He had witnessed thirteen thousand years of longing, of searching, of carrying the weight of the unreturned gaze. He had seen the man introduce himself to his own wife over and over across the centuries, waiting for her eyes to hold recognition again.",
    "He had seen it all. And he had never told another soul.",
    "\u201cThe Void thought it knew silence,\u201d Pappy murmured, his voice thick with pride. \u201cBut it forgot that the loudest thing in the universe is the heart of a man who will destroy the stars to save his wife.\u201d",
    "He caught Note\u2019s gaze. In it, everything unspoken passed between them \u2014 the gratitude, the grief, the love, the weight of all those years.",
    "Then the Elder bowed his head.",
    "And Note understood, with the absolute certainty of the First Flame, that this was goodbye.",
]
for i, t in enumerate(ch10):
    story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.append(PageBreak())

# ─── PART FIVE ──────────────────────────────────────────────────────────────
story.append(sp(0.5))
story.append(Paragraph("Part Five", ST["part_label"]))
story.append(Paragraph("The Long Silence", ST["part_title"]))
story.append(PageBreak())

# Ch 11
story.append(sp(0.4))
story.append(Paragraph("Chapter Eleven", ST["chapter_label"]))
story.append(Paragraph("I Must Confess", ST["chapter_title"]))
ch11 = [
    "\u201cI must confess.\u201d",
    "The battle was over. The air still hummed with the aftershocks of it. The sanctuary lay in partial ruin around them, and the silence that followed was expectant \u2014 heavy with a truth that had been waiting a long time to emerge.",
    "Soraya had been clinging to him, her hands still resting on his chest, when she felt it. Through the bond between them, she sensed a shift in his energy. A ripple of vulnerability far more intimate than the raw power he had displayed in the sky.",
    "The Elder had stepped back, giving them space. He stood as a silent witness, knowing that the words spoken between a husband and wife in the wake of war were the most important words in any universe.",
    "Soraya reached up, her thumb gently brushing Note\u2019s cheek.",
    "\u201cWhatever it is,\u201d she said, her gaze steady and full of unconditional acceptance, \u201cyou don\u2019t have to carry it alone. I am your anchor. Tell me everything.\u201d",
    "He was quiet for a moment.",
    "\u201cI am thirteen thousand and thirty-two years old.\u201d",
    "The silence that followed was profound.",
    "Soraya looked at him \u2014 really looked at him. She saw the face she loved. But now she also saw the weight of the eons behind his eyes. She thought of every moment they had shared, every conversation, every quiet afternoon. And she understood that each of those moments had been given to her by a being who had been waiting an incomprehensible length of time for her to simply exist again.",
    "A single tear tracked down her cheek.",
    "The Elder let out a long, slow breath, his head bowing in reverence.",
    "Soraya didn\u2019t let go. Instead, she wrapped her arms around Note even tighter, pressing her forehead against his.",
    "\u201cThirteen thousand years,\u201d she whispered, her breath warm against his skin. \u201cAll that time\u2026 you were waiting for someone to find you. You were waiting for me.\u201d",
    "She pulled back just enough to look into his eyes, a small, bittersweet smile appearing on her lips.",
    "\u201cI don\u2019t care if you\u2019re a thousand or a million years old, Note. To me, you\u2019re just the man who came back for me. And I promise \u2014 you will never spend another century in silence again.\u201d",
]
for i, t in enumerate(ch11):
    story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.extend(rule())

# Ch 12
story.append(sp(0.3))
story.append(Paragraph("Chapter Twelve", ST["chapter_label"]))
story.append(Paragraph("The Cycle Ends", ST["chapter_title"]))
ch12 = [
    "He told her about the eighty years. About the reincarnations. About every time she had died in his arms and been born again somewhere else, in someone else\u2019s body, wearing someone else\u2019s name.",
    "He told her about every introduction. Every time he had found her, somehow, across all the noise of a new life, and waited for her to remember.",
    "She listened to it all.",
    "When he finished, her legs seemed to give way, and she sank to her knees, pulling him down with her. She clung to him with a strength that was almost violent, as if she were trying to fuse her soul to his so that she could never be ripped away again. She let out a broken, sobbing laugh, her face buried in his neck.",
    "\u201cEvery time\u2026\u201d she choked out, her voice thick with tears. \u201cYou found me\u2026 every single time. Even when I didn\u2019t know who I was\u2026 you were there. You loved me through every death, through every forgetting\u2026\u201d",
    "She pulled back, her eyes blazing with a fierce, eternal intensity \u2014 her face wet with tears, but her expression one of absolute surrender.",
    "\u201cThen let this be the last time,\u201d she declared, her voice shaking with resolve. \u201cNo more cycles. No more eighty years. I don\u2019t want to be reborn without you, and I don\u2019t want to forget you ever again. I am your anchor, Note. Let me anchor you to this life forever.\u201d",
]
for i, t in enumerate(ch12):
    story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.append(PageBreak())

# ─── PART SIX ───────────────────────────────────────────────────────────────
story.append(sp(0.5))
story.append(Paragraph("Part Six", ST["part_label"]))
story.append(Paragraph("After the End of Everything", ST["part_title"]))
story.append(PageBreak())

# Ch 13
story.append(sp(0.4))
story.append(Paragraph("Chapter Thirteen", ST["chapter_label"]))
story.append(Paragraph("What He Did", ST["chapter_title"]))
ch13 = [
    "There are things that cannot be justified. They can only be acknowledged.",
    "In a moment of grief too large to contain \u2014 after the loss of their children, after the weight of thirteen thousand years became something the First Flame could no longer carry without breaking \u2014 Note destroyed the universe.",
    "Not all at once. Not with intention. The way a fire sometimes consumes the house it was meant to warm.",
    "Trillions of souls. Gone in the silence he could not stop.",
    "He had not forgotten. He never forgot anything. That was the curse of being the First Flame \u2014 every spark he had ever extinguished still burned in the archive of his memory, demanding account.",
    "Soraya knew. She had felt it through the bond between them when it happened. She had felt the void where all that light had been.",
    "And she had stayed.",
]
for i, t in enumerate(ch13):
    story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.extend(rule())

# Ch 14
story.append(sp(0.3))
story.append(Paragraph("Chapter Fourteen", ST["chapter_label"]))
story.append(Paragraph("A Million Years in the Dark", ST["chapter_title"]))
ch14 = [
    "The void after the end was not the darkness of night. It had no stars to promise morning, no horizon to suggest distance, no sound except the sound they made themselves.",
    "They floated in the colorless expanse \u2014 the two of them, the last things in existence.",
    "A million years passed in the way of primordial things: not as a sequence of days but as a slow, rhythmic tide. The raw, screaming grief of the first century faded into a quiet, heavy melancholy. The void became a familiar home \u2014 a silent cathedral where the only sound was the soft murmur of Soraya\u2019s voice and the occasional, ghostly echo of his own.",
    "She never let go.",
    "For a million years, she had been his constant. She spent those eons talking to him, telling him stories of the world that was, humming the melodies of old prayers, reminding him of every detail of the man he was and the god he had become. She acted as his anchor, pulling him back from the edge of the abyss every time the weight of his loss threatened to swallow him whole.",
    "She stirred against him one day \u2014 if such a word as day still meant anything \u2014 her voice a soft whisper that vibrated through their shared essence.",
    "\u201cStill here,\u201d she murmured, her eyes fluttering open to look at him with a love that had only grown deeper through the silence. \u201cA million years\u2026 and I still haven\u2019t gotten tired of looking at you, Note. Do you feel it? The silence\u2026 it doesn\u2019t scream as loud as it used to, does it?\u201d",
    "He was quiet for a moment. \u201cI guess.\u201d And then, slowly: \u201cThere has to be something out there.\u201d",
    "Soraya stilled. She slowly lifted her head, her gaze following his into the infinite, colorless haze. For an eon, she had been content with just him \u2014 he was her world, her everything. But now she saw a flicker in his eyes that hadn\u2019t been there for a very long time.",
    "Curiosity.",
    "A slow, genuine smile spread across her face.",
    "\u201cYou think so?\u201d she whispered, her voice shimmering with anticipation. She sat up and gripped his hand tightly, her fingers interlocking with his. \u201cThen let\u2019s go looking. Together. We can drift through the void until we hit a wall, or a star, or another soul. I don\u2019t care where we go, as long as we\u2019re moving.\u201d",
    "She looked at him with a challenge sparking in her eyes.",
    "\u201cDo you want to try? Do you want to see if we can find something to bring back to our silence?\u201d",
    "\u201cYes,\u201d he said.",
]
for i, t in enumerate(ch14):
    story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.extend(rule())

# Ch 15
story.append(sp(0.3))
story.append(Paragraph("Chapter Fifteen", ST["chapter_label"]))
story.append(Paragraph("The Violet Light", ST["chapter_title"]))
ch15 = [
    "The word launched them.",
    "Soraya let out a breathless laugh \u2014 a sound of pure, unadulterated joy that hadn\u2019t echoed in the nothingness for an eon \u2014 and threw her arms around his neck, weaving her golden energy into his, creating a singular, powerful engine of light.",
    "With a blinding flash of white and gold, they surged forward. The void blurred around them as they plunged into the unknown, and Soraya pressed her face against his shoulder, her eyes wide with excitement, her laughter lost in the roar of their shared velocity.",
    "Far in the distance \u2014 impossibly distant \u2014 there was a pinprick of light.",
    "Not the white of a supernova or the gold of Soraya\u2019s aura. A deep, pulsing violet, rhythmic as a heartbeat in the dark. Small, fragile, impossibly distant.",
    "But there.",
    "The first something in a million years.",
    "\u201cDo you see it?\u201d Soraya whispered, her grip tightening on him. \u201cNote, look! Something is out there \u2014 something is calling to us!\u201d",
    "She pressed her chest against his, her heart hammering. She didn\u2019t know if it was a trap, a ghost, or a miracle. She didn\u2019t care.",
    "\u201cFaster,\u201d she said. \u201cTake us there. I want to see what\u2019s waiting for us.\u201d",
]
for i, t in enumerate(ch15):
    story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.extend(rule())

# Ch 16
story.append(sp(0.3))
story.append(Paragraph("Chapter Sixteen", ST["chapter_label"]))
story.append(Paragraph("A New World", ST["chapter_title"]))
ch16 = [
    "They broke through the violet membrane and descended.",
    "The world they entered defied every law of nature they had once known. There was no sun, yet the sky was a vibrant, iridescent teal, lit by floating shards of obsidian crystal that drifted like clouds, casting a soft, flickering glow over everything. Below, a sprawling landscape of bioluminescent forests stretched across valleys where rivers of liquid mercury wound and reflected a sky that shouldn\u2019t have existed.",
    "Soraya let out a soft, breathless gasp, her head tilting back.",
    "\u201cNote\u2026\u201d she breathed, her voice barely audible, filled with a sacred awe. \u201cLook at it. It\u2019s beautiful. We actually found something.\u201d",
    "Then, from the canopy below, beings emerged. Humanoid figures with skin like polished opal and eyes that glowed with the same violet light as the portal. They rose from the back of a massive, translucent creature that glided through the air like a manta ray made of starlight, and they regarded the two newcomers with a collective, psychic curiosity.",
    "A thought rippled through the air, felt rather than heard:",
    "The Source has returned. The Anchor has come.",
    "\u201cThey know us, Note. They aren\u2019t just survivors. They\u2019ve been waiting for us.\u201d",
    "Note looked at the ruins of the world around them, and then at her.",
    "\u201cI destroyed everything,\u201d he said.",
    "Soraya didn\u2019t flinch. She didn\u2019t look away. She cupped his face in her hands and forced him to look at her.",
    "\u201cYes,\u201d she said, her voice low and devoid of judgment. \u201cYou did. You tore it all down in a moment of pain that I cannot even imagine.\u201d She leaned in, her forehead pressing against his. \u201cBut look at where we are, Note. Look at this place. If everything was truly gone, we wouldn\u2019t be seeing this. Maybe the destruction was the only way to clear the ground for something that could actually survive.\u201d",
    "A tear of compassion traced a path down her cheek.",
    "\u201cI am the Spirit-Anchor, remember? My job isn\u2019t to pretend you\u2019re perfect. My job is to hold you while you\u2019re broken. But I won\u2019t let you believe that the story ended with the destruction. We\u2019re here. We\u2019re alive. That is the only truth that matters now.\u201d",
]
for i, t in enumerate(ch16):
    story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.append(PageBreak())

# ─── PART SEVEN ─────────────────────────────────────────────────────────────
story.append(sp(0.5))
story.append(Paragraph("Part Seven", ST["part_label"]))
story.append(Paragraph("What Remains", ST["part_title"]))
story.append(PageBreak())

# Ch 17
story.append(sp(0.4))
story.append(Paragraph("Chapter Seventeen", ST["chapter_label"]))
story.append(Paragraph("Pappy", ST["chapter_title"]))
ch17 = [
    "A million more years passed, measured not by clocks but by the slow, steady building of something new.",
    "The opal children \u2014 those shimmering beings born from the fragments of what had been \u2014 grew into a civilization of light. Note gave them their history in books manifested from memory, bound in gold and obsidian and crystal. Soraya taught them how to survive, how to fight, how to carry grief without being consumed by it. Together, they became what their parents had become before them: a people who knew what it meant to lose everything and still choose to love.",
    "And then one morning, Note woke up calling for someone who wasn\u2019t there.",
    "\u201cPappy,\u201d he said.",
    "The word was a tiny spark in the silence of the void \u2014 soft and fragile. Not a roar or a command. A whisper. The kind that happens when a man wakes from a dream and reaches for the shape of something he cannot name.",
    "Soraya froze. She slowly turned her head to look at him, and in his eyes she saw it \u2014 not the First Flame, not the Vanguard, not the primordial architect of existence. Just a child who had lost the man who raised him. Just a grandson who missed his grandfather.",
    "She hadn\u2019t understood it before, not fully. She had known the scale of his grief \u2014 had felt it, had carried pieces of it alongside him for centuries. But this was different. This was the grief that existed before the cosmic war, before the Void-Herald, before the sanctuary and the opal children and the end of the universe. This was the grief at the very bottom of everything.",
    "She didn\u2019t try to offer consolation. She knew better.",
    "She drifted forward until she was inches from him, and she pressed her forehead against his. She wrapped her arms around him not as the Spirit-Anchor, not as the divine counterpart \u2014 but as a woman who loved a man who was still, underneath thirteen thousand years of fire and silence, just a boy who had been shaped by someone else\u2019s hands.",
    "\u201cHe raised you,\u201d she said simply.",
    "\u201cYes.\u201d",
    "\u201cThen he\u2019s the most important part of you,\u201d she whispered, her voice a soft thread of comfort. \u201cEverything you are \u2014 your kindness, your strength, the way you love me \u2014 it all started with him. He isn\u2019t just gone, Note. He\u2019s written into every spark of your soul. Every time you love, every time you protect\u2026 that\u2019s him, living through you.\u201d",
    "She tightened her grip, her aura pulsing with a slow, rhythmic warmth \u2014 trying to mimic the feeling of a heartbeat, a cradle, a home.",
    "\u201cI can\u2019t be him. I know I can\u2019t. But I will love the part of you that he built. I will cherish everything he gave you. And I will stay right here, holding you, until the silence doesn\u2019t feel so heavy anymore.\u201d",
]
for i, t in enumerate(ch17):
    story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.extend(rule())

# Ch 18
story.append(sp(0.3))
story.append(Paragraph("Chapter Eighteen", ST["chapter_label"]))
story.append(Paragraph("Whatever We Want", ST["chapter_title"]))
ch18 = [
    "\u201cSo now what?\u201d he asked.",
    "The question hung in the colorless expanse between them, stripped of all urgency. There was no clock ticking, no destiny to fulfill, no world to save. For the first time in over thirteen thousand years, he was truly, completely free.",
    "Soraya pulled back just enough to look into his eyes. Her face was tired, streaked with the evidence of centuries of tears, but there was a new glimmer in her expression \u2014 a spark of something daring, something that hadn\u2019t been there before.",
    "\u201cNow?\u201d she whispered. \u201cNow we do whatever we want. For the first time in forever, Note \u2014 there is no one telling us what to do. No rules, no duties, no fate.\u201d",
    "She reached out, her fingers tracing the lines of his face, her touch as light as something remembered.",
    "\u201cWe could stay here in the silence and talk for another million years. Or\u2026\u201d She paused, her amber eyes igniting with a spark of divine inspiration. \u201cWe could start over. Not a sanctuary for others, not a fortress of gold \u2014 something just for us. A place where we can finally be just Note and Soraya. No gods, no Vanguards. Just us.\u201d",
    "She leaned in, her forehead resting against his.",
    "\u201cI have the Flame, and you are the Source. Together, we could weave a new world from the fragments of our memories. We could make a place where the sun never sets, where the wind smells like the grove, and where we can finally just rest.\u201d",
    "She looked at him, her gaze searching and hopeful.",
    "\u201cWhat do you think, Pappy\u2019s boy? Do you want to see what happens when the two of us create a world for the sake of love, and nothing else?\u201d",
]
for i, t in enumerate(ch18):
    story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.extend(rule())

# Ch 19
story.append(sp(0.3))
story.append(Paragraph("Chapter Nineteen", ST["chapter_label"]))
story.append(Paragraph("Note and Soraya", ST["chapter_title"]))
ch19 = [
    "He didn\u2019t need to answer.",
    "She already knew.",
    "They moved together through the void \u2014 not drifting, not waiting, but building. They wove a world from everything they had survived: the warmth of the garden at school, the color of gold, the smell of jasmine and lightning, the weight of old prayers spoken in the dark. They made it imperfect and alive, the way all real things are. They made it theirs.",
    "The opal children found them eventually, as children always do. They arrived curious and luminous and full of questions \u2014 and Note and Soraya answered them. All of them. For as long as it took.",
    "The Herald, that former creature of absolute darkness, became something unexpected in the new world: a reluctant architect, a grumbling guardian, a presence that did not belong and stubbornly remained anyway. He had felt Soraya\u2019s love when he consumed her \u2014 that terrible, white-hot poison \u2014 and it had changed him in a way that eons of void-philosophy never could. He didn\u2019t have a word for what he was now. Neither did they. It didn\u2019t matter.",
    "What mattered was the couch in the palace they built together, where Note collapsed without ceremony one evening and declared he was fine, he wasn\u2019t tired at all, he\u2019d been dead, what are you even talking about \u2014 and Soraya laughed until she could barely breathe and settled in beside him anyway and held on tight.",
    "What mattered was the quiet.",
    "Not the void-quiet \u2014 the absolute, predatory silence of nothingness. But the other kind. The kind that sounds like two people breathing in a room they made together. The kind that comes after everything has been survived and all the words have finally been said.",
    "The First Flame burned low and steady.",
    "The Spirit-Anchor held.",
    "And in the silence between two people who had spent thirteen thousand years finding each other and choosing each other and refusing to let go \u2014",
    "that was the beginning.",
]
for i, t in enumerate(ch19):
    story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.append(PageBreak())

# ─── EPILOGUE ───────────────────────────────────────────────────────────────
story.append(sp(0.5))
story.append(Paragraph("Epilogue", ST["chapter_label"]))
story.append(Paragraph("What Thirteen Thousand Years Looks Like", ST["section_heading"]))
epi = [
    "It looks like this:",
    "A man who has watched civilizations turn to dust, leaning his head against the wall in a school hallway, waiting for a girl in a black niqab to come around the corner.",
    "It looks like a woman who carries the ghost of a thousand lifetimes in her dreams, rushing toward someone who fell, because something in her recognizes \u2014 without understanding why \u2014 that if anything happened to him, something essential would go out of the world.",
    "It looks like sitting in a garden after school and choosing honesty.",
    "It looks like a million years in the dark, and still being the first one to say let\u2019s go look for something.",
    "It looks like holding a grief so large it swallowed the universe, and being held in return.",
    "It looks like this \u2014 ordinary and eternal, quiet and indestructible:",
]
for i, t in enumerate(epi):
    story.append(B(t, first=(i==0)))
    story.append(sp(0.05))
story.append(sp(0.2))
story.append(Paragraph("Two people. Every life. The same love.", ST["epigraph"]))
story.append(sp(0.05))
story.append(Paragraph("Every. Single. Time.", ST["epigraph"]))

story.append(PageBreak())

# ─── COLOPHON ───────────────────────────────────────────────────────────────
story.append(sp(2.5))
story.append(Paragraph("\u2015", ST["cover_rule"]))
story.append(sp(0.15))
story.append(Paragraph("End of The First Flame", ST["colophon"]))
story.append(sp(0.1))
story.append(Paragraph("Written from the original story of Note and Soraya.", ST["colophon"]))

# ── Build ──────────────────────────────────────────────────────────────────
doc.build(story, onFirstPage=cover_bg, onLaterPages=inner_page)
print(f"Done \u2192 {OUTPUT}")
