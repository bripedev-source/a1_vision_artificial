import gradio as gr
from ... import agent_api
from ..utils import wrapper_analyze, format_median_demo_result

def create_tab():
    with gr.Tab("🔬 Diagnosis & Experiments"):
        gr.Markdown("## 📊 Metric Analysis")
        
        with gr.Row():
            with gr.Column(scale=1):
                diag_img = gr.Image(type="filepath", label="Input Image")
                diag_btn = gr.Button("📈 Analyze Metrics", variant="primary")
            with gr.Column(scale=1):
                diag_out = gr.Markdown(label="Metrics Report")
        
        diag_btn.click(fn=wrapper_analyze, inputs=diag_img, outputs=diag_out, api_name="analyze_image")
        
        gr.Markdown("---")
        gr.Markdown("## 🧪 Demo: Efectividad del Filtro de Mediana (Tema 4 & 5)")
        gr.Markdown("""
**Flujo del experimento:**
1. 📷 Se parte de la **imagen original**
2. ➕🔊 Se **añade ruido impulsivo** (sal y pimienta) a la imagen original
3. 🔧 Se **aplica el filtro de mediana** sobre la imagen con ruido
4. 📊 Se compara el resultado para verificar la efectividad del filtro
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                demo_img = gr.Image(type="filepath", label="Imagen de Entrada (Original)")
                with gr.Row():
                    demo_noise = gr.Slider(0.01, 0.2, value=0.05, step=0.01, label="Prob. Ruido S&P")
                    demo_kernel = gr.Slider(3, 9, value=3, step=2, label="Kernel Mediana")
                demo_btn = gr.Button("▶️ Ejecutar Demo", variant="primary")
            
            with gr.Column(scale=2):
                gr.Markdown("### Resultados del Experimento")
                with gr.Row():
                    demo_original = gr.Image(label="1️⃣ Original", type="filepath")
                    demo_noisy = gr.Image(label="2️⃣ Original + Ruido S&P", type="filepath")
                with gr.Row():
                    demo_filtered = gr.Image(label="3️⃣ Mediana(Ruidosa)", type="filepath")
                    demo_diff = gr.Image(label="4️⃣ Ruido Eliminado", type="filepath")
                    
        demo_metrics = gr.Markdown(label="Comparación de Métricas")
        
        def run_demo_wrapper(img_path, noise_prob, kernel_size):
            result = agent_api.run_median_demo(img_path, noise_prob=noise_prob, kernel_size=int(kernel_size))
            return (
                result["images"]["01_original"],
                result["images"]["02_noisy"],
                result["images"]["03_filtered"],
                result["images"]["04_difference"],
                format_median_demo_result(result)
            )
        
        demo_btn.click(
            fn=run_demo_wrapper,
            inputs=[demo_img, demo_noise, demo_kernel],
            outputs=[demo_original, demo_noisy, demo_filtered, demo_diff, demo_metrics],
            api_name="run_median_demo"
        )
        
        gr.Markdown("---")
        gr.Markdown("## 🔬 Multi-Strategy Experimentation")
        gr.Markdown("Compara automáticamente múltiples técnicas de mejora sobre una imagen.")
        
        with gr.Row():
            with gr.Column(scale=1):
                exp_img = gr.Image(type="filepath", label="Imagen de Entrada")
                exp_custom = gr.Textbox(
                    label="Candidates JSON (Opcional)", 
                    placeholder='[{"name": "CustomGamma", "steps": [{"op": "gamma", "params": {"gamma": 0.4}}]}]',
                    lines=2
                )
                exp_btn = gr.Button("🚀 Ejecutar Experimento", variant="primary")
            with gr.Column(scale=2):
                exp_out_md = gr.Markdown(label="Resultados")
        
        gr.Markdown("### 🖼️ Galería de Resultados")
        exp_gallery = gr.Gallery(
            label="Imágenes Procesadas",
            columns=4,
            rows=2,
            height="auto",
            object_fit="contain"
        )
        
        with gr.Accordion("📋 JSON Completo (para Agentes)", open=False):
            exp_out_json = gr.JSON(label="Raw JSON")
        
        def run_experiment_visual(img_path, custom_json):
            from ..utils import format_experiment_result
            result = agent_api.run_experiment(img_path, custom_json if custom_json.strip() else None)
            
            # Build gallery from REPORT images (include histogram)
            gallery_images = []
            for r in result.get("results", []):
                report_path = r.get("artifacts", {}).get("report")
                if report_path:
                    gallery_images.append((report_path, r["strategy"]))
            
            return format_experiment_result(result), gallery_images, result
        
        exp_btn.click(
            fn=run_experiment_visual,
            inputs=[exp_img, exp_custom],
            outputs=[exp_out_md, exp_gallery, exp_out_json],
            api_name="run_experiment"
        )
