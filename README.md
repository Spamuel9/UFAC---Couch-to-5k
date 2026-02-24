# Custom Couch to 5K PT Plan (Printable PDF)

This repository generates a clean, printable **6-month (24-week)** Couch to 5K plan that:
- uses **4 required workout days/week**,
- includes **3 optional rest days**,
- captures an individual's **age** and **last cumulative PT score**,
- is **week-based only** (no fixed calendar day/date assignments),
- places the **24-week schedule at the top**,
- then includes **consecutive walkthrough pages** with multiple workout examples and form visuals,
- and appends the uploaded PT chart PDF for reference.

## Why the plan PDF is not committed
`Custom_Couch_to_5K_PT_Plan.pdf` is a generated binary artifact. Some environments block or limit binary file downloads from commits, so this repo keeps source files and generates the PDF locally.

## Generate the PDF

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Run the generator:

```bash
python generate_custom_c25k_pdf.py
```

3. Output:
- `Custom_Couch_to_5K_PT_Plan.pdf` (generated in repo root)

## Inputs
- `PT Charts New - 50-20-15-15_with 2Mile_FINAL_23 Sep 25.pdf` (already in repository)
