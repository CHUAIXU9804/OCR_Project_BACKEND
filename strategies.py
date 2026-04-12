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
            "avg_config": best_avg_conf,
             
        }