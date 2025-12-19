
# Facade for backward compatibility and unified access
from .config import OPERATION_CATEGORY_MAP, BASE_OUTPUT_DIR
from .io import load_image, list_images, save_semantic_image
from .meta import get_capabilities, configure_agent
from .diagnostics import analyze_image_metrics, compute_difference, compute_average
from .transform import apply_transformation, add_noise, simulate_degradation, apply_arithmetic
from .workflows import run_experiment, apply_pipeline, process_batch, run_median_demo
