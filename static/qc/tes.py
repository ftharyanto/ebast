import subprocess
import os

def convert_xlsx_to_pdf(filename):
  """
  Converts an XLSX file to PDF using the LibreOffice command-line interface.

  Args:
    filename: Path to the input XLSX file.

  Returns:
    True if the conversion was successful, False otherwise.
  """
  try:
    command = ["soffice", "--headless", "--convert-to", "pdf:impress_pdf_Export", filename]
    subprocess.run(command, check=True) 
    return True
  except subprocess.CalledProcessError as e:
    print(f"Error converting {filename} to PDF: {e}")
    return False

# Example usage
filename = os.path.join(os.getcwd(), 'QC.xlsx')
print(filename)
convert_xlsx_to_pdf(filename)