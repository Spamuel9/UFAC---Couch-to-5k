from datetime import date, timedelta
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

BASE_DIR = Path(__file__).resolve().parent
PLAN_PDF = BASE_DIR / "Custom_Couch_to_5K_PT_Plan.base.pdf"
FINAL_PDF = BASE_DIR / "Custom_Couch_to_5K_PT_Plan.pdf"
PT_CHART_PDF = BASE_DIR / "PT Charts New - 50-20-15-15_with 2Mile_FINAL_23 Sep 25.pdf"


def build_plan_pdf(output_path: Path) -> None:
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0B1F3A"),
        alignment=1,
    )
    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=colors.HexColor("#0B1F3A"),
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.3,
        leading=12,
    )

    flow = []
    flow.append(Paragraph("Custom 6-Month Couch to 5K PT Plan", title_style))
    flow.append(Spacer(1, 0.12 * inch))
    flow.append(
        Paragraph(
            "Printable worksheet based on your age and last cumulative PT score. "
            "This plan runs 24 weeks (about 6 months) until your next PT test.",
            body_style,
        )
    )
    flow.append(Spacer(1, 0.2 * inch))

    info_data = [
        ["Name", "", "Unit", ""],
        ["Age", "", "Date Started", ""],
        ["Last Cumulative PT Score", "", "Goal Cumulative PT Score", ""],
        ["Target PT Test Date", "", "Projected 5K Goal Time", ""],
    ]
    info_table = Table(info_data, colWidths=[1.8 * inch, 1.5 * inch, 2.0 * inch, 1.6 * inch])
    info_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.8, colors.HexColor("#9FB2C7")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#F6F9FC")]),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    flow.append(info_table)
    flow.append(Spacer(1, 0.16 * inch))

    flow.append(Paragraph("How to Personalize This Plan", heading_style))
    flow.append(
        Paragraph(
            "1) Use the attached PT chart pages to find your age-based point standards. "
            "2) Circle your starting tier from your last cumulative score. "
            "3) Follow 4 required workout days each week + 3 optional rest days spread as needed. "
            "4) Re-test at Weeks 8, 16, and 24.",
            body_style,
        )
    )
    flow.append(Spacer(1, 0.1 * inch))

    tier_data = [
        ["Starting Tier", "Last Cumulative PT Score", "Starting Pace Guidance"],
        ["Tier 1 (Foundation)", "< 75", "Walk/jog intervals; conversational effort"],
        ["Tier 2 (Build)", "75-84", "Steady easy runs + short intervals"],
        ["Tier 3 (Advance)", "85+", "Longer run segments + controlled speed work"],
    ]
    tier_table = Table(tier_data, colWidths=[1.75 * inch, 1.6 * inch, 3.0 * inch])
    tier_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B1F3A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.8),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#EEF4FA"), colors.white]),
                ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#8FA5BD")),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    flow.append(tier_table)
    flow.append(Spacer(1, 0.16 * inch))

    flow.append(Paragraph("24-Week Training Layout (4 Training Days + 3 Optional Rest Days)", heading_style))

    def week_block(start_week: int, end_week: int, description: str):
        return f"Weeks {start_week}-{end_week}: {description}"

    phases = [
        week_block(1, 4, "Ease in. Run/Walk progression. Focus on consistency and form."),
        week_block(5, 8, "Build aerobic base. Increase total running time each week."),
        week_block(9, 12, "Strength + speed introduction. Add controlled intervals."),
        week_block(13, 16, "Sustain pace. Longer steady efforts and re-test at Week 16."),
        week_block(17, 20, "Performance phase. Tempo + threshold work scaled by tier."),
        week_block(21, 24, "Peak and taper. Keep quality, reduce volume, PT re-test Week 24."),
    ]

    for phase in phases:
        flow.append(Paragraph(phase, body_style))

    flow.append(Spacer(1, 0.1 * inch))

    weeks = []
    start_date = date.today()
    for week_num in range(1, 25):
        wk_start = start_date + timedelta(days=(week_num - 1) * 7)
        wk_end = wk_start + timedelta(days=6)
        if week_num <= 4:
            workout = "2 run/walk days + 1 easy run + 1 cross-train"
        elif week_num <= 8:
            workout = "2 easy runs + 1 interval day + 1 cross-train"
        elif week_num <= 16:
            workout = "1 long easy run + 1 tempo + 1 intervals + 1 strength/cardio"
        elif week_num <= 20:
            workout = "1 long run + 1 threshold + 1 speed + 1 mobility/strength"
        else:
            workout = "1 long run + 1 race-pace + 1 short speed + 1 easy recovery"
        weeks.append([f"{week_num}", f"{wk_start:%b %d} - {wk_end:%b %d}", workout, "Notes: ____________________"])

    schedule_data = [["Week", "Date Range", "Required 4 Workouts", "Coach / Athlete Notes"]] + weeks
    schedule_table = Table(schedule_data, colWidths=[0.45 * inch, 1.25 * inch, 3.45 * inch, 1.85 * inch])
    schedule_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B1F3A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 7.4),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFD")]),
                ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#B8C7D8")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 2.8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.8),
            ]
        )
    )
    flow.append(schedule_table)

    flow.append(Spacer(1, 0.08 * inch))
    flow.append(
        Paragraph(
            "Recovery guidance: Use your 3 optional rest days any way you need to keep quality high. "
            "If soreness accumulates, reduce interval volume first, then running duration.",
            body_style,
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
