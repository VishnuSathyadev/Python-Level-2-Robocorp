from RPA.HTTP import HTTP
from robocorp import browser
import pandas as pd
from RPA.PDF import PDF
import shutil
from Resources.Merged_pdf import *
import os


def download_excel_file():
    """Downloads excel file from the given URL"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)


def read_csv_file():
    """Read data from csv"""
    table = pd.read_csv("orders.csv")
    return table

def fill_orders(index, row):
    page = browser.page()
    if index == 0:
        browser.goto("https://robotsparebinindustries.com/#/robot-order")
    page.click("button:has-text('OK')")
    page.select_option('//select[@id="head"]', str(row["Head"]))
    page.click(f'//input[@id="id-body-{str(row["Body"])}"]')
    page.fill(f'//input[@type="number"]', str(row["Legs"]))
    page.fill(f'//input[@name="address"]', str(row["Address"]))
    page.click("#order")
    while page.is_visible(f'//div[@role="alert" and (contains(text(),"Error") or contains(text(),"Again"))]'):
        page.click("#order")
        page.wait_for_timeout(1000)
    order_number=export_as_pdf()
    screenshot_robot(order_number)
    embed_screenshot_to_receipt(order_number)
    page.click(f'//button[@id="order-another"]')


def export_as_pdf():
    """Export the receipt to a pdf file"""
    page = browser.page()
    sales_results_html = page.locator(f'//div[@id="receipt"]').inner_html()
    text = page.text_content(f'//p[@class="badge badge-success"]')
    pdf = PDF()
    pdf.html_to_pdf(sales_results_html, "output/Receipt/Receipt_"+text+".pdf")
    return text


def screenshot_robot(order_number):
    """Take a screenshot of the robot"""
    page = browser.page()
    element = page.query_selector(f'//div[@id="robot-preview-image"]')
    element.screenshot(path="output/Screenshots/"+order_number+".png")


# def embed_screenshot_to_receipt(order_number):
#     from fpdf import FPDF
#     pdf = FPDF()
#     pdf.add_page()
#     image_path = "output/Screenshots/"+order_number+".png"
#     pdf.image(image_path, x=10, y=10, w=190)  # Adjust x, y, w as needed
#     pdf.output("output/Receipt/Receipt_"+order_number+".pdf")

def archive_receipts():
    """Zips the specified folder into a zip file."""
    folder_to_zip = "output/Merged_Pdfs" 
    zip_file_name = "output/Zipped_Folder"
    shutil.make_archive(zip_file_name, 'zip', folder_to_zip)

def delete_all_files_in_folder(folder_path):
    """Deletes all files in the specified folder."""
    try:
        # Iterate through all files in the specified directory
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # Check if it's a file
            if os.path.isfile(file_path):
                os.remove(file_path)  # Delete the file
            elif os.path.isdir(file_path):
                print(f"Found a directory (not deleted): {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
