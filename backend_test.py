import numpy as np
import cv2 as cv
import os
from .strategies import run_best_ocr_strategy    
    
def main():
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_link = os.path.join(base_dir, './t3qWG.png')
    
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