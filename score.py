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