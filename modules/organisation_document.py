from bs4 import BeautifulSoup   #scraping by using the BeautifulSoup package

import sys
import PyPDF2

sys.path.append("./../")

from services.database_service import add_organisation_document_to_db
from nlp import language_processing

from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from io import StringIO

def add_organisation_document():

    module = "Operating Systems (OS)"
    module = module.lower()

    pdf_document_name = "organisation.pdf"

    #fp = open('organisation.pdf', 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp =  open(pdf_document_name, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    text.rstrip()

    fp.close()
    device.close()
    retstr.close()

    add_organisation_document_to_db(module, text)

    #print("TEXT: " + str(text))

if __name__ == '__main__':
    add_organisation_document()
