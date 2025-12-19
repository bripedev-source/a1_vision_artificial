import gradio as gr
from ... import agent_api

# Pipeline Presets
PIPELINE_PRESETS = {
    "Ninguno (Manual)": "[]",
    "Denoise + Enhance (Gamma)": '[{"op": "median", "params": {"kernel_size": 3}}, {"op": "gamma", "params": {"gamma": 0.5}}]',
    "Low Light Recovery (CLAHE)": '[{"op": "clahe", "params": {"clip_limit": 3.0}}, {"op": "gamma", "params": {"gamma": 0.7}}]',
    "Aggressive Enhancement (Log + Equalize)": '[{"op": "log"}, {"op": "equalize"}]',
    "Noise Reduction Only (Median K5)": '[{"op": "median", "params": {"kernel_size": 5}}]'
}

def create_tab():
    with gr.Tab("⚙️ Pipelines & Batch"):
        gr.Markdown("## 🔗 Pipeline de Transformaciones")
        gr.Markdown("Aplica una secuencia de operaciones con trazabilidad completa.")
        
        with gr.Row():
            with gr.Column(scale=1):
                pipe_img = gr.Image(type="filepath", label="Imagen de Entrada")
                pipe_preset = gr.Dropdown(
                    choices=list(PIPELINE_PRESETS.keys()),
                    value="Ninguno (Manual)",
                    label="Preset de Pipeline"
                )
                pipe_json = gr.Textbox(
                    label="Steps JSON", 
                    placeholder='[{"op": "gamma", "params": {"gamma": 0.5}}, {"op": "median", "params": {"kernel_size": 3}}]',
                    lines=3
                )
                pipe_btn = gr.Button("▶️ Ejecutar Pipeline", variant="primary")
            
            with gr.Column(scale=1):
                pipe_out_img = gr.Image(type="filepath", label="Resultado Final")
                pipe_out_json = gr.JSON(label="Artefactos Generados")
        
        def update_json_from_preset(preset_name):
            return PIPELINE_PRESETS.get(preset_name, "[]")
        
        def run_pipeline_visual(img_path, steps_json):
            result = agent_api.apply_pipeline(img_path, steps_json)
            if "error" in result:
                return None, result
            return result.get("final_image"), result
        
        pipe_preset.change(fn=update_json_from_preset, inputs=pipe_preset, outputs=pipe_json)
        pipe_btn.click(
            fn=run_pipeline_visual,
            inputs=[pipe_img, pipe_json],
            outputs=[pipe_out_img, pipe_out_json],
            api_name="apply_pipeline"
        )
        
        gr.Markdown("---")
        gr.Markdown("## 📦 Procesamiento por Lotes")
        gr.Markdown("Aplica un pipeline a todas las imágenes de un directorio.")
        
        with gr.Row():
            with gr.Column():
                batch_dir = gr.Textbox(label="Directorio de Entrada", placeholder="/ruta/a/imagenes")
                batch_json = gr.Textbox(
                    label="Pipeline JSON", 
                    placeholder='[{"op": "gamma", "params": {"gamma": 0.5}}]',
                    lines=2
                )
                batch_btn = gr.Button("▶️ Procesar Lote", variant="primary")
            with gr.Column():
                batch_out = gr.JSON(label="Resultados del Lote")
        
        batch_btn.click(
            fn=agent_api.process_batch,
            inputs=[batch_dir, batch_json],
            outputs=batch_out,
            api_name="process_batch"
        )
