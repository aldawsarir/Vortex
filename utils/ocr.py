import pytesseract
from PIL import Image
import cv2
import numpy as np
import os

# ✅ تحديد مسار Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    """
    استخراج النص من الصور باستخدام OCR
    يدعم: PNG, JPG, JPEG, BMP, TIFF
    """
    try:
        # قراءة الصورة
        img = cv2.imread(image_path)
        
        if img is None:
            print(f"❌ Could not read image: {image_path}")
            return ""
        
        # تحسين جودة الصورة للـ OCR
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # إزالة الضوضاء
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        # زيادة التباين
        _, threshold = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # استخراج النص باستخدام Tesseract
        # دعم العربية والإنجليزية
        text = pytesseract.image_to_string(threshold, lang='eng+ara')
        
        print(f"✅ OCR extracted {len(text)} characters from image")
        
        return text.strip()
    
    except Exception as e:
        print(f"❌ OCR Error: {str(e)}")
        return ""

def is_image_file(filename):
    """التحقق من امتداد الصورة"""
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'gif', 'webp'}
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return ext in ALLOWED_IMAGE_EXTENSIONS

def preprocess_image_for_ocr(image_path, output_path=None):
    """
    معالجة مسبقة للصورة لتحسين دقة OCR
    """
    try:
        img = cv2.imread(image_path)
        
        # تحويل لـ grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # إزالة الضوضاء
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        # تحسين التباين
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        # Thresholding
        _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        if output_path:
            cv2.imwrite(output_path, binary)
        
        return binary
    
    except Exception as e:
        print(f"❌ Image preprocessing error: {e}")
        return None