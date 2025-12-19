# Docker & MCP: Known Limitations & Solutions

## 🐳 Problem Summary

**Docker containers have network isolation** that prevents them from accessing external resources like Gradio's public share links (`gradio.live`). This creates challenges when trying to connect MCP clients from the host machine to a Gradioserver running in Docker.

---

## ❌ What DOESN'T Work

### 1. Gradio Share Links Inside Docker → Host MCP Client
```dockerfile
# ❌ FAILS
FROM python:3.10
RUN pip install gradio opencv-python
CMD ["python", "-c", "import gradio as gr; gr.Interface(fn=lambda x: x, inputs='text', outputs='text').launch(share=True)"]
```

**Why:** Docker container cannot reach `gradio.live` servers (firewall/network isolation).
Share link only works if client is also inside the container.

### 2. Localhost:7861 Inside Container → Host Client
```json
// ❌ FAILS
{
  "command": "npx",
  "args": ["-y", "mcp-remote@latest", "http://localhost:7861/gradio_api/mcp/"]
}
```

**Why:** `localhost` from host machine = `127.0.0.1` on host's loopback device, not the container's.
Container's localhost is different from host's localhost.

---

## ✅ What WORKS

### Solution 1: `host.docker.internal` (Recommended for Local Dev)

**From the host machine:**
```json
{
  "mcpServers": {
    "dark-face-docker": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "http://host.docker.internal:7861/gradio_api/mcp/",
        "--allow-http"
      ]
    }
  }
}
```

**Prerequisites:**
- ✅ Docker running on macOS or Windows (Docker Desktop)
- ✅ Container port 7861 exposed in `docker-compose.yml`:
  ```yaml
  services:
    dark-face-app:
      ports:
        - "7861:7861"  # Map container:7861 to host:7861
  ```
- ✅ `--allow-http` flag (trusts local network)

**Limitations:**
- ❌ Doesn't work on Linux (Docker on Linux doesn't have `host.docker.internal`)
- ❌ Requires explicit port mapping

---

### Solution 2: Container Hostname (For Service-to-Service Communication)

**From another container in the same `docker-compose.yml`:**
```json
{
  "mcpServers": {
    "dark-face-docker": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "http://dark-face-app:7861/gradio_api/mcp/"
      ]
    }
  }
}
```

**Prerequisites:**
- ✅ Both containers in same Docker network
- ✅ Container name matches service name in `docker-compose.yml`:
  ```yaml
  services:
    dark-face-app:  # ← Use this name
      image: dark-face:latest
      ports:
        - "7861:7861"
  ```

**Note:** Use `http://` (not `https://`) within private Docker networks.

---

### Solution 3: Linux + Docker: IP Address of Container

**Find container IP:**
```bash
docker inspect dark-face-app --format='{{.NetworkSettings.IPAddress}}'
# Returns: 172.18.0.2
```

**Use in config:**
```json
{
  "command": "npx",
  "args": ["-y", "mcp-remote@latest", "http://172.18.0.2:7861/gradio_api/mcp/"]
}
```

**Limitations:**
- ❌ IP changes if container restarts
- ❌ Brittle, not recommended for production
- ✅ Works on Linux, macOS, Windows with custom Docker networks

---

### Solution 4: Reverse Proxy (Production-Ready)

**Use nginx or Traefik to expose container:**

```yaml
# docker-compose.yml
version: '3.8'
services:
  dark-face-app:
    build: .
    expose:
      - "7861"
    networks:
      - proxy

  nginx:
    image: nginx:alpine
    ports:
      - "7861:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - dark-face-app
    networks:
      - proxy

networks:
  proxy:
```

