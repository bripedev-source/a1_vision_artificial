import gradio as gr
from ... import agent_api

def create_tab():
    with gr.Tab("🧠 Meta-Cognitive"):
        gr.Markdown("### Self-Inspection & Configuration")
        gr.Interface(
            fn=agent_api.get_capabilities,
            inputs=[],
            outputs=gr.JSON(label="Agent Capabilities Schema"),
            api_name="get_capabilities",
            description="Returns the agent's capabilities."
        )
        gr.Interface(
            fn=agent_api.configure_agent,
            inputs=gr.Textbox(label="Config JSON", value='{"base_output_dir": "output"}'),
            outputs=gr.JSON(label="Status"),
            api_name="configure_agent",
            description="Updates runtime configuration."
        )
