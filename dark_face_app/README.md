# 🌑 Dark Face Enhancement App

## 🔬 Scientific Collaborative Interface (Human + AI)
Una plataforma híbrida diseñada para la colaboración entre **Investigadores Humanos** y **Agentes de IA** (vía MCP).

### 🌟 Características Clave (Syllabus Completo)
*   **Interfaz Híbrida**: Controles visuales (Arrastrar y Soltar / Sliders) para humanos, JSON puro para agentes.
*   **Laboratorio de Simulación**: Generación de ruido (Gaussiano/Salt&Pepper) y degradación digital (Downsampling/Cuantización).
*   **Aritmética de Imágenes**: Operaciones píxel a píxel (Suma, Resta, Multiplicación, División).
*   **Meta-Cognición**: Herramientas para que el agente inspeccione sus las capacidades de la app gradio.
*   **Pipelines de Ciencia Real**: Ejecución de experimentos controlados con trazabilidad completa.

---

## 🚀 Inicio Rápido

### Opción A: Ejecución Local (Recomendada)
Este proyecto usa **uv** para gestión moderna de dependencias.

1.  **Instalar y Ejecutar**:
    ```bash
    uv run dev.py
    ```
    *Nota: `dev.py` incluye recarga automática (hot-reload).*

2.  (Alternativa pip)
    ```bash
    pip install -r requirements.txt
    python dev.py
    ```

3.  **Abre el navegador:** `http://localhost:7861`
    - Interfaz visual completa + pestañas interactivas
    - No necesitas configuración de MCP
    - Ideal para exploración y aprendizaje

### Opción B: Docker
```bash
docker-compose up --build
```
Accede a: `http://localhost:7861`

---

## 🎨 Interfaz Visual de Gradio

### Acceso Directo en Navegador

**Abrir en navegador:** `http://localhost:7861`

La interfaz visual incluye todas las funcionalidades sin necesidad de configurar MCP. Es ideal para:
- 🧪 Experimentar con transformaciones de imagen
- 📊 Ver métricas en tiempo real
- 🎯 Testear pipelines complejos
- 📚 Aprender los algoritmos de visión artificial

### Pestañas Disponibles

#### 1. **🧠 Meta-Cognitive** 
Información sobre el agente y sus capacidades:
- Detección automática del entorno (Local, Colab, Docker)
- IPs disponibles y puertos
- Versión de la API
- Configuración actual

#### 2. **ℹ️ Help & Connectivity**
Guía interactiva de conexión MCP:
- Instrucciones específicas por cliente (Claude, Cursor, Windsurf, Copilot)
- Configuraciones copiar-pegar para cada IDE
- Tabla comparativa de métodos de conexión
- Troubleshooting integrado

#### 3. **✨ Restoration & Enhancement**
**Mejora de imágenes** usando transformaciones clásicas:

| Función | Parámetros | Uso | Tema |
|---------|-----------|-----|------|
| **Gamma Correction** | `gamma: 0.1-3.0` | Ajustar brillo | Tema 6 |
| **CLAHE** | `clip_limit: 1.0-4.0` | Realce adaptativo | Tema 6 |
| **Log Transform** | None | Expandir rango dinámico | Tema 6 |
| **Equalization** | None | Ecualización global | Tema 6 |
| **Median Filter** | `kernel_size: 3,5,7` | Remover ruido sal-pimienta | Tema 5 |
| **Gaussian Blur** | `kernel_size, sigma` | Reducción general de ruido | Tema 5 |

**Workflow Típico:**
1. Arrastra una imagen o sube desde archivo
2. Selecciona la operación
3. Ajusta parámetros con sliders
4. Visualiza resultado en tiempo real
5. Descarga imagen mejorada

#### 4. **🧪 Simulation Lab**
**Simula degradación de imágenes:**

- **Noise Simulation:**
  - Gaussian Noise (thermal/electronic)
  - Salt & Pepper Noise (impulsive)
  - Parámetros: mean, sigma, probability

