try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

def extract_text_from_image(image_path):
    if not OCR_AVAILABLE:
        return "OCR not available. Please install: pip install pytesseract pillow"
    
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_text_from_pdf_images(pdf_path):
    try:
        import fitz
        
        doc = fitz.open(pdf_path)
        text = ""
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_text = page.get_text()
            
            if len(page_text.strip()) < 50:
                pix = page.get_pixmap()
                img_path = f"temp_page_{page_num}.png"
                pix.save(img_path)
                
                ocr_text = extract_text_from_image(img_path)
                text += ocr_text + "\n"
                
                import os
                os.remove(img_path)
            else:
                text += page_text + "\n"
        
        return text
    
    except Exception as e:
        return f"Error: {str(e)}"