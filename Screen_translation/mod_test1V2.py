import os
from pathlib import Path

import cv2
import mss
import numpy as np
import pytesseract
from langdetect import detect
from translate import Translator

# Set up Tesseract
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
    def __init__(self, image):
        self.image = image

    def extract_text(self):
        custom_config = f'--tessdata-dir "{tessdata_dir}"'
        return pytesseract.image_to_string(self.image, config=custom_config)


class TextTranslator:
    def __init__(self, text):
        self.text = text

    def translate_text(self):
        detected_lang = detect(self.text)
        translator = Translator(from_lang=detected_lang, to_lang="en")
        translated_text = translator.translate(self.text)
        return translated_text


class ScreenCapturer:
    def capture_screenshot(self):
        with mss.mss() as sct:
            monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
            sct_img = sct.grab(monitor)
            screenshot_np = np.array(sct_img)
        return screenshot_np


class ROISelector:
    def __init__(self, image):
        self.image = image
        self.drawing = False
        self.x_start, self.y_start, self.x_end, self.y_end = -1, -1, -1, -1

    def _mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.x_start, self.y_start = x, y
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                self.x_end, self.y_end = x, y
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.x_end, self.y_end = x, y

    def select_roi(self):
        cv2.namedWindow("Select area and press Enter")
        cv2.setMouseCallback("Select area and press Enter", self._mouse_callback)

        while True:
            img_copy = self.image.copy()
            if self.x_start != -1 and self.y_start != -1:
                cv2.rectangle(
                    img_copy,
                    (self.x_start, self.y_start),
                    (self.x_end, self.y_end),
                    (0, 255, 0),
                    2,
                )
            cv2.imshow("Select area and press Enter", img_copy)

            key = cv2.waitKey(1) & 0xFF

            if cv2.getWindowProperty("Select area and press Enter", 0) < 0:
                cv2.destroyAllWindows()
                return None

            if key == 27:  # Escape key
                cv2.destroyAllWindows()
                return None
            elif key == ord("\r") or key == ord("\n"):  # Enter key
                break

        roi = (
            self.x_start,
            self.y_start,
            self.x_end - self.x_start,
            self.y_end - self.y_start,
        )
        x_coord, y_coord, width, height = roi
        cropped_image = self.image[
            y_coord : y_coord + height, x_coord : x_coord + width
        ]
        cv2.destroyAllWindows()

        return cropped_image


def write_to_file(translated_text, folder="temp", filename="translated_text.txt"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(translated_text)
    os.startfile(os.path.abspath(filepath))


capturer = ScreenCapturer()
screenshot_np = capturer.capture_screenshot()

roi_selector = ROISelector(screenshot_np)
cropped_screenshot = roi_selector.select_roi()

if cropped_screenshot is not None:
    preprocessor = ImageProcessor()
    resized_image = preprocessor.resize(cropped_screenshot)
    inverted_image = preprocessor.invert(resized_image)
    gray_image = preprocessor.grayscale(inverted_image)

    extractor = TextExtractor(gray_image)
    extracted_text = extractor.extract_text()

    translator = TextTranslator(extracted_text)
    translated_text = translator.translate_text()

    write_to_file(translated_text)

    cv2.destroyAllWindows()
