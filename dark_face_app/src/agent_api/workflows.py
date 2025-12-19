
import json
import os
import datetime
import cv2
import numpy as np
from .. import processing
from .config import BASE_OUTPUT_DIR
from .io import load_image
from .transform import _execute_step

# NOTE: circular import potential if apply_pipeline uses workflows.
# Wait, 'apply_pipeline' (single image) is currently in agent_api (transform or workflow?)
# In legacy agent_api, 'apply_pipeline' was separate.
# In my new 'transform.py', I strictly put single-op logic.
# 'apply_pipeline' is multiple ops, so it belongs here in workflows.
# Let's fix 'process_batch' to use 'apply_pipeline' from here.

def apply_pipeline(image_path: str, steps_json: str) -> dict:
    """
    Applies a sequence of transformations, saving separate intermediate artifacts
    for EVERY step to allow full scientific traceability.
    """
    try:
        steps = json.loads(steps_json)
    except:
        return {"error": "Invalid JSON"}
        
    img = load_image(image_path)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create Pipeline Flow Directory
    flow_dir = os.path.join(BASE_OUTPUT_DIR, "Pipelines", f"{base_name}_{timestamp}_Flow")
    os.makedirs(flow_dir, exist_ok=True)
    
    artifacts = []
    current_img = img.copy()
    
    # Save Step 0 (Original)
    step0_name = "00_original.png"
    step0_path = os.path.join(flow_dir, step0_name)
    cv2.imwrite(step0_path, current_img)
    # Generate Report 0
    step0_rep = processing.generate_evaluation_plot(current_img, title="Step 0: Original")
    if step0_rep is not None:
        cv2.imwrite(os.path.join(flow_dir, "00_original_REPORT.png"), step0_rep)
    artifacts.append(step0_path)
    
    for i, step in enumerate(steps, 1):
        op = step.get("op")
        params = step.get("params", {})
        
        try:
            current_img = _execute_step(current_img, op, params)
        except ValueError as e:
            return {"error": str(e)}
            
        # Naming: 01_median.png
        step_name = f"{i:02d}_{op}.png"
        step_path = os.path.join(flow_dir, step_name)
        cv2.imwrite(step_path, current_img)
        
        # Report
        step_rep = processing.generate_evaluation_plot(current_img, title=f"Step {i}: {op}")
        if step_rep is not None:
             cv2.imwrite(os.path.join(flow_dir, f"{i:02d}_{op}_REPORT.png"), step_rep)
             
        artifacts.append(step_path)
            
    return {
        "flow_dir": flow_dir,
        "final_image": artifacts[-1],
        "all_artifacts": artifacts
    }

def process_batch(directory: str, pipeline_json: str) -> list[str]:
    """
    Applies a defined PIPELINE to all images in a directory.
    """
    from .io import list_images
    
    images = list_images(directory)
    results = []
    
    try:
        _ = json.loads(pipeline_json)
    except:
        return ["Error: Invalid Pipeline JSON"]

    for img_path in images:
        try:
            # Re-use the traceable apply_pipeline logic
            res = apply_pipeline(img_path, pipeline_json)
            if "final_image" in res:
                results.append(res["final_image"])
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
            
    return results

