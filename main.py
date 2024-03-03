import os
import zipfile
import PyPDF2

from typing import List
from dotenv import load_dotenv

load_dotenv()

class PDFSplitter():
    """Handles splitting pdfs by page number."""
    path: str
    def __init__(self, path: str) -> None:
        self.path = path

    def __get_basename(self) -> str:
        """Gets filename exluding extension."""
        return os.path.basename(self.path).replace(".pdf", "")

    def split(self, slices: List[List[int]], result_dir: str, zip: bool = False, zip_file: str = "") -> None:
        """Splits PDF into separate files given a list of integer lists indicating the page that should be included
        in each PDF.
        :param slices: List of lists of pdf page numbers (0 - based)
        
        :return: None 
        """
        files: list[str] = list()
        if not result_dir:
            result_dir = os.path.dirname(self.path)
        
        with open(self.path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for i, slice in enumerate(slices):
                filename = f"{result_dir}{self.__get_basename()}_{i+1}.pdf"
                files.append(filename)
                merger = PyPDF2.PdfWriter()
                for page_num in range(len(reader.pages)):
                    if page_num in slice:
                        page = reader.pages[page_num]
                        merger.add_page(page) 
                merger.write(filename)
                merger.close()
        if zip:
            if zip_file:
                filename = zip_file
            else:
                filename = f"{os.path.basename(self.path)[:-4]}.zip"
            with zipfile.ZipFile(self.path, "w") as zipf:
                zipf.write(filename)

def main():
    path = os.getenv("FILE_PATH")
    zip_filename = f"{os.path.basename(path)[:-4]}.zip"
    result_dir = os.getenv("RESULT_DIR")
    splitter = PDFSplitter(path)
    pages = []
    pages.append([0,2])
    pages.append([1,3])
    splitter.split(pages, result_dir)
    splitter.split(pages, result_dir, zip=True, zip_file=zip_filename)

main()