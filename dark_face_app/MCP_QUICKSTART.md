# MCP QuickStart Guide - Dark Face Agent

## 🚀 Fastest Setup (5 minutes)

### Step 1: Start the Server
```bash
# Local native
python mcp_interface.py

# Or with hot-reload (development)
python dev.py

# Or with uv
uv run mcp_interface.py
```

Browser opens at: `http://localhost:7861`

### Step 2: Choose Your Client

#### **Claude Desktop**
1. Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
   - Or `%APPDATA%\Claude\claude_desktop_config.json` (Windows)

2. Add:
```json
{
  "mcpServers": {
    "dark-face-agent-local": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "http://127.0.0.1:7861/gradio_api/mcp/"]
    }
  }
}
```

3. **Restart Claude Desktop**
4. Look for 🔨 tool icon in bottom-right
5. Click to see available tools

#### **Cursor IDE**
1. Edit `~/.cursor/mcp.json`
2. Add same `mcpServers` config above
3. Restart Cursor
4. Chat with agent directly

#### **Windsurf**
1. Edit `~/.codeium/windsurf/mcp_config.json`
2. Add same `mcpServers` config
3. Restart Windsurf

#### **VS Code + GitHub Copilot**
⚠️ Different format! Uses direct HTTP (no mcp-remote wrapper)

1. Create/edit `.vscode/mcp.json`:
```json
{
  "servers": {
    "gradio-api-remote": {
      "url": "http://localhost:7861/gradio_api/mcp/",
      "type": "http"
    }
  },
  "inputs": []
}
```

2. Restart VS Code
3. Use Copilot chat as normal

---

## 🔴 Special: Google Colab Setup

### When Running in Colab

```python
# In a cell:
!python mcp_interface.py
```

Gradio auto-generates: `https://XXXXXXXX.gradio.live/`

### In VS Code (Remote to Colab)

Replace `http://localhost:7861/...` with the Colab share URL:

```json
{
  "servers": {
    "gradio-api-colab": {
      "url": "https://9797ddffb4c22ffcb7.gradio.live/gradio_api/mcp/",
      "type": "http"
    }
  },
  "inputs": []
}
```

---

## 🐳 Docker Setup (Advanced)

### From Host Machine
Use `host.docker.internal` instead of `localhost`:

```json
{
  "mcpServers": {
    "dark-face-docker": {
      "command": "npx",
      "args": [
        "-y", "mcp-remote@latest",
        "http://host.docker.internal:7861/gradio_api/mcp/",
        "--allow-http"
      ]
    }
  }
}
```

### From Inside Docker
```json
"args": [
  "-y", "mcp-remote@latest",
  "http://dark-face-app:7861/gradio_api/mcp/"
]
```
(Replace `dark-face-app` with your container name in docker-compose.yml)

---

## 🔍 Testing Connection

### Option 1: Browser Check
Open `http://localhost:7861/gradio_api/mcp/` in browser
- Should return JSON with tools list
- Status code: 200 ✅

### Option 2: Using mcp-remote Directly
```bash
npx mcp-remote-client http://127.0.0.1:7861/gradio_api/mcp/ --debug
```

This will:
- List all available tools
- Test connection
- Show detailed logs

### Option 3: Check Claude Desktop Logs
- **macOS/Linux:** `tail -f ~/Library/Logs/Claude/mcp*.log`
- **Windows (PowerShell):** `Get-Content "C:\Users\YourUsername\AppData\Local\Claude\Logs\mcp.log" -Wait -Tail 20`

---

## ⚡ Available Tools in MCP

Once connected, these tools become available:

### Restoration & Enhancement
- `apply_gamma` - Adjust brightness
- `apply_clahe` - Adaptive contrast enhancement
- `apply_median_filter` - Remove salt&pepper noise
- `apply_gaussian_filter` - General noise reduction
- `apply_log_transform` - Expand dark areas

### Simulation
- `add_gaussian_noise` - Add thermal noise
- `add_salt_pepper_noise` - Add impulsive noise
- `simulate_downsampling` - Simulate resolution loss
- `simulate_quantization` - Simulate bit-depth reduction

### Analysis & Pipelines
- `run_experiment` - Test multiple enhancement strategies
- `apply_pipeline` - Chain operations for full traceback
- `process_batch` - Apply pipeline to directory of images
- `run_median_demo` - Demonstrate noise removal

### Arithmetic
- `apply_arithmetic_ops` - Pixel-wise operations (add, sub, mult, div)

---

## 📋 Checklist Before Asking for Help

- [ ] Server running at `http://localhost:7861`?
- [ ] Port 7861 not blocked by firewall?
- [ ] MCP config file in correct location?
- [ ] JSON syntax valid (no trailing commas)?
- [ ] Client restarted after config change?
- [ ] Share link not expired (if using Colab)?
- [ ] Correct endpoint: `/gradio_api/mcp/` (not `/mcp/`)?

---

## 🆘 Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `Connection refused` | Start server: `python mcp_interface.py` |
| `404 Not Found` | Check URL ends with `/gradio_api/mcp/` |
| `ECONNREFUSED 127.0.0.1:7861` | Server not running, or port is wrong |
| `mcp-remote: command not found` | Install Node.js first, then: `npm install -g mcp-remote` |
| Tools don't appear in Claude | Restart Claude, check `.log` files |
| `HTTP 403 Forbidden` | Auth issue - use `--header` if needed |
| Docker `Connection reset` | Use `host.docker.internal`, add `--allow-http` |
| Colab + Copilot no work | Copilot doesn't support mcp-remote tunneling in notebooks |

---

## 📚 Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│          MCP Client (Claude, Cursor, etc)               │
└────────────────────┬─────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        v                         v
   STDIO-based            HTTP-based clients
   (npx mcp-remote)       (VS Code Copilot)
        │                         │
        v                         v
┌───────────────────────────────────────────────────────────┐
│ Gradio MCP Server (gradio 5.x + mcp support)           │
│  ├─ /gradio_api/mcp/ (HTTP endpoint)                    │
│  ├─ tools/list (list available functions)               │
│  └─ tools/call (execute functions)                      │
└───────────────┬────────────────────────────────────────┘
                │
        ┌───────┴────────┐
        │                │
        v                v
┌─────────────────┐ ┌──────────────────┐
│ OpenCV Engine   │ │ NumPy Compute    │
│ (processing.py) │ │ (src/agent_api/) │
└─────────────────┘ └──────────────────┘
        │                │
        └────────┬───────┘
                 v
        Image outputs (PNG)
        Metrics (JSON)
```

---

## 🎯 What's Next?

- Review [Help tab](http://localhost:7861) in the UI
- Check [`README.md`](./README.md) for full documentation
- Explore [`src/agent_api/`](./src/agent_api/) for implementation details
- Read MCP spec: https://modelcontextprotocol.io/

**Happy processing!** 🚀
