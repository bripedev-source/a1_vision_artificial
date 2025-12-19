import gradio as gr
from ... import agent_api

def create_tab():
    with gr.Tab("➕ Arithmetic Lab"):
        gr.Markdown("### Topic 6: Arithmetic Operations")
        
        with gr.Blocks():
            with gr.Row():
                a_img1 = gr.Image(type="filepath", label="Image 1")
                a_img2 = gr.Image(type="filepath", label="Image 2")
            
            with gr.Row():
                a_op = gr.Dropdown(choices=["add", "subtract", "multiply", "divide"], label="Operation", value="add")
                a_btn = gr.Button("Execute Arithmetic", variant="primary")
            
            a_out = gr.Image(type="filepath", label="Result")
            
            a_btn.click(fn=agent_api.apply_arithmetic, inputs=[a_img1, a_img2, a_op], outputs=a_out, api_name="apply_arithmetic")
        
        gr.Markdown("#### Utilities")
        with gr.Row():
            gr.Interface(
                fn=agent_api.compute_difference,
                inputs=[gr.Image(type="filepath", label="Image 1"), gr.Image(type="filepath", label="Image 2")],
                outputs=gr.Image(type="filepath", label="Diff Output"),
                api_name="compute_difference"
            )
            gr.Interface(
                fn=agent_api.compute_average,
                inputs=gr.Textbox(label="Directory"), # Directory hard to visualize
                outputs=gr.Image(type="filepath", label="Avg Output"),
                api_name="compute_average"
            )
