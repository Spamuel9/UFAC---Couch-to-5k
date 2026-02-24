from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.graphics.shapes import Circle, Drawing, Line, Rect, String
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

BASE_DIR = Path(__file__).resolve().parent
PLAN_PDF = BASE_DIR / "Custom_Couch_to_5K_PT_Plan.base.pdf"
FINAL_PDF = BASE_DIR / "Custom_Couch_to_5K_PT_Plan.pdf"
PT_CHART_PDF = BASE_DIR / "PT Charts New - 50-20-15-15_with 2Mile_FINAL_23 Sep 25.pdf"


def make_form_illustration(title: str, cue_a: str, cue_b: str) -> Drawing:
    d = Drawing(230, 130)
    d.add(Rect(0, 0, 230, 130, strokeColor=colors.HexColor("#9FB2C7"), fillColor=colors.HexColor("#F7FAFD")))
    d.add(String(8, 114, title, fontName="Helvetica-Bold", fontSize=9, fillColor=colors.HexColor("#0B1F3A")))

    # Simple athlete figure
    d.add(Circle(45, 80, 11, strokeColor=colors.black, fillColor=None))
    d.add(Line(45, 69, 45, 42, strokeColor=colors.black, strokeWidth=2))
    d.add(Line(45, 62, 26, 52, strokeColor=colors.black, strokeWidth=2))
    d.add(Line(45, 62, 66, 54, strokeColor=colors.black, strokeWidth=2))
    d.add(Line(45, 42, 30, 18, strokeColor=colors.black, strokeWidth=2))
    d.add(Line(45, 42, 62, 20, strokeColor=colors.black, strokeWidth=2))

    # Ground reference and cue text
    d.add(Line(12, 16, 90, 16, strokeColor=colors.HexColor("#667"), strokeWidth=1))
    d.add(String(104, 66, f"• {cue_a}", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor("#10253F")))
    d.add(String(104, 49, f"• {cue_b}", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor("#10253F")))
    d.add(String(104, 32, "• Keep breathing steady", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor("#10253F")))

    return d


