
import json
import os
import cv2
from .. import processing
from .io import load_image, save_semantic_image

def _execute_step(image, op, params):
    """
    Applies a single operation to an image in memory.
    Centralizes all syllabus logic.
    """
    if op == "gamma":
        return processing.apply_gamma(image, float(params.get("gamma", 1.0)))
    elif op == "clahe":
        return processing.apply_clahe(image, clip_limit=float(params.get("clip_limit", 2.0)))
    elif op == "median":
        return processing.apply_median_filter(image, int(params.get("kernel_size", 3)))
    elif op == "log":
        return processing.apply_log_transform(image)
    elif op == "equalize":
        return processing.apply_equalization(image)

    elif op == "gaussian":
        return processing.apply_gaussian_filter(image, kernel_size=int(params.get("kernel_size", 5)), sigma=float(params.get("sigma", 0)))
    elif op == "noise_gaussian":
        return processing.add_gaussian_noise(image, mean=float(params.get("mean", 0)), sigma=float(params.get("sigma", 25)))
    elif op == "noise_salt_pepper":
        return processing.add_salt_pepper_noise(image, prob=float(params.get("prob", 0.05)))
    elif op == "sim_downsampling":
        return processing.simulate_downsampling(image, factor=float(params.get("factor", 0.5)))
    elif op == "sim_quantization":
        return processing.simulate_quantization(image, bits=int(params.get("bits", 3)))
    elif op == "arithmetic":
        # Load second image
        img2_path = params.get("image2_path")
        if not img2_path or not os.path.exists(img2_path):
            raise ValueError(f"Arithmetic op requires valid 'image2_path'. Got: {img2_path}")
        img2 = cv2.imread(img2_path)
        if img2 is None:
             raise ValueError(f"Could not load image2 from {img2_path}")
        return processing.apply_arithmetic_ops(image, img2, operation=params.get("operation", "add"))
    else:
        raise ValueError(f"Unknown operation: {op}")

def apply_transformation(image_path: str, operation: str, params: str = "{}") -> str:
    """
    Applies a single transformation to an image and saves the result.
    Wraps the shared logic.
    """
    try:
        parameters = json.loads(params)
    except:
        parameters = {}
        
    img = load_image(image_path)
    
    try:
        result_img = _execute_step(img, operation, parameters)
    except ValueError as e:
        raise ValueError(str(e))
        
    # Generate meaningful suffix
    if operation == "gamma":
        suffix = f"gamma{parameters.get('gamma', 1.0)}"
    elif operation == "clahe":
        suffix = f"clahe{parameters.get('clip_limit', 2.0)}"
    elif operation == "median":
        suffix = f"median{parameters.get('kernel_size', 3)}"
    elif operation == "gaussian":
        suffix = f"gauss{parameters.get('kernel_size', 5)}"
    elif operation == "arithmetic":
        sub_op = parameters.get("operation", "arithmetic")
        suffix = f"{sub_op}"
        operation = sub_op 

    elif operation.startswith("noise_"):
        simple_name = operation.replace("noise_", "")
        if "sigma" in parameters:
            suffix = f"{simple_name}_sigma{parameters['sigma']}"
        elif "prob" in parameters:
            suffix = f"{simple_name}_prob{parameters['prob']}"
        else:
            suffix = simple_name

    elif operation.startswith("sim_"):
        simple_name = operation.replace("sim_", "")
        if "factor" in parameters:
            suffix = f"{simple_name}_{parameters['factor']}"
        elif "bits" in parameters:
            suffix = f"{simple_name}_{parameters['bits']}bits"
        else:
            suffix = simple_name
    else:
        suffix = operation
        
    return save_semantic_image(result_img, image_path, operation, suffix)

def add_noise(image_path: str, type: str, params: str = "{}") -> str:
    return apply_transformation(image_path, "noise_" + type if not type.startswith("noise_") else type, params)

def simulate_degradation(image_path: str, type: str, params: str = "{}") -> str:
    return apply_transformation(image_path, "sim_" + type if not type.startswith("sim_") else type, params)

def apply_arithmetic(image1_path: str, image2_path: str, operation: str) -> str:
    return apply_transformation(image1_path, "arithmetic", f'{{"operation": "{operation}", "image2_path": "{image2_path.replace(os.sep, "/")}"}}')
