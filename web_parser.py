import asyncio
import os

from pyppeteer import launch


PDF_BUCKET = "pdf_bucket"


def type_url():
    url: str = input("Enter the link: ")
    url_name = url[:-1] if url.endswith("/") else url
    pdf_name = url_name.split("/")[2].replace(".", "_").replace(",", "") + ".pdf"
    pdf_path = os.path.join(PDF_BUCKET, pdf_name)
    return url, pdf_path


async def make_web_page_as_pdf(url, pdf_path_to_save):
    """Converting a web page into pdf-file"""

    browser = await launch()
    page = await browser.newPage()

    await page.goto(url=url)
    await page.pdf({"path": pdf_path_to_save, "format": "A2", "scale": 1})

    await browser.close()


url, pdf_path = type_url()


asyncio.get_event_loop().run_until_complete(make_web_page_as_pdf(url, pdf_path))
