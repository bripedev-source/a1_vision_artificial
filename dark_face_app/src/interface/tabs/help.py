
import gradio as gr
import os
import socket

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def create_tab():
    with gr.Tab("ℹ️ Help & Connectivity"):
        gr.Markdown("### 🔗 Connectivity Information")
        
        is_colab = "google.colab" in os.sys.modules
        is_docker = os.path.exists("/.dockerenv")
        
        env_type = "Google Colab" if is_colab else ("Docker Container" if is_docker else "Local/Native")
        local_ip = get_local_ip()
        
        gr.Markdown(f"""
        **Current Environment:** `{env_type}`
        **Local IP:** `{local_ip}`
        **MCP Server Port:** `7861` (Default)
        """)
        
        gr.Markdown("### 🤖 How to Connect (MCP)")
        gr.Code(language="json", label="MCP Client Configuration (Claude Desktop / Other)", value=f"""
{{
  "mcpServers": {{
    "dark-face-agent": {{
      "command": "python",
      "args": ["path/to/mcp_interface.py"],
      "env": {{ "GRADIO_SERVER_NAME": "0.0.0.0" }}
    }}
  }}
}}
""")

        gr.Markdown("### 📓 Notebook Integration")
        gr.Markdown("""
        To use this agent programmatically from a Jupyter Notebook:
        1. Ensure the server is running.
        2. Use `src.agent_api` directly if in the same environment.
        3. Or use an MCP Client to connect remotely.
        """)
