# 📚 Documentación Completa - Dark Face Agent

**Bienvenido a Dark Face Enhancement App** - Una plataforma científica híbrida para procesamiento de imágenes con Visión Artificial.

Este documento indexa toda la documentación disponible.

---

## 📖 Documentos Principales

### 1. **README.md** (Empezar aquí)
📄 Documento central del proyecto

**Contiene:**
- ✅ Descripción general
- ✅ Instrucciones de instalación (Local, Docker)
- ✅ Guía de UI Visual (7 pestañas)
- ✅ Flujos de trabajo comunes
- ✅ Comparación UI vs MCP
- ✅ Guía de MCP Integration

**Ideal para:** Primera vez, overview general

---

### 2. **GRADIO_UI_GUIDE.md** (Usar la interfaz visual)
🎨 Guía completa de la interfaz Gradio

**Contiene:**
- ✅ Acceso rápido a cada pestaña
- ✅ Explicación detallada de 7 pestañas
- ✅ Parámetros y fórmulas de cada operación
- ✅ Workflows completos paso a paso
- ✅ Mapeo a temario (Temas 3-6)
- ✅ Tips & tricks
- ✅ Troubleshooting

**Ideal para:**
- Usuarios que **NO quieren configurar MCP**
- Aprendizaje mediante experimentación
- Uso educativo (laboratorio de visión)
- Prototiping rápido

**Tiempo de lectura:** 10-15 minutos (saltar al tema que interese)

---

### 3. **MCP_QUICKSTART.md** (Conectar agentes IA)
⚡ Guía rápida de 5 minutos para MCP

**Contiene:**
- ✅ Setup rápido para cada cliente
- ✅ Claude Desktop
- ✅ Cursor IDE
- ✅ Windsurf
- ✅ VS Code + GitHub Copilot
- ✅ Google Colab especial
- ✅ Docker setup
- ✅ Testing de conexión
- ✅ Troubleshooting

**Ideal para:** Configuración rápida de MCP

**Tiempo:** 5 minutos para setup (si sabes qué cliente usar)

---

### 4. **MCP_CONFIG_CHEATSHEET.md** (Referencia rápida)
📋 Tabla de configuraciones copiar-pegar

**Contiene:**
- ✅ Todas las configuraciones listas para copiar
- ✅ Tabla comparativa
- ✅ What works vs what doesn't
- ✅ Solución para cada problema

**Ideal para:** Cuando ya sabes qué hacer, solo necesitas la sintaxis

**Tiempo:** 1 minuto (solo copiar-pegar)

---

### 5. **DOCKER_MCP_LIMITATIONS.md** (Docker + MCP)
🐳 Análisis profundo de Docker networking

**Contiene:**
- ✅ Por qué Docker no funciona "out of the box"
- ✅ Soluciones para cada OS (Linux, macOS, Windows)
- ✅ `host.docker.internal` vs container names vs IPs
- ✅ Reverse proxy example (production)
- ✅ Troubleshooting avanzado
- ✅ Tabla comparativa de soluciones

**Ideal para:**
- Debugging de Docker
- Entender network namespaces
- Setup production-ready

**Tiempo de lectura:** 10 minutos (o saltar al problema específico)

---

### 6. **MCP_INVESTIGATION_REPORT.md** (Investigación completa)
📊 Reporte ejecutivo de toda la investigación

**Contiene:**
- ✅ Resumen ejecutivo
- ✅ Protocolo comparison
- ✅ Environment-specific recommendations
- ✅ Configuration files & locations
- ✅ Key technical discoveries
- ✅ Troubleshooting flowchart
- ✅ Best practices

**Ideal para:**
- Entender toda la investigación
- Decisiones técnicas
- Referencia completa

**Tiempo de lectura:** 15 minutos

---

## 🎯 Flujos de Lectura Recomendados

### Flujo 1: "Solo quiero experimentar con imágenes"
```
1. Instala: README.md → "Inicio Rápido"
2. Abre navegador: http://localhost:7861
3. Lee: GRADIO_UI_GUIDE.md → Tabs que te interesen
4. Experimenta: Prueba los ejemplos de caso de uso
5. Listo
```
**Tiempo total:** 10 minutos  
**No necesitas:** MCP, Node.js, configuración JSON

---

### Flujo 2: "Quiero conectar desde Claude Desktop"
```
1. Instala: README.md → "Inicio Rápido"
2. Config: MCP_CONFIG_CHEATSHEET.md → Claude Desktop
3. Copia-pega la configuración
4. Reinicia Claude
5. Testing: MCP_QUICKSTART.md → "Testing Connection"
6. Listo
```
**Tiempo total:** 5 minutos (si instalaste Node.js)

