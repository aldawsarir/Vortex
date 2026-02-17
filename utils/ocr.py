import os

def extract_text_from_image(image_path):
    """
    استخراج النص من الصور
    """
    try:
        # محاولة استخدام Tesseract OCR
        return _extract_with_tesseract(image_path)
    except Exception as e:
        print(f"❌ OCR Error: {str(e)}")
        # إذا فشل Tesseract، جرب PIL فقط
        return _extract_with_pil(image_path)

def _extract_with_tesseract(image_path):
    """استخراج النص باستخدام Tesseract"""
    try:
        import pytesseract
        from PIL import Image
        import cv2
        import numpy as np

        # ✅ جرب مسارات Tesseract المختلفة
        tesseract_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            r'C:\Users\rawan\AppData\Local\Programs\Tesseract-OCR\tesseract.exe',
            'tesseract'  # إذا كان في PATH
        ]

        tesseract_found = False
        for path in tesseract_paths:
            if path == 'tesseract' or os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                tesseract_found = True
                print(f"✅ Tesseract found at: {path}")
                break

        if not tesseract_found:
            print("❌ Tesseract not found! Trying PIL fallback...")
            return _extract_with_pil(image_path)

        # قراءة الصورة
        img = cv2.imread(image_path)

        if img is None:
            # جرب PIL إذا فشل cv2
            from PIL import Image
            pil_img = Image.open(image_path)
            text = pytesseract.image_to_string(pil_img, lang='eng')
            print(f"✅ OCR (PIL) extracted {len(text)} characters")
            return text.strip()

        # تحسين الصورة
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        _, threshold = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # استخراج النص - جرب إنجليزي أولاً
        try:
            text = pytesseract.image_to_string(threshold, lang='eng+ara')
        except:
            text = pytesseract.image_to_string(threshold, lang='eng')

        print(f"✅ OCR extracted {len(text)} characters from image")
        return text.strip()

    except ImportError as e:
        print(f"❌ Missing library: {e}")
        return _extract_with_pil(image_path)
    except Exception as e:
        print(f"❌ Tesseract error: {e}")
        return _extract_with_pil(image_path)

def _extract_with_pil(image_path):
    """استخراج بسيط باستخدام PIL فقط (fallback)"""
    try:
        from PIL import Image
        img = Image.open(image_path)
        print(f"✅ Image opened with PIL: {img.size}")
        # PIL وحده لا يستطيع OCR - نرجع رسالة توضيحية
        return ""
    except Exception as e:
        print(f"❌ PIL error: {e}")
        return ""

def is_image_file(filename):
    """التحقق من امتداد الصورة"""
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'gif', 'webp'}
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return ext in ALLOWED_IMAGE_EXTENSIONS

def preprocess_image_for_ocr(image_path, output_path=None):
    """معالجة مسبقة للصورة"""
    try:
        import cv2
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if output_path:
            cv2.imwrite(output_path, binary)
        return binary
    except Exception as e:
        print(f"❌ Image preprocessing error: {e}")
        return None