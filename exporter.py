from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from io import BytesIO
from xml.sax.saxutils import escape
import re
from io import BytesIO

import matplotlib
matplotlib.use("Agg")

from matplotlib import mathtext
from matplotlib.font_manager import FontProperties

from reportlab.platypus import Image

def make_pdf(title, questions):
    buf=BytesIO()
    doc=SimpleDocTemplate(buf,pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=16*mm,bottomMargin=16*mm)
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Q",parent=styles["Heading3"],textColor=colors.HexColor("#123c69"),spaceBefore=10))
    story=[Paragraph(escape(title),styles["Title"]),Spacer(1,8)]
    for i,q in enumerate(questions,1):
        story.append(Paragraph(f"Q{i}. {escape(q['question'])}",styles["Q"]))
        for opt in q.get("options",[]): story.append(Paragraph(escape(opt),styles["BodyText"]))
        story.append(Paragraph(f"<b>Answer:</b> {escape(q['answer'])}",styles["BodyText"]))
        story.append(Paragraph(f"<b>Solution:</b> {escape(q['solution'])}",styles["BodyText"]))
        story.append(Spacer(1,6))
    doc.build(story)
    def latex_to_pdf_image(latex, max_width=450):
    # Remove LaTeX delimiters
    latex = latex.strip()
    latex = latex.replace("$$", "")
    latex = latex.replace("$", "")
    latex = latex.replace(r"\(", "")
    latex = latex.replace(r"\)", "")
    latex = latex.replace(r"\[", "")
    latex = latex.replace(r"\]", "")

    buffer = BytesIO()

    width, height = mathtext.math_to_image(
        latex,
        buffer,
        dpi=200,
        format="png",
        prop=FontProperties(size=14)
    )

    buffer.seek(0)

    scale = min(max_width / width, 1)
    return Image(
        buffer,
        width=width * scale,
        height=height * scale
    )
    return buf.getvalue()
