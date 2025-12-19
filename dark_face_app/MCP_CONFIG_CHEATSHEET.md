# 🎯 MCP Connectivity - Quick Reference Card

## 1. VS Code + GitHub Copilot (Windows) 📝
```json
// .vscode/mcp.json
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
✅ Works locally  
✅ Works with Colab share URLs  
⚠️ Different format than Claude Desktop

---

## 2. Claude Desktop (All Platforms) 🤖
```json
// macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
// Windows: %APPDATA%\Claude\claude_desktop_config.json
{
  "mcpServers": {
    "dark-face-agent": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "http://127.0.0.1:7861/gradio_api/mcp/"]
    }
  }
}
```
✅ Local setup (best latency)  
✅ Works with Colab share URLs  
✅ Production-ready

---

## 3. Cursor IDE 📦
```json
// ~/.cursor/mcp.json
{
  "mcpServers": {
    "dark-face-agent": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "http://127.0.0.1:7861/gradio_api/mcp/"]
    }
  }
}
```
Same as Claude Desktop

---

## 4. Windsurf ⚙️
```json
// ~/.codeium/windsurf/mcp_config.json
{
  "mcpServers": {
    "dark-face-agent": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "http://127.0.0.1:7861/gradio_api/mcp/"]
    }
  }
}
```
Same as Claude Desktop

---

## 5. Google Colab + VS Code (Remote) 🔴
1. In Colab: `python mcp_interface.py`
2. Copy share URL: `https://XXXXXXXX.gradio.live/`
3. In `.vscode/mcp.json`:
```json
{
  "servers": {
    "gradio-api-colab": {
      "url": "https://XXXXXXXX.gradio.live/gradio_api/mcp/",
      "type": "http"
    }
  },
  "inputs": []
}
```
✅ Works great  
⚠️ Expires in 7 days  
⚠️ Requires public access

---

## 6. Docker (macOS/Windows) 🐳
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
✅ Works on macOS & Windows  
❌ Doesn't work on Linux  
⚠️ Requires `--allow-http` flag

---

## Key Discovery: What Works vs What Doesn't

| Setup | Local | Colab | Docker |
|-------|-------|-------|--------|
| **Claude Desktop** | ✅ | ✅ (share URL) | ⚠️ (host.docker.internal) |
| **VS Code Copilot** | ✅ | ✅ | ❌ |
| **Cursor** | ✅ | ✅ (mcp-remote) | ⚠️ |
| **Gradio Share Link** | N/A | ✅ | ❌ (isolated) |
| **Performance** | ⭐⭐⭐ | ⭐⭐ | ⭐ |

---

## Why Docker Doesn't Work "Out of the Box"

Docker containers run in isolated network namespaces:
- ❌ `localhost:7861` on host ≠ `localhost:7861` in container
- ❌ Container can't reach `gradio.live` (external URLs blocked)
- ✅ `host.docker.internal` bridges the gap (Docker Desktop only)

---

## Quick Troubleshooting

```bash
# Test if server is running
curl http://localhost:7861/gradio_api/mcp/

# Test with mcp-remote directly
npx mcp-remote-client http://127.0.0.1:7861/gradio_api/mcp/ --debug

# Check Claude logs (macOS/Linux)
tail -f ~/Library/Logs/Claude/mcp*.log

# Kill zombie process on port 7861
lsof -i :7861 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

---

## Summary

| Format | Clients | Best For |
|--------|---------|----------|
| **STDIO + mcp-remote** | Claude, Cursor, Windsurf | Local development |
| **HTTP direct** | VS Code Copilot | Remote/Colab |
| **Gradio Share Link** | Any HTTP client | Quick sharing (7 days) |

**Golden Rule:** Use the right config format for your client, or debugging will be painful!
