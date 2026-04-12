# Adaptive OCR Engine

A command-line OCR tool that performs text recognition from image and improves text recognition accuracy by running multiple preprocessing strategies


---

## Project Structure

```
ocr_project/
│
├── backend_test.py
├── preprocess.py
├── score.py
├── engine.py
├── strategies.py
├── README.md
```
---

##  Usage

To Run OCR on an image:

```bash
python backend_test.py --image path/to/image.png
```

Example:

```bash
python backend_test.py --image sample.png
```

---

## Example Output

```
Best OCR Result
Strategy: resize_adaptive
Config: --psm 6
Score: 85.23
Average Confidence: 78.45
Text: "Sample extracted text from image"
```

---

## Technologies

* Python
* OpenCV
* pytesseract
* NumPy

---

## Author

Crystal Xu
GitHub: https://github.com/CHUAIXU9804/OCR_Project_BACKEND
