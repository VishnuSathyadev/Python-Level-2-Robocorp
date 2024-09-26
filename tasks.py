from robocorp.tasks import task
from robocorp import browser
from Resources.Download_csv import *

@task
def robot_spare_bin_python():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    browser.configure(
        slowmo=100,
    )
    screenshot_path= f"output/Screenshots"
    reciept_path = f"output/Receipt"
    mergedPdf_path = f"output/Merged_Pdfs"
    delete_all_files_in_folder(mergedPdf_path)
    delete_all_files_in_folder(reciept_path)
    delete_all_files_in_folder(screenshot_path)

    download_excel_file()
    table = read_csv_file()
    print(table)

    for index, row in table.iterrows():
        fill_orders(index, row)

    archive_receipts()