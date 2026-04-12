import numpy as np
import pytesseract
import cv2 as cv
import os
from pytesseract import Output

# Simple processing - for clear image processing
def ocr_image (img):
    config = "--psm 6"
    text = pytesseract.image_to_string(img, config=config)
    return text


# Get gray scale image
def get_gray_scale(img):
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)


# General Purpose - when dark text on lght background
def gray_otsu (img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    return cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

# when text is small or tiny resolution
def resize_otsu (img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.resize(gray, None, fx=2, fy=2, interpolation=cv.INTER_CUBIC)
    return cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

# for colorful or bright background, or normal thresholding loses value
def resize_adaptive (img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.resize(gray, None, fx=2, fy=2, interpolation=cv.INTER_CUBIC)
    adaptive = cv.adaptiveThreshold(
    gray, 255,
    cv.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv.THRESH_BINARY,
    31, 11
)
    return adaptive


# when image has noise, background is messy, or text edges are rough
def resize_light_blur_adaptive (img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.resize(gray, None, fx=2, fy=2, interpolation=cv.INTER_CUBIC)
    gray = cv.GaussianBlur(gray, (3, 3), 0)
    adaptive = cv.adaptiveThreshold(
        gray, 255,
        cv.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv.THRESH_BINARY,
        31, 11
    )
    return adaptive
# when text is light on dark_background    
def invert_process (img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
    inverted = cv.bitwise_not(binary)
    return inverted

def score_text (data):
    """
    Run Tesseract on each image version
    Collect structured OCR data
    score by confidence and text quality
    Keep he strongest result
    """
    valid_words = []
    valid_confs = []
    for text, conf in zip(data["text"], data["conf"]):
        text = text.strip()
        
        try:
            conf = float(conf)
        except ValueError:
            continue
        
        if text and conf >= 0:
            valid_words.append(text)
            valid_confs.append(conf)
    # print(f"valid words: {valid_words}")
    if not valid_words:
            return 0, "", 0
    extracted_text = " ".join(valid_words)
    avg_conf = sum(valid_confs) / len(valid_confs)
    score = avg_conf + len(valid_words) * 2
    
    return score, extracted_text, avg_conf

def run_tesseract_with_data (img, config):
    data = pytesseract.image_to_data(img, config=config, output_type= Output.DICT)
    return score_text(data)
    
def run_best_ocr_strategy (img):
    strategies = [
        ("gray", get_gray_scale),
        ("gray_otsu", gray_otsu),
        ("resize_otsu", resize_otsu),
        ("resize_adaptive", resize_adaptive),
        ("resize_light_blur_adaptive", resize_light_blur_adaptive),
        ("invert_process", invert_process),
    ]
    configs = [
        "--psm 6",
        "--psm 7",
        "--psm 11",
    ]
    
    best_score = -1
    best_text = -1
    best_strategy = None
    best_config = None
    best_avg_conf = 0
    
    for strategy_name, preprocess_method in strategies:
        # print(f"strategy {strategy_name}")
        processed = preprocess_method(img)
        
        for config in configs:
            score, text, avg_conf = run_tesseract_with_data(processed, config)
            print(
            f"Strategy={strategy_name}, config={config}, "
            f"Score={score:.2f}, AvgConf={avg_conf:.2f}, text={repr(text)}"
            )
        
            if score > best_score:
                best_score = score
                best_text = text
                best_strategy = strategy_name
                best_config = config
                best_avg_conf = avg_conf
        
    return {
            "score": best_score,
            "text": best_text,
            "strategy": best_strategy,
            "config": best_config,
            "avg_config": best_avg_conf,
             
        }
    
def main():
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_link = os.path.join(base_dir, 't3qWG.png')
    
    img = cv.imread(img_link)
    if img is None:
        print("Failed to load image")
        return
    # Perform image pre-processing

    result = run_best_ocr_strategy(img)
    print(f"\nBest OCR Result \nStrategy: {result['strategy']}\nConfig: {result['config']}\nScore: {result['score']}\nAverage Confidence: {result['avg_config']}\nText: {result['text']}")
    """
    img = get_gray_scale(img)
    img = threshold_setup(img)
    img = remove_noise(img)
    print(ocr_image(img))
    """
    

    

if __name__ == "__main__":
    main()