def run_experiment(image_path: str, candidates_json: str = None) -> dict:
    """
    Experimentally applies multiple strategies (pipelines) to an image.
    Returns comprehensive metrics for scientific analysis.
    """
    import time
    experiment_start = time.time()
    
    img = load_image(image_path)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create Experiment Directory
    exp_dir = os.path.join(BASE_OUTPUT_DIR, "Experiments", f"{base_name}_{timestamp}")
    os.makedirs(exp_dir, exist_ok=True)
    
    # Calculate original image metrics
    snr_orig = processing.calculate_snr(img)
    entropy_orig = processing.calculate_entropy(img)
    mean_orig = float(np.mean(img))
    std_orig = float(np.std(img))
    min_orig = int(np.min(img))
    max_orig = int(np.max(img))
    contrast_orig = (max_orig - min_orig) / 255.0 if max_orig != min_orig else 0
    
    # 1. Determine Candidates
    if candidates_json:
        try:
            raw_candidates = json.loads(candidates_json)
            candidates_to_run = []
            for c in raw_candidates:
                candidates_to_run.append((c["name"], c["steps"]))
        except json.JSONDecodeError:
             return {"error": "Invalid JSON in candidates definition"}
    else:
        # Standard Battery (Tema 4, 5, 6 coverage)
        candidates_to_run = [
            ("Original", [], "Baseline", "N/A"),
            ("Gamma_0.5", [{"op": "gamma", "params": {"gamma": 0.5}}], "Enhancement", "Topic 6"),
            ("CLAHE_Clip2.0", [{"op": "clahe", "params": {"clip_limit": 2.0}}], "Enhancement", "Topic 6"),
            ("CLAHE_Clip4.0", [{"op": "clahe", "params": {"clip_limit": 4.0}}], "Enhancement", "Topic 6"),
            ("Log_Transform", [{"op": "log"}], "Enhancement", "Topic 6"),
            ("Equalization", [{"op": "equalize"}], "Enhancement", "Topic 6"),
            ("Median_K3", [{"op": "median", "params": {"kernel_size": 3}}], "Restoration", "Topic 5"),
            ("Median_K5", [{"op": "median", "params": {"kernel_size": 5}}], "Restoration", "Topic 5"),
            ("Denoise_Enhance", [{"op": "median", "params": {"kernel_size": 3}}, {"op": "gamma", "params": {"gamma": 0.5}}], "Pipeline", "Topic 5+6"),
        ]
    
    experiment_results = []
    
    for candidate in candidates_to_run:
        # Support both 2-tuple (name, steps) and 4-tuple (name, steps, category, topic)
        if len(candidate) == 4:
            name, steps, category, topic = candidate
        else:
            name, steps = candidate
            category, topic = "Custom", "N/A"
        
        current_img = img.copy()
        param_desc = []
        
        try:
            for step in steps:
                op = step.get("op")
                params = step.get("params", {})
                current_img = _execute_step(current_img, op, params)
                param_desc.append(f"{op}")
                
            snr_new = processing.calculate_snr(current_img)
            ent_new = processing.calculate_entropy(current_img)
            delta_snr = snr_new - snr_orig
            
            # Additional metrics
            mean_new = float(np.mean(current_img))
            std_new = float(np.std(current_img))
            min_new = int(np.min(current_img))
            max_new = int(np.max(current_img))
            contrast_new = (max_new - min_new) / 255.0 if max_new != min_new else 0
            
            title = f"{name} ({' -> '.join(param_desc)})" if param_desc and not candidates_json else name
            
            report_img = processing.generate_evaluation_plot(current_img, title=title)
            
            safe_name = name.replace(" ", "_")
            img_filename = f"{safe_name}.png"
            report_filename = f"{safe_name}_REPORT.png"
            
            cv2.imwrite(os.path.join(exp_dir, img_filename), current_img)
            if report_img is not None:
                cv2.imwrite(os.path.join(exp_dir, report_filename), report_img)
                
            experiment_results.append({
                "strategy": name,
                "category": category,
                "syllabus_topic": topic,
                "steps": param_desc,
                "metrics": {
                    "snr_db": float(round(snr_new, 2)),
                    "delta_snr": float(round(delta_snr, 2)),
                    "entropy": float(round(ent_new, 3)),
                    "mean_brightness": float(round(mean_new, 2)),
                    "std_deviation": float(round(std_new, 2)),
                    "contrast_ratio": float(round(contrast_new, 3)),
                    "histogram_range": [min_new, max_new]
                },
                "verdict": "Recommended" if delta_snr > 5 else ("Good" if delta_snr > 2 else "Marginal"),
                "artifacts": {
                    "image": os.path.join(exp_dir, img_filename),
                    "report": os.path.join(exp_dir, report_filename)
                }
            })
            
        except Exception as e:
            print(f"Failed candidate {name}: {e}")
        
    experiment_results.sort(key=lambda x: x["metrics"]["delta_snr"], reverse=True)
    
    # Agent-friendly summary
    best = experiment_results[0] if experiment_results else None
    
    experiment_end = time.time()
    execution_time_ms = round((experiment_end - experiment_start) * 1000, 2)
    
    return {
        "experiment_id": f"{base_name}_{timestamp}",
        "experiment_dir": exp_dir,
        "image_analyzed": image_path,
        "execution_time_ms": execution_time_ms,
        "original_metrics": {
            "snr_db": float(round(snr_orig, 2)),
            "entropy": float(round(entropy_orig, 3)),
            "mean_brightness": float(round(mean_orig, 2)),
            "std_deviation": float(round(std_orig, 2)),
            "contrast_ratio": float(round(contrast_orig, 3)),
            "histogram_range": [min_orig, max_orig]
        },
        "summary": {
            "best_strategy": best["strategy"] if best else "None",
            "best_delta_snr": best["metrics"]["delta_snr"] if best else 0,
            "total_strategies_tested": len(experiment_results),
            "recommended_strategies": [r["strategy"] for r in experiment_results if r["verdict"] == "Recommended"]
        },
        "results": experiment_results
    }

