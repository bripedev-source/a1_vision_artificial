import os
import cv2
import json
from .. import processing
from .config import OPERATION_CATEGORY_MAP, BASE_OUTPUT_DIR

def load_image(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {path}")
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Failed to load image: {path}")
    return img

def list_images(directory: str) -> list[str]:
    """Lists supported image files in a directory."""
    exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tif')
    files = [os.path.join(directory, f) for f in os.listdir(directory) 
             if f.lower().endswith(exts)]
    return sorted(files)

def save_semantic_image(img, original_path, operation, suffix):
    """
    Saves image in a structured directory: output/{Category}/{Operation}/filename_suffix.ext
    Also generates and saves a companion histogram plot.
    """
    category = OPERATION_CATEGORY_MAP.get(operation, "Misc")
    
    # Build output directory
    # Note: BASE_OUTPUT_DIR is imported from config, make sure it's updated dynamically if needed.
    # Actually, config.BASE_OUTPUT_DIR is a constant initialized at import.
    # If configure_agent updates it, we need a way to access the updated value.
    # Better pattern: getter/setter in config or simple global access.
    # let's import the specific module to access its global variable dynamically?
    # Or just use the imported one. Python modules are singletons.
    from . import config
    base_dir = config.BASE_OUTPUT_DIR
    
    output_dir = os.path.join(base_dir, category, operation)
    os.makedirs(output_dir, exist_ok=True)
    
    # Build filename
    file_name = os.path.basename(original_path)
    name, ext = os.path.splitext(file_name)
    
    # Avoid double suffixing
    if suffix and not name.endswith(suffix):
        new_name = f"{name}_{suffix}{ext}"
    else:
        new_name = f"{name}{ext}"
        
    final_path = os.path.join(output_dir, new_name)
    
    cv2.imwrite(final_path, img)
    
    # --- Generate Visual Report ---
    try:
        report_title = f"{operation} ({suffix})"
        report_img = processing.generate_evaluation_plot(img, title=report_title)
        
        if report_img is not None:
            report_name = f"{name}_{suffix}_REPORT{ext}" if suffix else f"{name}_REPORT{ext}"
            report_path = os.path.join(output_dir, report_name)
            cv2.imwrite(report_path, report_img)
    except Exception as e:
        print(f"Warning: Failed to generate report for {final_path}: {e}")
        
    return final_path
