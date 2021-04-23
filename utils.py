import json
import pytesseract as tsc
from PIL import Image
import os
import fitz

#pdb.set_trace()
tsc.pytesseract.tesseract_cmd = r".\Tesseract-OCR\tesseract.exe"

def ocr_text(filename):
    """
    Retorna el texto del archivo que obtiene desde la pagina web
    """
    text = tsc.image_to_string(filename, config='--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ-1234567890')  
    if r"\n\x0c" in text:
        text = text.replace(r"\n\x0c", "")
    elif r"\n\f" in text:
        text = text.replace(r"\n\f", "")
    if text == "":
        text = "No se pudo procesar la imagen"
    if os.path.exists(filename):
        os.remove(filename)
    return text

def pdf_to_text(filename):
    text=""
    doc = fitz.open(filename)
    cant_page = doc.page_count
    for i in range(cant_page):
        page = doc.loadPage(i)  # number of page
        text += str(page.get_text())
    if text == "":
        text = "No se pudo procesar pdf"
    doc.close()
    if os.path.exists(filename):
        os.remove(filename)
    return text

def pdf_to_text_json(filename):
    doc = fitz.open(filename)
    cant_page = doc.page_count
    for i in range(cant_page):
        page = doc.loadPage(i)  # number of page
        text = page.get_text("json")
        jsoneado = json.dumps(text)
    if jsoneado == "":
        jsoneado = "No se pudo procesar pdf"
    doc.close()
    if os.path.exists(filename):
        os.remove(filename)
    return jsoneado

def pdf_to_text_html(filename):
    text=""
    doc = fitz.open(filename)
    cant_page = doc.page_count
    for i in range(cant_page):
        page = doc.loadPage(i)  # number of page
        text += str(page.get_text("html"))
    if text == "":
        text = "No se pudo procesar pdf"
    doc.close()
    if os.path.exists(filename):
        os.remove(filename)
    return text


def ocr_json(filename):
    """
    Retorna el texto del archivo que obtiene desde la pagina web en Formato json
    """
    diccionario_out={}
    text = tsc.image_to_string(filename, config='--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ-1234567890')  
    if r"\n\x0c" in text:
        text = text.replace(r"\n\x0c", "")
    text = text.replace("\n\x0c", "")
    
    for idx,lines in enumerate(text.split("/n")):
        diccionario_out = {"Output":{f"Line: {idx}": lines}}
        json_out = json.dumps(diccionario_out)
    if json_out == "":
        json_out = "No se pudo procesar la imagen"
    if os.path.exists(filename):
        os.remove(filename)
    return json_out

def create_pdf(filename):
    pdf = tsc.image_to_pdf_or_hocr(filename, config='--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ-1234567890')  
    if os.path.exists("demo.pdf"):
        os.remove("demo.pdf")
    with open("demo.pdf", "wb") as f:
        f.write(bytearray(pdf))



if __name__ == "__main__":
    pass
    # print(ocr_text(r'C:\Users\novasrodrigo\Desktop\OcrTorch\imagenes\Peru.jpg'))
    # print(ocr_json(r'C:\Users\novasrodrigo\Desktop\OcrTorch\imagenes\Peru.jpg'))
    # print(pdf_to_text(r'categoria-b.pdf'))
    # print(pdf_to_text_json(r'categoria-b.pdf'))
    # print(pdf_to_text_html(r'categoria-b.pdf'))
    #create_pdf(r'C:\Users\novasrodrigo\Desktop\OcrTorch\imagenes\Patente.jpg')