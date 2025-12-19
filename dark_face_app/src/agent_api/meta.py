import json
import os
from . import config

def get_capabilities() -> dict:
    """
    Returns the agent's capabilities, valid operations, and parameter schemas.
    Collaborative entities should use this to construct valid requests.
    """
    return {
        "agent_version": "2.0.0 (Scientific/Traceable)",
        "supported_workflows": [
            "run_experiment (dynamic strategy comparison)",
            "apply_pipeline (multi-step traceable transformation)",
            "process_batch_pipeline (mass application)"
        ],
        "operations_schema": {
            "gamma": {
                "description": "Power-law transformation for brightness adjustment.",
                "params": {"gamma": "float (0.1 - 3.0)"},
                "syllabus_topic": "Topic 6"
            },
            "clahe": {
                "description": "Contrast Limited Adaptive Histogram Equalization.",
                "params": {"clip_limit": "float (1.0 - 4.0)"},
                "syllabus_topic": "Topic 6"
            },
            "equalize": {
                "description": "Global Histogram Equalization.",
                "params": {},
                "syllabus_topic": "Topic 6"
            },
            "log": {
                "description": "Logarithmic transformation for expanding dark dynamic range.",
                "params": {},
                "syllabus_topic": "Topic 6"
            },
            "median": {
                "description": "Median filter for salt-and-pepper noise reduction.",
                "params": {"kernel_size": "int (odd: 3, 5, 7)"},
                "syllabus_topic": "Topic 5"
            },
            "gaussian": {
                "description": "Gaussian blur for general noise reduction.",
                "params": {"kernel_size": "int (odd, default 5)", "sigma": "float (default 0=auto)"},
                "syllabus_topic": "Topic 5"
            },
            "unsharp": {
                "description": "Unsharp masking for edge enhancement.",
                "params": {"sigma": "float (default 1.0)", "strength": "float (default 1.5)"},
                "syllabus_topic": "Topic 6"
            },
            "noise_gaussian": {
                "description": "Add Gaussian Noise (Thermal/Electronic simulation).",
                "params": {"mean": "float (default 0)", "sigma": "float (default 25)"},
                "syllabus_topic": "Topic 4"
            },
            "noise_salt_pepper": {
                "description": "Add Salt & Pepper Noise (Impulsive simulation).",
                "params": {"prob": "float (0.0 - 1.0, default 0.05)"},
                "syllabus_topic": "Topic 4"
            },
            "sim_downsampling": {
                "description": "Simulate resolution reduction (Aliasing).",
                "params": {"factor": "float (0.1 - 1.0, default 0.5)"},
                "syllabus_topic": "Topic 3"
            },
            "sim_quantization": {
                "description": "Simulate bit-depth reduction (Posterization).",
                "params": {"bits": "int (1-8, default 3)"},
                "syllabus_topic": "Topic 3"
            },
            "arithmetic": {
                "description": "Topic 6 Arithmetic Operations (Add, Sub, Mult, Div).",
                "params": {"operation": "str (add, subtract, multiply, divide)", "image2_path": "str (absolute path)"},
                "syllabus_topic": "Topic 6"
            }
        },
        "output_structure": {
            "experiments": "{base}/Experiments/{image_name}_{timestamp}/",
            "pipelines": "{base}/Pipelines/{image_name}_{timestamp}_Flow/"
        }
    }

def configure_agent(config_json: str) -> dict:
    """
    Updates the agent's runtime configuration.
    """
    try:
        conf = json.loads(config_json)
        if "base_output_dir" in conf:
            new_dir = conf["base_output_dir"]
            os.makedirs(new_dir, exist_ok=True)
            config.BASE_OUTPUT_DIR = new_dir
            return {"status": "success", "message": f"Output directory updated to {config.BASE_OUTPUT_DIR}"}
        return {"status": "ignored", "message": "No valid configuration keys found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