---

### Flujo 3: "Tengo error en Docker"
```
1. Léeme: DOCKER_MCP_LIMITATIONS.md
2. Identifica tu caso (Linux? macOS? Windows?)
3. Aplica la solución específica
4. Troubleshoot: Flowchart en MCP_INVESTIGATION_REPORT.md
5. Check logs: MCP_QUICKSTART.md → "Check logs"
```
**Tiempo total:** 10-20 minutos

---

### Flujo 4: "Quiero entender TODO"
```
1. README.md (completo)
2. GRADIO_UI_GUIDE.md (UI visual)
3. MCP_INVESTIGATION_REPORT.md (contexto)
4. MCP_CONFIG_CHEATSHEET.md (referencia)
5. DOCKER_MCP_LIMITATIONS.md (si usas Docker)
```
**Tiempo total:** 1 hora

---

## 🗺️ Mapa de Características

### Funcionalidades por Pestaña (Interfaz Visual)

| Pestaña | Documenta en... | Ideal Para |
|---------|-----------------|-----------|
| Meta-Cognitive | README.md / GRADIO_UI_GUIDE.md | Info del servidor |
| Help & Connectivity | README.md / MCP_CONFIG_CHEATSHEET.md | Configuración MCP |
| Restoration & Enhancement | GRADIO_UI_GUIDE.md | Mejorar imágenes |
| Simulation Lab | GRADIO_UI_GUIDE.md | Aprender ruido |
| Arithmetic Lab | GRADIO_UI_GUIDE.md | Comparar imágenes |
| Diagnosis & Experiments | GRADIO_UI_GUIDE.md | Optimizar automático |
| Pipelines & Batch | GRADIO_UI_GUIDE.md | Procesamiento en lote |

---

## 🔗 Conexiones Rápidas

### Por Tema Syllabus

**Tema 3: Sampling & Quantization**
- Simulación: GRADIO_UI_GUIDE.md → "Simulation Lab" → Downsampling/Quantization
- Métricas: GRADIO_UI_GUIDE.md → "Diagnosis" → Rango dinámico

**Tema 4: Noise**
- Simulación: GRADIO_UI_GUIDE.md → "Simulation Lab" → Noise
- Filtrado: GRADIO_UI_GUIDE.md → "Restoration & Enhancement" → Filters
- Demo: GRADIO_UI_GUIDE.md → "Diagnosis" → Run Median Demo

**Tema 5: Restoration**
- Filtros: GRADIO_UI_GUIDE.md → "Restoration & Enhancement"
- Comparación: GRADIO_UI_GUIDE.md → "Arithmetic Lab" → Subtract

**Tema 6: Enhancement**
- Operaciones: GRADIO_UI_GUIDE.md → "Enhancement"
- Experimentos: GRADIO_UI_GUIDE.md → "Diagnosis" → Run Experiment
- Aritméticas: GRADIO_UI_GUIDE.md → "Arithmetic Lab"

---

## ❓ Encuentra tu Respuesta

### "¿Cómo instalo?"
→ **README.md** → "Inicio Rápido"

### "¿Cómo uso la interfaz visual?"
→ **GRADIO_UI_GUIDE.md** → Pestaña específica

### "¿Cómo configuro Claude Desktop?"
→ **MCP_QUICKSTART.md** → Claude Desktop  
→ O **MCP_CONFIG_CHEATSHEET.md** → copiar-pegar

### "¿Cómo configuro VS Code Copilot?"
→ **README.md** → VS Code section (formato diferente)  
→ O **MCP_CONFIG_CHEATSHEET.md** → copiar-pegar

### "¿Cómo configuro Cursor?"
→ **MCP_QUICKSTART.md** → Cursor IDE

### "¿Por qué no funciona en Docker?"
→ **DOCKER_MCP_LIMITATIONS.md** (análisis completo)

### "¿Cuál es la diferencia entre Claude, Cursor y Copilot?"
→ **MCP_INVESTIGATION_REPORT.md** → "Key Findings"

### "¿Cómo pruebo que MCP está conectado?"
→ **MCP_QUICKSTART.md** → "Testing Connection"

### "¿Cómo proceso 1000 imágenes?"
→ **GRADIO_UI_GUIDE.md** → "Pipelines & Batch" → Batch Processing

### "¿Cuál es la mejor estrategia para mi imagen oscura?"
→ **GRADIO_UI_GUIDE.md** → Diagnosis & Experiments → Run Experiment

### "¿Cómo funcionan los filtros de mediana?"
→ **GRADIO_UI_GUIDE.md** → Restoration Tab → Median Filter  
→ O usa **Run Median Demo** en Diagnosis tab

---

## 📝 Referencia Técnica