def run_median_demo(image_path: str, noise_prob: float = 0.05, kernel_size: int = 3) -> dict:
    """
    Demonstrates the effectiveness of median filter for salt & pepper noise removal.
    Tema 4 (Noise) + Tema 5 (Filtering) integration.
    
    Returns paths to: original, noisy, filtered, difference images + metrics comparison.
    """
    img = load_image(image_path)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create Demo Directory
    demo_dir = os.path.join(BASE_OUTPUT_DIR, "MedianDemo", f"{base_name}_{timestamp}")
    os.makedirs(demo_dir, exist_ok=True)
    
    # Step 1: Original metrics
    snr_original = processing.calculate_snr(img)
    entropy_original = processing.calculate_entropy(img)
    
    # Step 2: Add Salt & Pepper Noise
    noisy_img = processing.add_salt_pepper_noise(img, prob=noise_prob)
    snr_noisy = processing.calculate_snr(noisy_img)
    entropy_noisy = processing.calculate_entropy(noisy_img)
    
    # Step 3: Apply Median Filter
    filtered_img = processing.apply_median_filter(noisy_img, kernel_size=kernel_size)
    snr_filtered = processing.calculate_snr(filtered_img)
    entropy_filtered = processing.calculate_entropy(filtered_img)
    
    # Step 4: Compute Difference (Noise Removed)
    diff_img = cv2.absdiff(noisy_img, filtered_img)
    
    # Save all images
    paths = {}
    for name, image in [("01_original", img), ("02_noisy", noisy_img), 
                        ("03_filtered", filtered_img), ("04_difference", diff_img)]:
        path = os.path.join(demo_dir, f"{name}.png")
        cv2.imwrite(path, image)
        paths[name] = path
        
        # Generate report for each
        report = processing.generate_evaluation_plot(image, title=name.replace("_", " ").title())
        if report is not None:
            cv2.imwrite(os.path.join(demo_dir, f"{name}_REPORT.png"), report)
    
    return {
        "demo_dir": demo_dir,
        "images": paths,
        "metrics": {
            "original": {"snr_db": float(round(snr_original, 2)), "entropy": float(round(entropy_original, 3))},
            "noisy": {"snr_db": float(round(snr_noisy, 2)), "entropy": float(round(entropy_noisy, 3))},
            "filtered": {"snr_db": float(round(snr_filtered, 2)), "entropy": float(round(entropy_filtered, 3))}
        },
        "noise_params": {"prob": noise_prob},
        "filter_params": {"kernel_size": kernel_size},
        "snr_recovery_db": float(round(snr_filtered - snr_noisy, 2))
    }
