import numpy as np
import cv2 as cv
import os
from strategies import run_best_ocr_strategy    
import argparse

def load_image(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {path}")

    img = cv.imread(path)
    if img is None:
        raise ValueError("Failed to load image")

    return img
def parse_args():
    parser = argparse.ArgumentParser(description="OCR CLI")
    parser.add_argument("--image", required=True, help="Path to image")
    return parser.parse_args()
    
def main():
    args = parse_args()
    img = load_image(args.image)

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