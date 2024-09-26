from RPA.PDF import PDF
from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter

def embed_screenshot_to_receipt(order_number):
    # Paths for the existing and new PDFs
    existing_pdf_path = f"output/Receipt/Receipt_{order_number}.pdf"
    screenshot_pdf_path = f"output/Screenshots/{order_number}.pdf"
    
    # Create a PDF with the screenshot
    pdf = FPDF()
    pdf.add_page()
    image_path = f"output/Screenshots/{order_number}.png"
    pdf.image(image_path, x=5, y=5, w=100)  # Adjust x, y, w as needed
    pdf.output(screenshot_pdf_path)

    # Merge the existing PDF and the screenshot PDF
    pdf_writer = PdfWriter()

    # Read existing PDF
    with open(existing_pdf_path, "rb") as existing_pdf_file:
        pdf_reader = PdfReader(existing_pdf_file)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

    # Read the screenshot PDF
    with open(screenshot_pdf_path, "rb") as screenshot_pdf_file:
        screenshot_reader = PdfReader(screenshot_pdf_file)
        for page in screenshot_reader.pages:
            pdf_writer.add_page(page)

    # Save the merged PDF
    merged_pdf_path = f"output/Merged_Pdfs/Merged_Receipt_{order_number}.pdf"
    with open(merged_pdf_path, "wb") as output_pdf_file:
        pdf_writer.write(output_pdf_file)