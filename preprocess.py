import cv2 as cv
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