- **Degradation Simulation:**
  - Downsampling (aliasing)
  - Quantization (posterization/bit-depth reduction)
  - Parámetros: factor, bits

**Use Case:** Entender cómo afecta el ruido/degradación a las imágenes

#### 5. **➕ Arithmetic Lab**
**Operaciones píxel a píxel entre imágenes:**

- Add (suma)
- Subtract (resta)
- Multiply (multiplicación)
- Divide (división)

**Ejemplo:** Restar dos imágenes para ver diferencia → detectar cambios

#### 6. **🔬 Diagnosis & Experiments**
**Análisis métrico y optimización:**

**Análisis Individual:**
- SNR (Signal-to-Noise Ratio)
- Entropía (información contenida)
- Rango dinámico
- Distribución de píxeles oscuros/claros

**Experimentos Automatizados:**
- Prueba múltiples estrategias de mejora automáticamente
- Compara resultados con métricas
- Recomienda mejor estrategia
- Genera reportes visuales

**Ejemplo de Experimento:**
1. Carga una imagen oscura
2. "Run Experiment" prueba:
   - Original (baseline)
   - Gamma corrections (0.5, 1.0, 1.5)
   - CLAHE (diferentes clip_limits)
   - Log Transform
   - Combinations
3. Resultados clasificados por ΔSNRdb (mejora)

#### 7. **⚙️ Pipelines & Batch**
**Procesamiento en lote y workflows complejos:**

**Pipeline (Imagen Individual):**
1. Define secuencia de operaciones (JSON o visual)
2. Aplica a una imagen
3. Guarda cada paso intermedio
4. Genera reportes para cada etapa
5. Trazabilidad completa del proceso

**Batch Processing:**
1. Carga carpeta con múltiples imágenes
2. Define pipeline una vez
3. Aplica automáticamente a todas
4. Organiza resultados en carpetas

**Ejemplo JSON Pipeline:**
```json
[
  {"operation": "log", "description": "Expandir dinámico"},
  {"operation": "clahe", "clip_limit": 3.0, "description": "Realce adaptativo"},
  {"operation": "gaussian", "kernel_size": 3, "description": "Desruido ligero"}
]
```

---

## 🎯 Flujos de Trabajo Comunes (Visual UI)

### Flujo 1: Mejorar Imagen Oscura
```
1. [Restoration] Abre imagen oscura
2. [Diagnosis] Analiza: SNR muy bajo, 90% píxeles oscuros
3. [Enhancement] Prueba Log Transform
4. [Enhancement] Prueba CLAHE con clip_limit 3.0
5. [Enhancement] Gaussian Blur (k=3) para desruido
6. [Diagnosis] Compara métricas antes/después
7. [Pipelines] Guarda pipeline para reutilizar
```

### Flujo 2: Experiment Científico
```
1. [Diagnosis] Carga imagen problemática
2. [Diagnosis] "Run Experiment" (prueba automática)
3. [Diagnosis] Revisa resultados clasificados
4. [Enhancement] Aplica estrategia recomendada manualmente
5. [Diagnosis] Genera reporte final
6. [Pipelines] Exporta pipeline optimizado
```

### Flujo 3: Procesamiento en Lote
```
1. [Pipelines] Define pipeline JSON:
   - Log Transform
   - CLAHE (clip=3.0)
   - Gaussian (k=3)
2. [Pipelines] Selecciona carpeta con 100+ imágenes
3. [Pipelines] "Batch Process"
4. Espera a que procese en background
5. Descarga carpeta con todas mejoradas
```

### Flujo 4: Aprender Algoritmos
```
1. [Simulation] Abre imagen limpia
2. [Simulation] Agrega "Gaussian Noise" (sigma=25)
3. [Restoration] Aplica "Median Filter" (k=5)
4. [Diagnosis] Compara SNR original vs ruidosa vs filtrada
5. [Arithmetic] Sustrae ruidosa - filtrada = "ruido removido"
6. [Help] Lee documentación sobre filtros
```

---

## 🖥️ UI vs MCP: Cuándo Usar Cada Una

