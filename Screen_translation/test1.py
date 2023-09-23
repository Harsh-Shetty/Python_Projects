import os
from pathlib import Path

import cv2
import mss
import numpy as np
import pytesseract
from langdetect import detect
from translate import Translator

tessdata_dir = Path(__file__).resolve().parent / "Tesseract"
tesseract_exe = tessdata_dir / "tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = str(tesseract_exe)

tessdata_dir = tessdata_dir / "tessdata"
os.environ["TESSDATA_PREFIX"] = str(tessdata_dir)


class ImageProcessor:
    @staticmethod
    def grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def invert(image):
        return cv2.bitwise_not(image)

    @staticmethod
    def resize(image):
        return cv2.resize(image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)


class TextExtractor:
    @staticmethod
    def extract_text(image):
        custom_config = f'--tessdata-dir "{tessdata_dir}"'
        return pytesseract.image_to_string(image, config=custom_config)


class TextTranslator:
    @staticmethod
    def translate_text(text):
        detected_lang = detect(text)
        translator = Translator(from_lang=detected_lang, to_lang="en")
        translated_text = translator.translate(text)
        return translated_text


def preprocess_image(image):
    preprocessor = ImageProcessor()
    resized_image = preprocessor.resize(image)
    inverted_image = preprocessor.invert(resized_image)
    gray_image = preprocessor.grayscale(inverted_image)

    # cv2.imshow("resized_image", gray_image)
    cv2.waitKey(0)
    return gray_image


def capture_and_select_roi():
    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
        sct_img = sct.grab(monitor)
        screenshot_np = np.array(sct_img)

    cv2.imshow("Select area and press Enter", screenshot_np)

    roi = cv2.selectROI("Select area and press Enter", screenshot_np, False, False)
    x_coord, y_coord, width, height = roi
    cropped_screenshot = screenshot_np[
        y_coord : y_coord + height, x_coord : x_coord + width
    ]
    cv2.destroyAllWindows()

    return cropped_screenshot


def write_to_file(translated_text, folder="temp", filename="translated_text.txt"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(translated_text)
    os.startfile(os.path.abspath(filepath))


cropped_screenshot = capture_and_select_roi()
preprocessed_image = preprocess_image(cropped_screenshot)

extracted_text = TextExtractor.extract_text(preprocessed_image)
translated_text = TextTranslator.translate_text(extracted_text)

write_to_file(translated_text)

cv2.destroyAllWindows()
