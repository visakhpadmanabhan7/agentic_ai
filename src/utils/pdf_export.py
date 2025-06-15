from fpdf import FPDF
import unicodedata

def clean_text(text: str) -> str:
    # Normalize and remove non-latin1 characters
    return unicodedata.normalize("NFKD", text).encode("latin-1", "ignore").decode("latin-1")

def save_plan_as_pdf(output: str, filename: str):
    if not output.strip():
        raise ValueError("Empty content, cannot generate PDF.")

    sanitized_output = clean_text(output)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in sanitized_output.split("\n"):
        pdf.multi_cell(0, 10, line)

    pdf.output(filename)