| Característica | UI Visual | MCP (Agentes) |
|---------------|-----------|---------------|
| **Facilidad** | ⭐⭐⭐ Arrastra y suelta | ⭐⭐ Requiere config |
| **Velocidad Setup** | Instantáneo | 5-10 minutos |
| **Interactividad** | ✅ Real-time sliders | ❌ JSON params |
| **Automatización** | ❌ Manual | ✅ Programática |
| **Integración IDE** | ❌ Navegador separado | ✅ Dentro de Claude/Copilot |
| **Batch Processing** | ✅ Carpeta completa | ✅ Posible pero menos intuitivo |
| **Visualización** | ✅ Gráficos interactivos | ⚠️ JSON responses |
| **Reportes** | ✅ Histogramas + métricas | ✅ Métricas JSON |

**Recomendaciones:**
- **Aprende primero con UI** (experimenta, visualiza)
- **Usa MCP después** (automatiza, integra en flujos)
- **Combina ambas** (UI para desarrollo, MCP para producción)

---

## 📥 Inputs & Outputs

### Formatos Aceptados (UI)
- **Imágenes entrada:** PNG, JPG, BMP, TIFF
- **Archivos salida:** PNG (compresión lossless)
- **Reportes:** PNG (visualización de métricas)

### Estructura de Carpetas (Output)
```
output/
├── Enhancement/          # Mejora de contraste/brillo
│   ├── gamma/
│   ├── clahe/
│   └── log/
├── Restoration/         # Filtros de ruido
│   ├── median/
│   └── gaussian/
├── Simulation/          # Degradación/ruido agregado
│   ├── gaussian_noise/
│   └── downsampling/
├── Experiments/         # Resultados de experimentos
│   └── image_20251220_120000/
│       ├── Original.png
│       ├── Gamma_0.5.png
│       ├── CLAHE_Clip2.0.png
│       └── experiment_REPORT.json
└── Pipelines/          # Pipelines con trazabilidad
    └── image_Flow/
        ├── 00_original.png
        ├── 01_log.png
        ├── 02_log_clahe3.png
        └── 03_log_clahe3_gauss3.png
```

---

## 🚀 Tips & Tricks (UI)

### Tip 1: Experimenta Primero
No necesitas configurar MCP para empezar. La UI tiene todo lo que necesitas para aprender.

### Tip 2: Genera Reportes Automáticos
Cada operación genera un reporte visual con:
- Histograma antes/después
- Estadísticas (media, std, min, max)
- Visualización de mejora

### Tip 3: Usa Experiments para Encontrar Mejores Parámetros
En vez de probar manualmente, deja que "Run Experiment" pruebe combinaciones automáticamente.

### Tip 4: Descarga Pipelines como JSON
Genera un pipeline visual → exporítalo como JSON → úsalo en MCP o batch

### Tip 5: Comparación Visual de Ruido
Usa [Arithmetic] para **restar imágenes**:
- Imagen ruidosa - Imagen filtrada = Ruido removido visualizado

---

## 🔗 Siguiente: Integración MCP

### Cuándo Usar MCP

**MCP permite conectar la app a agentes de IA** (Claude, Cursor, Copilot, Windsurf) para:
- ✅ Automatizar flujos complejos con lenguaje natural
- ✅ Integrar procesamiento de imágenes en workflows de codificación
- ✅ Usar la app como herramienta dentro del IDE
- ✅ Programación sin configuración visual

**Si solo quieres experimentar:** usa la UI visual (opción más fácil)  
**Si quieres automatizar/integrar:** configura MCP

### Overview
Este proyecto expone una API compatible con **MCP** para conectar agentes de IA (Claude Desktop, Cursor, VS Code + Copilot, etc.) sin necesidad de código.

### Transport Protocols Soportados
- **STDIO** (Default): Conexión local directa (zero latency)
- **HTTP + SSE**: Para conexiones remotas (Colab, Docker, servidores web)

### Environment-Specific Configurations