### Architectura
- **Servidor:** Gradio 5.x con MCP support
- **Backend:** Python + OpenCV + NumPy
- **Frontend:** Gradio UI (HTML/CSS/JS generado automáticamente)
- **Protocolos:** STDIO (local) + HTTP/SSE (remoto)

### Transports MCP Soportados
| Transport | Clientes | Config File |
|-----------|----------|------------|
| STDIO | Claude, Cursor, Windsurf | `.claude_desktop_config.json` |
| HTTP Direct | VS Code Copilot | `.vscode/mcp.json` |
| HTTP + mcp-remote | Todos (bridge) | Mismo que STDIO |

### Operaciones Disponibles
Tema 3-6 del syllabus completamente cubiertas:
- 4 Transformaciones de brillo (Gamma, CLAHE, Log, Equalization)
- 2 Filtros de ruido (Median, Gaussian)
- 2 Simulaciones de ruido (Gaussian, Salt&Pepper)
- 2 Degradaciones (Downsampling, Quantization)
- 4 Operaciones aritméticas (Add, Sub, Mult, Div)
- Análisis métrico (SNR, Entropía, Rango dinámico)
- Experimentación automática (compara N estrategias)
- Pipelines con trazabilidad completa
- Batch processing (N imágenes)

---

## 🆘 Guía de Troubleshooting Rápido

**Problema:** Servidor no arranca
→ Léeme: README.md → Inicio Rápido → Alternativa pip

**Problema:** No veo interfaz en navegador
→ Léeme: GRADIO_UI_GUIDE.md → "🌐 Acceso Rápido"

**Problema:** MCP no conecta
→ Léeme: MCP_QUICKSTART.md → "Testing Connection"

**Problema:** Docker no funciona
→ Léeme: DOCKER_MCP_LIMITATIONS.md (análisis completo)

**Problema:** No sé qué filtro usar
→ Léeme: GRADIO_UI_GUIDE.md → Diagnosis tab → Run Experiment (automático)

**Problema:** Imagen se ve rara después de filtro
→ Léeme: GRADIO_UI_GUIDE.md → Restoration tab → Parámetros correctos

**Problema:** Necesito documentación MCP oficial
→ https://modelcontextprotocol.io/

---

## 📚 Recursos Externos

### Documentación Oficial
- **MCP Spec:** https://modelcontextprotocol.io/
- **Gradio Docs:** https://www.gradio.app/docs/
- **OpenCV:** https://docs.opencv.org/
- **NumPy:** https://numpy.org/doc/

### Herramientas Mencionadas
- **mcp-remote:** https://github.com/geelen/mcp-remote
- **Gradio:** https://github.com/gradio-app/gradio
- **Claude Desktop:** https://claude.ai/download
- **Cursor:** https://www.cursor.com/
- **Windsurf:** https://www.codeium.com/windsurf

### Tutoriales Recomendados
- MCP QuickStart: https://modelcontextprotocol.io/quickstart
- Gradio Tutorial: https://www.gradio.app/getting_started/
- Docker Networking: https://docs.docker.com/engine/network/

---

## 📊 Estadísticas de Documentación

| Documento | Líneas | Secciones | Tiempo Lectura |
|-----------|--------|-----------|----------------|
| README.md | 300+ | 15+ | 15 min |
| GRADIO_UI_GUIDE.md | 400+ | 20+ | 20 min |
| MCP_QUICKSTART.md | 250+ | 10+ | 10 min |
| MCP_CONFIG_CHEATSHEET.md | 150+ | 10+ | 5 min |
| DOCKER_MCP_LIMITATIONS.md | 350+ | 15+ | 20 min |
| MCP_INVESTIGATION_REPORT.md | 400+ | 15+ | 20 min |
| **TOTAL** | **~1850** | **~85** | **1.5 horas** |

---

## ✅ Checklist Inicial

- [ ] Instalé el proyecto (README.md)
- [ ] Abrí navegador en `http://localhost:7861`
- [ ] Vi las 7 pestañas de la UI
- [ ] Cargué una imagen de prueba
- [ ] Apliqué una transformación
- [ ] Descargué resultado
- [ ] Leí GRADIO_UI_GUIDE.md
- [ ] Si quiero MCP, seguí MCP_QUICKSTART.md
- [ ] Si tengo problema, consulté troubleshooting específico

**Cuando completes esto:** ¡Ya sabes usar Dark Face App! 🎉

---

**Última actualización:** December 20, 2025  
**Versión:** 2.0.0 (Scientific/Traceable)  
**Mantenimiento:** [GitHub Issues](https://github.com/pesci/dark-face-app)

¿Preguntas? Revisa la pestaña Help & Connectivity en la app.
