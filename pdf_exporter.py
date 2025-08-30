from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def export_to_pdf(results: list[str], filename: str = "results.pdf") -> str:
    """Export a list of search results to a PDF file."""
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    flowables = [Paragraph("Search Results", styles["Heading1"]), Spacer(1, 12)]

    for r in results:
        flowables.append(Paragraph(r, styles["Normal"]))
        flowables.append(Spacer(1, 6))

    doc.build(flowables)
    return f"Exported {len(results)} results to {filename}"

# Optional test
if __name__ == "__main__":
    test_data = [
        "AI beats humans at StarCraft II\nhttps://example.com",
        "Breakthrough in protein folding\nhttps://example.com"
    ]
    print(export_to_pdf(test_data, "test_results.pdf"))
