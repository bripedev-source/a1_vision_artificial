
import json
import gradio as gr
from .. import agent_api

# --- 1. VISIBILITY LOGIC ---

def update_visibility(op):
    """
    Updates slider visibility based on selected operation.
    """
    show_gamma = (op == "gamma")
    show_kernel = (op in ["median", "gaussian"])
    show_clip = (op == "clahe")
    
    return (
        gr.update(visible=show_gamma), 
        gr.update(visible=show_kernel),
        gr.update(visible=show_clip)
    )

def update_noise_vis(type):
    """
    Updates slider visibility for Noise Sim.
    """
    is_gaussian = (type == "gaussian")
    # Gaussian: Mean/Sigma. Salt&Pepper: Prob only.
    return (
        gr.update(visible=is_gaussian),
        gr.update(visible=is_gaussian),
        gr.update(visible=not is_gaussian) # Prob slider
    )

def update_deg_vis(type):
    """
    Updates slider visibility for Degradation Sim.
    """
    is_down = (type == "downsampling")
    return (
        gr.update(visible=is_down),
        gr.update(visible=not is_down)
    )

# --- 2. METRICS PROCESSOR ---

def format_metrics_table(json_data):
    """
    Converts raw metrics JSON into a readable Markdown table.
    """
    if not json_data or "error" in json_data:
        return "## Error analyzing metrics"
    
    md = "| Metric | Value | Description |\n| :--- | :--- | :--- |\n"
    md += f"| **SNR** | **{json_data.get('snr_db', 'N/A')} dB** | {json_data.get('verdict', '')} |\n"
    md += f"| Entropy | {json_data.get('entropy', 'N/A')} | Information Content |\n"
    md += f"| Dynamic Range % | {json_data.get('dynamic_range_usage_pct', 'N/A')}% | Histogram Usage |\n"
    md += f"| Dark Pixels % | {json_data.get('dark_pixels_pct', 'N/A')}% | Underexposure |\n"
    
    return md

# --- 3. EXECUTION WRAPPERS (Hybrid Logic) ---

def wrapper_transform(img, op, json_params, gamma, kernel, clip):
    """Hybrid wrapper: uses JSON if active, else uses sliders."""
    p = {}
    # Try parsing JSON first
    if json_params and json_params.strip() != "{}":
            try: p = json.loads(json_params)
            except: pass
    
    # Fallback to sliders if JSON is empty/invalid
    if not p:
        if op == "gamma": p = {"gamma": gamma}
        elif op in ["median", "gaussian"]: p = {"kernel_size": int(kernel)}
        elif op == "clahe": p = {"clip_limit": clip}
    
    return agent_api.apply_transformation(img, op, json.dumps(p))

def wrapper_noise(img, type, json_params, mean, sigma, prob):
    p = {}
    if json_params and json_params.strip() != "{}":
            try: p = json.loads(json_params)
            except: pass
    if not p:
        if type == "gaussian": p = {"mean": mean, "sigma": sigma}
        elif type == "salt_pepper": p = {"prob": prob}
    return agent_api.add_noise(img, type, json.dumps(p))

def wrapper_degradation(img, type, json_params, factor, bits):
    p = {}
    if json_params and json_params.strip() != "{}":
            try: p = json.loads(json_params)
            except: pass
    if not p:
        if type == "downsampling": p = {"factor": factor}
        if type == "quantization": p = {"bits": int(bits)}
    return agent_api.simulate_degradation(img, type, json.dumps(p))

def wrapper_analyze(img):
    data = agent_api.analyze_image_metrics(img)
    return format_metrics_table(data)

def format_median_demo_result(result):
    """
    Formats the run_median_demo result into a readable Markdown table.
    """
    m = result["metrics"]
    recovery = result["snr_recovery_db"]
    
    md = "### 📊 Comparación de Métricas (SNR)\n\n"
    md += "| Etapa | SNR (dB) | Entropía | Δ vs Original |\n"
    md += "| :--- | :---: | :---: | :---: |\n"
    md += f"| **Original** | {m['original']['snr_db']} | {m['original']['entropy']} | — |\n"
    md += f"| **Con Ruido** | {m['noisy']['snr_db']} | {m['noisy']['entropy']} | {m['noisy']['snr_db'] - m['original']['snr_db']:.2f} dB |\n"
    md += f"| **Filtrada (Mediana)** | {m['filtered']['snr_db']} | {m['filtered']['entropy']} | {m['filtered']['snr_db'] - m['original']['snr_db']:.2f} dB |\n"
    md += f"\n**Recuperación de SNR por filtro:** `+{recovery} dB`\n"
    md += f"\n*Parámetros: Ruido prob={result['noise_params']['prob']}, Kernel={result['filter_params']['kernel_size']}*"
    
    return md

def format_experiment_result(result):
    """
    Formats run_experiment result into a human-readable Markdown summary.
    For collaborative entities (humans and agents).
    """
    if "error" in result:
        return f"## ❌ Error\n{result['error']}"
    
    summary = result.get("summary", {})
    results = result.get("results", [])
    
    md = f"## 🔬 Experiment: `{result.get('experiment_id', 'N/A')}`\n\n"
    md += f"**Original SNR:** `{result.get('original_snr_db', 'N/A')} dB`\n\n"
    md += f"### 🏆 Best Strategy: `{summary.get('best_strategy', 'N/A')}` (+{summary.get('best_delta_snr', 0)} dB)\n\n"
    
    if summary.get("recommended_strategies"):
        md += f"**Recommended:** {', '.join(summary['recommended_strategies'])}\n\n"
    
    md += "### 📊 Results Ranking\n\n"
    md += "| # | Strategy | Category | ΔSNR | Verdict |\n"
    md += "| :---: | :--- | :--- | :---: | :---: |\n"
    
    for i, r in enumerate(results, 1):
        emoji = "🥇" if i == 1 else ("🥈" if i == 2 else ("🥉" if i == 3 else ""))
        verdict_emoji = "✅" if r["verdict"] == "Recommended" else ("👍" if r["verdict"] == "Good" else "⚠️")
        md += f"| {emoji}{i} | **{r['strategy']}** | {r['category']} | +{r['metrics']['delta_snr']} dB | {verdict_emoji} {r['verdict']} |\n"
    
    md += f"\n*{len(results)} strategies tested. Artifacts saved to: `{result.get('experiment_dir', 'N/A')}`*"
    
    return md
