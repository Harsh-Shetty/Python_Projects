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


class TextExtractor:
    @staticmethod
    def extract_text(image):
        custom_config = f'--tessdata-dir "{tessdata_dir}" --psm 6 -l deu+pol'
        return pytesseract.image_to_string(image, config=custom_config)


class TextTranslator:
    @staticmethod
    def translate_text(text):
        detected_lang = detect(text)
        translator = Translator(from_lang=detected_lang, to_lang="en")
        translated_text = translator.translate(text)
        return translated_text


class ImagePreprocessor:
    @staticmethod
    def preprocess(image):
        resized_image = ImagePreprocessor.resize(image)
        gray_image = ImagePreprocessor.to_grayscale(resized_image)
        threshold_image = ImagePreprocessor.to_binary(gray_image)

        return gray_image

    @staticmethod
    def resize(image, new_width=800):
        aspect_ratio = float(image.shape[1]) / float(image.shape[0])
        new_height = int(new_width / aspect_ratio)
        return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    @staticmethod
    def to_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def to_binary(image):
        _, binary_image = cv2.threshold(
            image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        return binary_image


def capture_and_select_roi():
    def mouse_callback(event, x, y, flags, param):
        nonlocal drawing, x_start, y_start, x_end, y_end

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            x_start, y_start = x, y
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                x_end, y_end = x, y
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            x_end, y_end = x, y

    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
        sct_img = sct.grab(monitor)
        screenshot_np = np.array(sct_img)

    cv2.namedWindow("Select area and press Enter")
    cv2.setMouseCallback("Select area and press Enter", mouse_callback)

    drawing = False
    x_start, y_start, x_end, y_end = -1, -1, -1, -1

    while True:
        img_copy = screenshot_np.copy()
        if x_start != -1 and y_start != -1:
            cv2.rectangle(img_copy, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
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

    roi = (x_start, y_start, x_end - x_start, y_end - y_start)
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
preprocessed_image = ImagePreprocessor.preprocess(cropped_screenshot)
cv2.imshow("Preprocessed Image", preprocessed_image)
cv2.waitKey(0)

extracted_text = TextExtractor.extract_text(preprocessed_image)
translated_text = TextTranslator.translate_text(extracted_text)

write_to_file(translated_text)

cv2.destroyAllWindows()
