
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
        gr.Markdown("### 🔗 Connectivity Information & MCP Configuration")
        
        is_colab = "google.colab" in os.sys.modules
        is_docker = os.path.exists("/.dockerenv")
        
        env_type = "Google Colab" if is_colab else ("Docker Container" if is_docker else "Local/Native")
        local_ip = get_local_ip()
        
        gr.Markdown(f"""
        **Current Environment:** `{env_type}`
        **Local IP:** `{local_ip}`
        **MCP Server Port:** `7861` (Default)
        """)
        
        gr.Markdown("### 🤖 MCP Connection Methods by Client & Environment")
        
        if is_colab:
            gr.Markdown("#### 🔴 Google Colab Detected")
            gr.Markdown("""
            **✅ Share Link Mode (Automatic)**
            - Gradio automatically enables public share links in Colab
            - URL format: `https://XXXXXXXX.gradio.live/gradio_api/mcp/`
            
            **Best for Colab:** Use the public share link with HTTP-based MCP clients
            """)
        
        if is_docker:
            gr.Markdown("#### 🐳 Docker Container Detected")
            gr.Markdown("""
            ⚠️ **Known Limitations:**
            - Docker containers cannot directly access `gradio.live` share links (network isolation)
            - Must use explicit external URLs with `--allow-http` flag in mcp-remote
            - Requires proper port mapping and network configuration
            
            **Solution:** Use `localhost:7861` from host machine, or expose via reverse proxy
            """)
        else:
            gr.Markdown("#### 💻 Local/Native Environment Detected")
            gr.Markdown("""
            **✅ Best Option:** Direct localhost connection
            - URL: `http://localhost:7861/gradio_api/mcp/`
            - Lowest latency and most reliable
            """)
        
        gr.Markdown("---")
        gr.Markdown("### 1️⃣ Claude Desktop (macOS/Windows)")
        gr.Code(language="json", label="~/.claude_desktop_config.json", value="""
{
  "mcpServers": {
    "dark-face-agent-local": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "http://127.0.0.1:7861/gradio_api/mcp/"
      ]
    }
  }
}
""")
        
        gr.Markdown("### 2️⃣ VS Code + GitHub Copilot (Windows)")
        gr.Code(language="json", label=".vscode/mcp.json", value="""
{
  "servers": {
    "gradio-api-remote": {
      "url": "https://GRADIO_SHARE_URL/gradio_api/mcp/",
      "type": "http"
    }
  },
  "inputs": []
}
""")
        gr.Markdown("**Note:** Replace `GRADIO_SHARE_URL` with your actual share link from Colab")
        
        gr.Markdown("### 3️⃣ Cursor IDE")
        gr.Code(language="json", label="~/.cursor/mcp.json (v0.48.0+)", value="""
{
  "mcpServers": {
    "dark-face-agent": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "http://127.0.0.1:7861/gradio_api/mcp/"
      ]
    }
  }
}
""")
        
        gr.Markdown("### 4️⃣ Windsurf")
        gr.Code(language="json", label="~/.codeium/windsurf/mcp_config.json", value="""
{
  "mcpServers": {
    "dark-face-agent": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "http://127.0.0.1:7861/gradio_api/mcp/"
      ]
    }
  }
}
""")
        
        gr.Markdown("---")
        gr.Markdown("### 🚀 Quick Reference Table")
        gr.Markdown("""
        | Environment | Best Connection | Config Type | Notes |
        |-------------|-----------------|-------------|-------|
        | **Local (Native)** | `localhost:7861` | STDIO (npx mcp-remote) | Fastest, no network overhead |
        | **Google Colab** | `gradio.live` share link | HTTP direct | Auto-generated, expires in 7 days |
        | **Docker** | Host port mapping + mcp-remote | HTTP + --allow-http | Requires proper network setup |
        | **VS Code Copilot** | HTTPS share link | HTTP direct | No npx wrapper needed |
        
        ### 🔧 Environment Variables (Optional)
        - `GRADIO_SERVER_NAME`: Override server address (default: `127.0.0.1` locally, `0.0.0.0` in Docker)
        - `GRADIO_SERVER_PORT`: Override server port (default: `7861`)
        
        ### 📚 About mcp-remote
        `mcp-remote` is an NPM bridge that converts HTTP/SSE servers into stdio-compatible MCP clients.
        - Supports OAuth for authorized servers
        - Transport strategies: `http-first`, `sse-first`, `http-only`, `sse-only`
        - Custom headers for authentication
        
        ### 📓 Notebook Integration
        To use this agent programmatically from a Jupyter Notebook:
        1. Ensure the server is running
        2. Import: `from src.agent_api import workflows`
        3. Or use the Python/JS Gradio client to query the API
        """)
