import os
import gradio as gr
from src.interface import build_mcp_interface

if __name__ == "__main__":
    import sys
    
    # 1. Environment Detection
    is_colab = "google.colab" in sys.modules
    is_docker = os.path.exists("/.dockerenv")
    
    env_name = "Google Colab" if is_colab else ("Docker" if is_docker else "Local/Native")
    
    print(f"🤖 Dark Face MCP Agent v2.0")
    print(f"🌍 Environment: {env_name}")
    print(f"📂 Modular Backend: Active")
    
    # 2. Config Checks
    if not os.path.exists("src"):
        print("⚠️ Warning: 'src' directory not found! Check working directory.")

    # 3. Launch Logic
    demo = build_mcp_interface()
    
    # Defaults
    server_name = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0" if is_docker else "127.0.0.1")
    server_port = int(os.getenv("GRADIO_SERVER_PORT", 7861))
    
    # Colab specific override
    share_link = False
    if is_colab or is_docker:
        print("🚀 Colab/Docker detected: Enabling Public Share Link (required for external access to MCP)")
        share_link = True
        
    print(f"🔌 Starting Server on {server_name}:{server_port} (Share={share_link})...")
    
    demo.launch(
        server_name=server_name, 
        server_port=server_port, 
        mcp_server=True, 
        show_error=True, 
        share=share_link
    )
