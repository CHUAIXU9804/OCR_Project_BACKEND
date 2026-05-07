from preprocess import (
    get_gray_scale,
    gray_otsu,
    resize_otsu,
    resize_adaptive,
    resize_light_blur_adaptive,
    invert_process,
)
from engine import run_tesseract_with_data
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
        "--psm 3",
        "--psm 4",
        "--psm 5",
        "--psm 6",
        "--psm 7",
        "--psm 8",
        "--psm 9",
        "--psm 10",
        "--psm 11",
        "--psm 12",
        "--psm 13",
    ]
    
    best_score = -1
    best_text = ""
    best_strategy = None
    best_config = None
    best_avg_conf = 0
    processed = None
    score, text, avg_conf = 0, "", 0
    for strategy_name, preprocess_method in strategies:
        # print(f"strategy {strategy_name}")
        try:
            processed = preprocess_method(img)
        except Exception:
            continue
        
        for config in configs:
            try:
                score, text, avg_conf = run_tesseract_with_data(processed, config)
            except Exception:
                continue
            """
            print(
            f"Strategy={strategy_name}, config={config}, "
            f"Score={score:.2f}, AvgConf={avg_conf:.2f}, text={repr(text)}"
            )
            """
        
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
            "avg_conf": best_avg_conf,
             
        }