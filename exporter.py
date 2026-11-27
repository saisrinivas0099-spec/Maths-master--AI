from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, 
    PageBreak, KeepTogether, ListFlowable, ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from io import BytesIO
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import mathtext
from matplotlib.font_manager import FontProperties

# ---------------- Math Rendering Helper ----------------

def latex_to_image(latex_str: str, fontsize: int = 14, dpi: int = 200) -> BytesIO:
    """
    Convert a LaTeX string to a PNG image (BytesIO)
    """
    # Clean the latex
    latex_str = latex_str.strip()
    if latex_str.startswith("$") and latex_str.endswith("$"):
        latex_str = latex_str[1:-1]
    if latex_str.startswith("\\(") and latex_str.endswith("\\)"):
        latex_str = latex_str[2:-2]

    fig = plt.figure(figsize=(0.01, 0.01))
    fig.patch.set_alpha(0)

    try:
        # Use mathtext (built into matplotlib) - no full LaTeX needed
        text = fig.text(0, 0, f"${latex_str}$", fontsize=fontsize, 
                       color="black", ha="left", va="bottom")
        
        # Get the bounding box
        fig.canvas.draw()
        bbox = text.get_window_extent(renderer=fig.canvas.get_renderer())
        
        # Adjust figure size
        width = bbox.width / dpi + 0.1
        height = bbox.height / dpi + 0.05
        fig.set_size_inches(width, height)
        
        text.set_position((0.01, 0.01))
        
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight", 
                    pad_inches=0.05, transparent=True, facecolor="white")
        buf.seek(0)
        plt.close(fig)
        return buf
    except Exception as e:
        plt.close(fig)
        # Fallback: return text as image
        fig, ax = plt.subplots(figsize=(6, 0.4))
        ax.axis("off")
        ax.text(0.01, 0.5, latex_str, fontsize=12, va="center", ha="left", 
                family="monospace")
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight", 
                    transparent=True)
        buf.seek(0)
        plt.close(fig)
        return buf


def process_text_with_math(text: str, styles):
    """
    Split text into normal paragraphs and math images
    Returns list of flowables
    """
    if not text:
        return []

    # Find all $...$ or $$...$$ expressions
    pattern = r'(\$\$.*?\$\$|\$.*?\$)'
    parts = re.split(pattern, text, flags=re.DOTALL)

    flowables = []
    for part in parts:
        part = part.strip()
        if not part:
            continue

        if (part.startswith("$") and part.endswith("$")) or \
           (part.startswith("$$") and part.endswith("$$")):
            # This is math
            try:
                img_buf = latex_to_image(part)
                img = Image(img_buf)
                # Scale the image reasonably
                img._restrictSize(160*mm, 40*mm)
                flowables.append(img)
                flowables.append(Spacer(1, 3*mm))
            except Exception:
                # If math fails, just show as text
                flowables.append(Paragraph(part.replace("$", ""), styles["Normal"]))
        else:
            # Normal text
            # Escape special characters for reportlab
            safe_text = part.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            flowables.append(Paragraph(safe_text, styles["Normal"]))
            flowables.append(Spacer(1, 2*mm))

    return flowables


# ---------------- Main PDF Generator ----------------

def generate_pdf(questions: list, title: str = "Maths Master AI - Question Paper") -> BytesIO:
    """
    questions: list of dicts
    Example:
    [
        {
            "qno": 1,
            "question": "The domain of ... $f(x) = \\sqrt{x^2-9}$ is",
            "options": ["(-3,3)", "[-3,3]", ...],
            "answer": "C",
            "solution": "For $f(x)=\\sqrt{x^2-9}$ ..."
        },
        ...
    ]
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18*mm,
        leftMargin=18*mm,
        topMargin=15*mm,
        bottomMargin=15*mm
    )

    styles = getSampleStyleSheet()

    # Custom styles
    styles.add(ParagraphStyle(
        name="MainTitle",
        parent=styles["Heading1"],
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=8*mm,
        textColor=colors.HexColor("#1a365d")
    ))
    styles.add(ParagraphStyle(
        name="QNo",
        parent=styles["Normal"],
        fontSize=11,
        fontName="Helvetica-Bold",
        spaceBefore=6*mm,
        spaceAfter=2*mm,
        textColor=colors.HexColor("#2c5282")
    ))
    styles.add(ParagraphStyle(
        name="Option",
        parent=styles["Normal"],
        fontSize=10,
        leftIndent=8*mm,
        spaceAfter=1*mm
    ))
    styles.add(ParagraphStyle(
        name="Answer",
        parent=styles["Normal"],
        fontSize=10,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#276749"),
        spaceBefore=2*mm
    ))
    styles.add(ParagraphStyle(
        name="SolutionHeader",
        parent=styles["Normal"],
        fontSize=10,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#744210"),
        spaceBefore=3*mm
    ))

    story = []

    # Title
    story.append(Paragraph(title, styles["MainTitle"]))
    story.append(Spacer(1, 4*mm))

    for q in questions:
        qno = q.get("qno", "")
        question = q.get("question", "")
        options = q.get("options", [])
        answer = q.get("answer", "")
        solution = q.get("solution", "")

        # Question number + question text
        elements = []
        elements.append(Paragraph(f"<b>Q{qno}.</b>", styles["QNo"]))

        # Process question text (may contain math)
        elements.extend(process_text_with_math(question, styles))

        # Options
        if options:
            for idx, opt in enumerate(options):
                label = chr(65 + idx)  # A, B, C, D
                opt_text = f"<b>({label})</b>  {opt}"
                elements.extend(process_text_with_math(opt_text, styles))

        # Answer
        if answer:
            elements.append(Paragraph(f"<b>Answer:</b> ({answer})", styles["Answer"]))

        # Solution
        if solution:
            elements.append(Paragraph("<b>Solution:</b>", styles["SolutionHeader"]))
            elements.extend(process_text_with_math(solution, styles))

        elements.append(Spacer(1, 4*mm))
        story.append(KeepTogether(elements))

    doc.build(story)
    buffer.seek(0)
    return buffer


# ---------------- Example usage (for testing) ----------------
if __name__ == "__main__":
    sample = [
        {
            "qno": 1,
            "question": r"The domain of the real-valued function $f(x) = \sqrt{x^2 - 9}$ is",
            "options": [
                r"$(-3, 3)$",
                r"$[-3, 3]$",
                r"$(-\infty, -3] \cup [3, \infty)$",
                r"$(-\infty, -3) \cup (3, \infty)$"
            ],
            "answer": "C",
            "solution": r"For $f(x) = \sqrt{x^2 - 9}$ to be defined, $x^2 - 9 \ge 0 \implies (x-3)(x+3) \ge 0$. Hence domain is $(-\infty, -3] \cup [3, \infty)$."
        }
    ]

    pdf_bytes = generate_pdf(sample, "Intermediate 1st Year - Mathematics IA - Functions")
    with open("test_output.pdf", "wb") as f:
        f.write(pdf_bytes.getvalue())
    print("PDF generated successfully → test_output.pdf")
