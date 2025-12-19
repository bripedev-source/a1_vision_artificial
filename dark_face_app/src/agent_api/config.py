
import os

OPERATION_CATEGORY_MAP = {
    # Restoration (Tema 5)
    "gaussian": "Restoration",
    "median": "Restoration",
    "average": "Restoration",
    
    # Enhancement (Tema 6)
    "gamma": "Enhancement",
    "log": "Enhancement",
    "clahe": "Enhancement",
    "equalize": "Enhancement",
    "contrast_stretching": "Enhancement",
    "negative": "Enhancement",
    "unsharp": "Enhancement",
    
    # Analysis
    "difference": "Analysis",
    "noise_gaussian": "Simulation",
    "noise_salt_pepper": "Simulation",
    "sim_downsampling": "Simulation",
    "sim_quantization": "Simulation",
    "arithmetic": "Arithmetic",
    "add": "Arithmetic",
    "subtract": "Arithmetic",
    "multiply": "Arithmetic",
    "divide": "Arithmetic",
    "pipeline": "Pipelines"
}

BASE_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "output")
