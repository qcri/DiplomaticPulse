"""
  implements pdf/images content parsing
"""
import urllib.parse
import urllib.request
from PyPDF2 import PdfFileReader
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from io import BytesIO
import pathlib
import hashlib
import os
import ssl
import logging
import urllib3
from PIL import Image
import fitz
import pytesseract
from diplomaticpulse.misc import utils


def parse_pdfminer(url, ignore_ssl_certficate):
    """
    This method parses pdf/image content

    Args
        url (string):
            link URL
        ignore_ssl_certficate : string
            True (ignore ssl certificate)

    Returns
        dict(json):
           {
           'statement': < body text>
           'posted_date': <date posted>
           '
           }

    Raises
        Exception
             when it catches  error

    """
    # following is just to ignore https certificate issues


    ssl._create_default_https_context = ssl._create_unverified_context

    try:
        skip_extensions = [".doc", ".docx", ".img", ".jpg"]
        body = {}
        if utils.get_url_extension(url) not in skip_extensions:
            logging.propagate = False
            logging.getLogger().setLevel(logging.ERROR)
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            tmpPdffile = "/tmp/" + hashlib.sha1(url.encode("utf-8")).hexdigest()
            opener = urllib.request.build_opener()
            opener.addheaders = [
                (
                    "User-agent",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
                )
            ]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(url, tmpPdffile)
            rsrcmgr = PDFResourceManager()
            retstr = BytesIO()
            codec = "utf-8"
            laparams = LAParams()
            device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
            fp = open(tmpPdffile, "rb")
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            pagenos = set()
            for page in PDFPage.get_pages(
                fp,
                pagenos,
                maxpages=10,
                password="",
                caching=True,
                check_extractable=True,
            ):
                interpreter.process_page(page)
            text = retstr.getvalue()
            text = text.decode("utf-8")
            body["statement"] = ""
            if text:
                body["statement"] = text.strip()
                if "".join(body["statement"]).strip():
                    pdfReader = PdfFileReader(fp)
                    posted_date = (
                        pdfReader.getDocumentInfo()["/CreationDate"].replace("D:", "")
                    )[:8]
                    body["posted_date"] = (
                        posted_date[:4]
                        + "-"
                        + posted_date[4:6]
                        + "-"
                        + posted_date[6:8]
                    )
            fp.close()
            device.close()
            retstr.close()
    except Exception:
        pass

    try:
        if body["statement"] is None:
            body["statement"] = text_from_image(tmpPdffile)
    except Exception:
            dict({body["statement"] : None})
    finally:
        if pathlib.Path(tmpPdffile).exists():
            os.remove(tmpPdffile)
        return dict(body)


def get_text_from_pdf_image(file_):
    """
    This method scrapes pdf/image text from file

    Args
        file_(string):
            pdf filename


    Returns
        text (string):
            pdf image  content

    Raises
        Exception
             when it catches  error

    """
    tmp_png_files = []
    try:
        content = []
        doc = fitz.open(file_)
        for i in range(len(doc)):
            for img in doc.getPageImageList(i):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 5:
                    pix.writePNG("p%s-%s.png" % (i, xref))
                    img = Image.open("p%s-%s.png" % (i, xref))
                    content.append(pytesseract.image_to_string(img))
                    tmp_png_files.append("p%s-%s.png" % (i, xref))
                else:
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.writePNG("p%s-%s.png" % (i, xref))
                    img = Image.open("p%s-%s.png" % (i, xref))
                    content.append(pytesseract.image_to_string(img))
                    tmp_png_files.append("p%s-%s.png" % (i, xref))
    except Exception:
        if pathlib.Path(file_).exists():
            os.remove(file_)
    try:
        for f in tmp_png_files:
            os.remove(f)
    except Exception:
        pass
    return "\n".join(content)