def build_plan_pdf(output_path: Path) -> None:
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=19,
        leading=23,
        textColor=colors.HexColor("#0B1F3A"),
        alignment=1,
    )
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12, textColor=colors.HexColor("#0B1F3A"))
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontSize=9.2, leading=12)

    flow = [
        Paragraph("Custom 6-Month Couch to 5K PT Plan", title_style),
        Spacer(1, 0.08 * inch),
        Paragraph(
            "Week-based format only (no fixed calendar dates). Complete 4 required workout days per week and place 3 optional rest days wherever needed.",
            body,
        ),
        Spacer(1, 0.12 * inch),
    ]

    info_data = [
        ["Name", "", "Unit", ""],
        ["Age", "", "Last Cumulative PT Score", ""],
        ["Goal Cumulative PT Score", "", "Target PT Test Window", "6 months"],
    ]
    info = Table(info_data, colWidths=[1.5 * inch, 1.55 * inch, 2.1 * inch, 1.8 * inch])
    info.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.7, colors.HexColor("#9FB2C7")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#F6F9FC")]),
            ]
        )
    )
    flow += [info, Spacer(1, 0.13 * inch), Paragraph("24-Week Schedule (at the top)", h2)]

    schedule_rows = [["Week Block", "Required 4 Workouts", "Optional Rest Days", "Checkpoint"]]
    blocks = [
        ("Weeks 1-4", "2 Run/Walk + 1 Easy Run + 1 Mobility/Cross-Train", "3 rest days", "Build consistency"),
        ("Weeks 5-8", "2 Easy Runs + 1 Intervals + 1 Strength/Cardio", "3 rest days", "PT check at week 8"),
        ("Weeks 9-12", "1 Long Easy + 1 Tempo + 1 Intervals + 1 Strength", "3 rest days", "Pace control"),
        ("Weeks 13-16", "1 Long + 1 Tempo + 1 Hills/Speed + 1 Recovery", "3 rest days", "PT check at week 16"),
        ("Weeks 17-20", "1 Long + 1 Threshold + 1 Speed + 1 Mobility", "3 rest days", "Performance build"),
        ("Weeks 21-24", "1 Long + 1 Race-Pace + 1 Short Speed + 1 Easy", "3 rest days", "PT check at week 24"),
    ]
    schedule_rows.extend(blocks)
    schedule = Table(schedule_rows, colWidths=[1.15 * inch, 3.6 * inch, 1.1 * inch, 1.15 * inch])
    schedule.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B1F3A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.7),
                ("GRID", (0, 0), (-1, -1), 0.55, colors.HexColor("#AAB9C9")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F8FBFE"), colors.white]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    flow += [schedule, Spacer(1, 0.1 * inch)]
    flow.append(Paragraph("Detailed Workout Walkthroughs (consecutive pages)", h2))
    flow.append(
        Paragraph(
            "The next pages include multiple workout examples and visual form walkthroughs for each workout type.",
            body,
        )
    )

    workout_pages = [
        {
            "title": "Workout Type: Run/Walk Intervals",
            "examples": [
                "Example A: 6 rounds of 2:00 jog + 1:00 walk.",
                "Example B: 5 rounds of 3:00 jog + 1:30 walk.",
                "Example C: 4 rounds of 4:00 jog + 2:00 walk.",
            ],
            "cues": [("Tall running posture", "Land under hips", "Relax shoulders"), ("Walk recovery form", "Swing arms naturally", "Reset breathing")],
        },
        {
            "title": "Workout Type: Easy Run + Long Easy Run",
            "examples": [
                "Example A: Easy run 20-30 minutes at conversational pace.",
                "Example B: Long easy run 35-50 minutes steady.",
                "Example C: Easy progression run: 10 easy + 10 moderate + 5 easy.",
            ],
            "cues": [("Midfoot strike", "Short quick cadence", "Eyes forward"), ("Distance form", "Keep effort easy", "No sprint finish")],
        },
        {
            "title": "Workout Type: Tempo / Threshold",
            "examples": [
                "Example A: 10 min easy + 12 min tempo + 8 min easy.",
                "Example B: 2 x 8 min threshold with 3 min easy jog.",
                "Example C: 3 x 6 min tempo with 2 min easy jog.",
            ],
            "cues": [("Tempo posture", "Ribs stacked over hips", "Smooth arm swing"), ("Breathing control", "In through nose/mouth", "Out rhythmically")],
        },
        {
            "title": "Workout Type: Speed / Intervals / Hills",
            "examples": [
                "Example A: 8 x 200m fast with 200m walk/jog recovery.",
                "Example B: 6 x 1:00 uphill effort, walk down recovery.",
                "Example C: 10 x 30 sec fast / 60 sec easy.",
            ],
            "cues": [("Speed mechanics", "Drive knees forward", "Push ground away"), ("Hill form", "Slight forward lean", "Keep strides short")],
        },
        {
            "title": "Workout Type: Strength + Mobility",
            "examples": [
                "Example A: 3 rounds — bodyweight squat, lunge, plank, glute bridge.",
                "Example B: Core circuit — dead bug, side plank, bird dog.",
                "Example C: Mobility flow — hips, calves, hamstrings, thoracic rotation.",
            ],
            "cues": [("Squat form", "Knees track over toes", "Chest stays up"), ("Plank form", "Neutral spine", "Brace core")],
        },
    ]

    for idx, wp in enumerate(workout_pages):
        flow.append(PageBreak())
        flow.append(Paragraph(wp["title"], title_style))
        flow.append(Spacer(1, 0.08 * inch))
        flow.append(Paragraph("Workout examples:", h2))
        for item in wp["examples"]:
            flow.append(Paragraph(f"• {item}", body))

        flow.append(Spacer(1, 0.1 * inch))
        flow.append(Paragraph("Form walkthrough visuals:", h2))

        cue_a = wp["cues"][0]
        cue_b = wp["cues"][1]
        visuals = Table(
            [[make_form_illustration(cue_a[0], cue_a[1], cue_a[2]), make_form_illustration(cue_b[0], cue_b[1], cue_b[2])]],
            colWidths=[3.3 * inch, 3.3 * inch],
        )
        visuals.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
        flow.append(visuals)

        flow.append(Spacer(1, 0.08 * inch))
        flow.append(
            Paragraph(
                "Coaching note: Keep effort appropriate for your tier and use any 3 days as optional rest/recovery to stay consistent across the full 24-week block.",
                body,
            )
        )

    doc.build(flow)


def merge_with_pt_chart(plan_pdf: Path, chart_pdf: Path, final_pdf: Path) -> None:
    writer = PdfWriter()
    for page in PdfReader(str(plan_pdf)).pages:
        writer.add_page(page)
    for page in PdfReader(str(chart_pdf)).pages:
        writer.add_page(page)
    with final_pdf.open("wb") as fh:
        writer.write(fh)


if __name__ == "__main__":
    build_plan_pdf(PLAN_PDF)
    merge_with_pt_chart(PLAN_PDF, PT_CHART_PDF, FINAL_PDF)
    print(f"Created {FINAL_PDF.name}")
