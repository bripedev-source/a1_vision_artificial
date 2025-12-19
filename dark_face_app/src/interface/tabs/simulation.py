import gradio as gr
from ..utils import update_noise_vis, update_deg_vis, wrapper_noise, wrapper_degradation

def create_tab():
    with gr.Tab("🧪 Simulation Lab"):
        gr.Markdown("### Topic 3 (Degradation) & Topic 4 (Noise)")
        
        # Noise Section
        gr.Markdown("#### Noise Generation")
        with gr.Blocks():
            with gr.Row():
                with gr.Column():
                    n_img = gr.Image(type="filepath", label="Input")
                    n_type = gr.Dropdown(["gaussian", "salt_pepper"], value="gaussian", label="Type")
                    
                    # Controls
                    n_mean = gr.Slider(-50, 50, value=0, label="Mean", visible=True)
                    n_sigma = gr.Slider(0, 100, value=25, label="Sigma", visible=True)
                    n_prob = gr.Slider(0.01, 0.5, value=0.05, label="Probability", visible=False)

                    with gr.Accordion("Advanced JSON", open=False):
                        n_json = gr.Textbox(value="{}", label="JSON Params")
                    n_btn = gr.Button("Add Noise")
                with gr.Column():
                    n_out = gr.Image(type="filepath", label="Noisy Result")
            
            n_type.change(fn=update_noise_vis, inputs=n_type, outputs=[n_mean, n_sigma, n_prob])
            
            n_btn.click(fn=wrapper_noise, inputs=[n_img, n_type, n_json, n_mean, n_sigma, n_prob], outputs=n_out, api_name="add_noise")

        gr.Markdown("---")
        # Degradation Section
        gr.Markdown("#### Digital Degradation")
        with gr.Blocks():
            with gr.Row():
                with gr.Column():
                    d_img = gr.Image(type="filepath", label="Input")
                    d_type = gr.Dropdown(["downsampling", "quantization"], value="downsampling", label="Type")
                    
                    d_factor = gr.Slider(0.1, 0.9, value=0.5, label="Downsampling Factor", visible=True)
                    d_bits = gr.Slider(1, 8, value=4, step=1, label="Quantization Bits", visible=False)
                    
                    with gr.Accordion("Advanced JSON", open=False):
                        d_json = gr.Textbox(value="{}", label="JSON Params")
                    d_btn = gr.Button("Simulate Degradation")
                with gr.Column():
                    d_out = gr.Image(type="filepath", label="Degraded Result")
            
            d_type.change(fn=update_deg_vis, inputs=d_type, outputs=[d_factor, d_bits])

            d_btn.click(fn=wrapper_degradation, inputs=[d_img, d_type, d_json, d_factor, d_bits], outputs=d_out, api_name="simulate_degradation")
