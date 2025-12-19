
from .. import processing
from .io import load_image

def analyze_image_metrics(image_path: str) -> dict:
    """
    Calculates key metrics (SNR, Entropy, distribution stats) for an image.
    Used to diagnose quality issues.
    """
    img = load_image(image_path)
    
    # Calculate basic metrics
    snr = processing.calculate_snr(img)
    entropy = processing.calculate_entropy(img)
    
    # Advanced stats
    stats = processing.calculate_advanced_statistics(img)
    outliers = processing.detect_outliers_iqr(img)
    
    return {
        "snr_db": float(round(snr, 2)),
        "entropy": float(round(entropy, 3)),
        "mean_intensity": float(round(stats['mean'], 1)),
        "dynamic_range_usage_pct": float(round(stats['dynamic_usage_pct'], 1)),
        "dark_pixels_pct": float(round(stats['dark_percentage'], 1)),
        "outliers_pct": float(round(outliers['outlier_percentage'], 2)),
        "verdict": "Low Contrast/Dark" if stats['mean'] < 50 else "OK"
    }

def compute_difference(path1: str, path2: str) -> str:
    """
    Calculates absolute difference between two images.
    Returns path to difference image.
    Tema 6: Image subtraction.
    """
    from .io import save_semantic_image
    import os
    
    img1 = load_image(path1)
    img2 = load_image(path2)
    
    diff = processing.calculate_difference(img1, img2)
    
    # Force output to structured analysis folder
    name2 = os.path.splitext(os.path.basename(path2))[0]
    suffix = f"diff_vs_{name2}"
    
    return save_semantic_image(diff, path1, "difference", suffix)

def compute_average(directory: str) -> str:
    """
    Averages all images in a directory to reduce noise.
    Returns path to averaged image.
    Tema 4: Image averaging (g_bar).
    """
    from .io import save_semantic_image, list_images
    import os
    
    images_paths = list_images(directory)
    if not images_paths:
        return "Error: No images found"
        
    images = [load_image(p) for p in images_paths]
    avg_img = processing.apply_image_averaging(images)
    
    # Define a virtual path for the result based on directory name
    dir_name = os.path.basename(os.path.normpath(directory))
    dummy_path = os.path.join(directory, f"{dir_name}_average.png")
    
    return save_semantic_image(avg_img, dummy_path, "average", "result")
