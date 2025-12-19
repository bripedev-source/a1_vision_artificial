import gradio as gr
from ..utils import update_visibility, wrapper_transform

def create_tab():
    with gr.Tab("✨ Restoration & Enhancement"):
        gr.Markdown("### Topic 5 (Filtering) & Topic 6 (Enhancement)")
        
        with gr.Blocks():
            with gr.Row():
                with gr.Column():
                    t2_img = gr.Image(type="filepath", label="Input Image")
                    t2_op = gr.Dropdown(
                        choices=["gamma", "clahe", "equalize", "log", "median", "gaussian"], 
                        label="Operation", value="gamma"
                    )
                    # Human Controls - Initial State: Gamma visible, others hidden
                    t2_gamma = gr.Slider(0.1, 5.0, value=0.5, label="Gamma Value", visible=True)
                    t2_kernel = gr.Slider(1, 15, value=3, step=2, label="Kernel Size", visible=False)
                    t2_clip = gr.Slider(1.0, 10.0, value=2.0, label="Clip Limit", visible=False)
                    
                    # Agent Control (Hidden-ish)
                    with gr.Accordion("Advanced Agent Params (JSON)", open=False):
                        t2_json = gr.Textbox(label="Override Params JSON", value="{}", placeholder="If set, overrides sliders.")
                    
                    t2_btn = gr.Button("Apply Transformation", variant="primary")
                
                with gr.Column():
                    t2_out = gr.Image(type="filepath", label="Result Image")
            
            # Logic Wiring
            t2_op.change(
                fn=update_visibility,
                inputs=t2_op,
                outputs=[t2_gamma, t2_kernel, t2_clip]
            )

            t2_btn.click(
                fn=wrapper_transform, 
                inputs=[t2_img, t2_op, t2_json, t2_gamma, t2_kernel, t2_clip],
                outputs=t2_out,
                api_name="apply_transform" 
            )
