
import gradio as gr
from .tabs import meta, restoration, simulation, arithmetic, diagnosis, pipelines, help

def build_mcp_interface():
    """
    Builds the modular Gradio interface.
    Aggregates all tabs from the sub-modules.
    """
    with gr.Blocks(title="Dark Face Agent API") as demo:
        gr.Markdown("""
        # 🤖 Dark Face Agent API
        **Scientific Collaborative Interface**
        
        This interface exposes the agent's capabilities divided by Syllabus Topics and Functional Areas.
        Designed for seamless integration with collaborative entities (MCP Clients, Agents) and human researchers.
        """)
        
        with gr.Tabs():
            meta.create_tab()
            help.create_tab()
            restoration.create_tab()
            simulation.create_tab()
            arithmetic.create_tab()
            diagnosis.create_tab()
            pipelines.create_tab()
            
    return demo