**nginx.conf:**
```nginx
upstream dark_face {
    server dark-face-app:7861;
}

server {
    listen 80;
    location / {
        proxy_pass http://dark_face;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**MCP Config:**
```json
{
  "command": "npx",
  "args": ["-y", "mcp-remote@latest", "http://localhost:7861/gradio_api/mcp/"]
}
```

---

## 📊 Comparison Table

| Solution | Local Dev | Production | Linux | macOS | Windows | Complexity |
|----------|-----------|-----------|-------|-------|---------|-----------|
| `host.docker.internal` | ✅ | ⚠️ | ❌ | ✅ | ✅ | Low |
| Container Hostname | ⚠️ | ✅ | ✅ | ✅ | ✅ | Low |
| Container IP | ⚠️ | ❌ | ✅ | ⚠️ | ⚠️ | Low |
| Reverse Proxy (nginx) | ✅ | ✅ | ✅ | ✅ | ✅ | High |
| Gradio Share Link | ❌ | ❌ | ❌ | ❌ | ❌ | N/A |

---

## 🔧 Docker Compose Template (Working Example)

```yaml
version: '3.8'

services:
  dark-face-app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: dark-face-app
    
    # ✅ Port mapping so host can access port 7861
    ports:
      - "7861:7861"
    
    # ✅ Override server_name to 0.0.0.0 (listen on all interfaces)
    environment:
      - GRADIO_SERVER_NAME=0.0.0.0
      - GRADIO_SERVER_PORT=7861
    
    # ✅ For file I/O (if needed)
    volumes:
      - ./img/input:/app/img/input
      - ./img/output:/app/img/output
    
    # ✅ Named network for container-to-container communication
    networks:
      - bridge-net

networks:
  bridge-net:
    driver: bridge
```

**Then use from host:**
```json
{
  "command": "npx",
  "args": ["-y", "mcp-remote@latest", "http://host.docker.internal:7861/gradio_api/mcp/", "--allow-http"]
}
```

---

## 🚨 Troubleshooting Docker + MCP

### Error: `Connection refused`
```
mcp-remote: connect ECONNREFUSED 127.0.0.1:7861
```
**Solution:** Use `host.docker.internal` instead of `localhost`

### Error: `connect ETIMEDOUT 172.x.x.x:7861`
```
(old stale container IP)
```
**Solution:** Restart containers, use hostname instead of IP

### Error: `HTTP 403 Forbidden / SSL Certificate Error`
**Cause:** `--allow-http` missing for HTTP connections in private networks

**Solution:** Add `--allow-http` flag:
```json
"args": ["mcp-remote@latest", "http://host.docker.internal:7861/gradio_api/mcp/", "--allow-http"]
```

### Error: `port 7861 already in use`
```bash
# Find and kill existing process
lsof -i :7861
kill -9 <PID>

# Or use different port
docker run -p 8000:7861 dark-face-app
```

### Server running but tools don't appear in MCP client
1. Check server logs: `docker logs dark-face-app`
2. Test endpoint manually: `curl http://host.docker.internal:7861/gradio_api/mcp/`
3. Verify JSON response has `tools` array
4. Restart MCP client

---

## 📝 Best Practices

### ✅ DO
- ✅ Use `0.0.0.0` as `GRADIO_SERVER_NAME` in Docker
- ✅ Explicitly expose ports in docker-compose.yml
- ✅ Use container hostnames for service-to-service communication
- ✅ Set `--allow-http` for local/private networks
- ✅ Include environment variables for configuration

### ❌ DON'T
- ❌ Rely on `localhost:7861` from host → container
- ❌ Assume Gradio share links work inside containers
- ❌ Change `/etc/hosts` in containers
- ❌ Use hardcoded container IPs in production
- ❌ Expose HTTP endpoints to untrusted networks without HTTPS + auth

---

## 🔗 Additional Resources

- Docker Networking: https://docs.docker.com/engine/network/
- Gradio Deployment: https://www.gradio.app/guides/sharing-your-app
- mcp-remote Issues: https://github.com/geelen/mcp-remote/issues
- MCP Spec: https://modelcontextprotocol.io/

---

## Summary

**TL;DR:** Docker prevents containers from accessing `localhost` or external URLs. Use:
- **macOS/Windows:** `host.docker.internal:7861`
- **Service-to-Service:** `container-name:7861`
- **Production:** Reverse proxy (nginx/Traefik)
- **Always add:** `--allow-http` for private networks