#### 1. **Local/Native Setup** ✅ RECOMENDADO
```json
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
```
**Location:**
- Claude Desktop: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
- Claude Desktop: `%APPDATA%\Claude\claude_desktop_config.json` (Windows)
- Cursor: `~/.cursor/mcp.json`
- Windsurf: `~/.codeium/windsurf/mcp_config.json`

#### 2. **Google Colab Setup** 🔴
```json
{
  "servers": {
    "gradio-api-remote": {
      "url": "https://9797ddffb4c22ffcb7.gradio.live/gradio_api/mcp/",
      "type": "http"
    }
  },
  "inputs": []
}
```
**Location:** `.vscode/mcp.json` en VS Code con GitHub Copilot

**Automatic Share Link:**
- Gradio genera automáticamente links públicos: `https://XXXXXXXX.gradio.live/`
- Válidos por 7 días
- No requieren autenticación

#### 3. **Docker Setup** 🐳 (⚠️ Limitaciones Conocidas)
```json
{
  "mcpServers": {
    "dark-face-agent-docker": {
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
**Problemas Documentados:**
- Containers aislados no pueden acceder a `gradio.live` URLs
- Requieren `--allow-http` para conexiones HTTP en redes privadas
- Mejor solución: usar reverse proxy o exponer puertos explícitamente

### Troubleshooting & Diagnostics

| Problema | Causa | Solución |
|----------|-------|----------|
| `Connection refused` | Servidor no corriendo | `python mcp_interface.py` |
| `404 Not Found` | Endpoint incorrecto | Verificar `/gradio_api/mcp/` en URL |
| `HTTP vs STDIO mismatch` | Cliente espera STDIO, mcp-remote sirve HTTP | Usar `mcp-remote` como bridge |
| Colab + Copilot = No funciona | Copilot no soporta mcp-remote en Colab | Usar instrucciones en Help tab |
| Docker + gradio.live = Timeout | Docker aislado, no puede alcanzar URLs externas | Usar localhost con port mapping |

### Advanced MCP Configuration

**Custom Headers (Authentication):**
```json
{
  "mcpServers": {
    "dark-face-agent": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "https://remote.mcp.server/gradio_api/mcp/",
        "--header",
        "Authorization:Bearer${AUTH_TOKEN}"
      ],
      "env": {
        "AUTH_TOKEN": "your-token-here"
      }
    }
  }
}
```

**Transport Strategy (HTTP vs SSE):**
```json
"args": [
  "-y",
  "mcp-remote@latest",
  "https://remote.server/mcp/",
  "--transport",
  "http-first"  // Options: http-first, sse-first, http-only, sse-only
]
```

### About mcp-remote

`mcp-remote` es un puente NPM que convierte servidores HTTP/SSE en clientes stdio-compatible de MCP.

- **Repositorio:** https://github.com/geelen/mcp-remote
- **NPM:** `npm i mcp-remote`
- **Uso:** `npx mcp-remote <url> [options]`

**Ventajas:**
- ✅ Funciona con cualquier cliente stdio (Claude Desktop, Cursor, Windsurf)
- ✅ Soporta OAuth y custom headers
- ✅ Configurable (transport, timeouts, proxies)
- ✅ Debugging: `--debug` para logs detallados

---

## 📂 Organización del Temario (Pestañas)

1.  **🧠 Meta-Cognitive**: Autoconfiguración del agente.
2.  **✨ Restoration & Enhancement**: Filtros y mejoras (Gamma, CLAHE, Filtros Espaciales).
3.  **🧪 Simulation Lab**: Simulación de ruido y degradación de señal.
4.  **➕ Arithmetic Lab**: Operaciones algebraicas entre imágenes.
5.  **🔬 Diagnosis & Experiments**: Análisis métrico (SNR, Entropía) y optimización.
6.  **⚙️ Pipelines & Batch**: Procesamiento por lotes y workflows complejos.

## 🛠️ Tecnologías
*   **Gradio 5.x**: Interfaz Reactiva + Servidor MCP.
*   **OpenCV / Numpy**: Motores de cálculo matricial.
*   **Matplotlib**: Renderizado de métricas.

