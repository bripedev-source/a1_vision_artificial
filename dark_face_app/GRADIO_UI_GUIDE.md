# 🎨 Guía Visual de la Interfaz Gradio

## 🌐 Acceso Rápido

**URL:** `http://localhost:7861`

La interfaz se divide en **7 pestañas principales**. Cada una es independiente pero puedes combinarlas para workflows complejos.

---

## 1️⃣ Meta-Cognitive Tab 🧠

**Qué es:** Panel de información sobre el agente

**Funcionalidad:**
- Detección automática del entorno (Local/Colab/Docker)
- IP local disponible
- Puerto de escucha (7861)
- Versión del API
- Información del servidor

**Cuándo usarlo:**
- Verificar que el servidor está corriendo
- Troubleshoot de conexión
- Confirmación de entorno

---

## 2️⃣ Help & Connectivity Tab ℹ️

**Qué es:** Guía interactiva de conexión MCP

**Secciones:**
1. **Connectivity Information** - Tu entorno actual
2. **MCP Configuration** - Instrucciones por cliente
3. **Quick Reference Table** - Tabla comparativa
4. **Environment Variables** - Configuración avanzada

**Clientes Soportados:**
- Claude Desktop
- Cursor IDE
- Windsurf
- VS Code + GitHub Copilot

**Cuándo usarlo:**
- Necesitas conectar MCP
- No sabes la sintaxis exacta de la configuración
- Troubleshoot de código con asistencia vía conexión MCP

---

## 3️⃣ Restoration & Enhancement Tab ✨

**Qué es:** Herramientas clásicas de procesamiento de imagen

### Subherramientas

#### **Gamma Correction**
- **Parámetro:** `gamma (0.1 - 3.0)`
- **Qué hace:** Ajusta el brillo exponencialmente
  - `gamma < 1.0` → más claro
  - `gamma = 1.0` → sin cambio
  - `gamma > 1.0` → más oscuro
- **Ejemplo:** Imagen oscura → `gamma = 0.5` → más clara
- **Tema:** Visión Artificial - Tema 6 (Enhancement)

#### **CLAHE (Contrast Limited Adaptive Histogram Equalization)**
- **Parámetro:** `clip_limit (1.0 - 4.0)`
- **Qué hace:** Realce adaptativo del contraste por regiones
- **Ventaja:** No sobre-amplifica ruido (a diferencia de equalization)
- **Ejemplo:** Imagen con contraste local pobre → CLAHE → mejora detalle
- **Tema:** Tema 6 (Enhancement)

#### **Log Transform**
- **Parámetro:** Ninguno
- **Qué hace:** Expande rangos oscuros, comprime claros
- **Fórmula:** `salida = log(1 + entrada)`
- **Ideal para:** Imágenes muy oscuras (nighttime, IR)
- **Tema:** Tema 6 (Enhancement)

#### **Histogram Equalization**
- **Parámetro:** Ninguno
- **Qué hace:** Estira el histograma globalmente
- **Cuidado:** Puede amplificar ruido
- **vs CLAHE:** Global vs Adaptativo por región
- **Tema:** Tema 6 (Enhancement)

#### **Median Filter**
- **Parámetro:** `kernel_size (3, 5, 7)`
- **Qué hace:** Remueve sal-pimienta sin desenfoque
- **Kernel:** Ventana cuadrada que toma valor central (mediana)
- **Ideal para:** Ruido impulsivo/impulsos únicos
- **Cuidado:** Kernel grande borra detalles finos
- **Tema:** Tema 5 (Restoration/Filtrado)

#### **Gaussian Blur**
- **Parámetros:** `kernel_size (default 5), sigma (default auto)`
- **Qué hace:** Suaviza imagen con desenfoque gaussiano
- **Ideal para:** Reducción general de ruido
- **vs Median:** Gaussian suaviza más, Median preserva bordes
- **Tema:** Tema 5 (Restoration)

### Workflow Típico en Esta Pestaña

```
1. Haz clic en "Select Image" o arrastra imagen
2. Selecciona operación de dropdown
3. Ajusta parámetro con slider
4. Visualiza resultado en tiempo real
5. Si te gusta → "Download" 
6. Si no → intenta otro parámetro
7. Repite pasos 3-6
```

---

## 4️⃣ Simulation Lab Tab 🧪

**Qué es:** Agrega ruido/degradación a imágenes para simular problemas reales

### Noise Simulation

#### **Gaussian Noise**
- **Parámetros:** `mean (default 0), sigma (default 25)`
- **Simula:** Ruido térmico/electrónico de cámara
- **Qué es:** Valores aleatorios distribuidos normalmente
- **Tema:** Tema 4 (Noise)

#### **Salt & Pepper Noise**
- **Parámetro:** `prob (0.0 - 1.0, default 0.05)`
- **Simula:** Píxeles muertos/hot pixels (impulsivo)
- **Qué es:** Píxeles aleatorios puro blanco (255) o negro (0)
- **Tema:** Tema 4 (Noise)

### Degradation Simulation

#### **Downsampling**
- **Parámetro:** `factor (0.1 - 1.0, default 0.5)`
- **Simula:** Pérdida de resolución, aliasing
- **Qué es:** Reduce tamaño → sube a original → aparecen artefactos
- **Tema:** Tema 3 (Sampling/Nyquist)

#### **Quantization**
- **Parámetro:** `bits (1-8, default 3)`
- **Simula:** Reducción de profundidad de bits (posterización)
- **Qué es:** Redondea valores de píxeles a menos niveles
- **Ejemplo:** 3 bits = 8 niveles de gris (muy posterizado)
- **Tema:** Tema 3 (Quantization/Sampling)

### Workflow Típico

```
1. Carga imagen limpia original
2. Simula ruido (Gaussian) con sigma=25
3. Visualiza degradación
4. En pestaña [Restoration], aplica Median Filter
5. Compara SNR antes/después en [Diagnosis]
6. Aprende cómo funcionan los filtros
```

---

## 5️⃣ Arithmetic Lab Tab ➕

**Qué es:** Operaciones píxel a píxel entre dos imágenes

### Operaciones Disponibles

#### **Add**
- Suma dos imágenes píxel a píxel
- Fórmula: `salida[i,j] = img1[i,j] + img2[i,j]`
- Riesgo: Saturación (valores > 255)
- Uso: Combinación de capas

#### **Subtract**
- Resta píxeles
- Fórmula: `salida[i,j] = abs(img1[i,j] - img2[i,j])`
- **Uso más común:** Detectar diferencias
- Ejemplo: `Imagen ruidosa - Imagen filtrada = Ruido visualizado`

#### **Multiply**
- Multiplica píxeles
- Fórmula: `salida[i,j] = img1[i,j] * img2[i,j] / 255`
- Uso: Máscaras, blending

#### **Divide**
- Divide píxeles (con cuidado con ceros)
- Uso: Normalización, ratios

### Workflow Típico

```
1. [Simulation] Abre imagen limpia
2. [Simulation] Agrega Gaussian Noise → noisy.png
3. [Restoration] Aplica Median Filter → filtered.png
4. [Arithmetic] Subtract: noisy.png - filtered.png
5. Resultado: Visualización del ruido que fue removido
```

**Tema:** Tema 6 (Operaciones aritméticas)

---

## 6️⃣ Diagnosis & Experiments Tab 🔬

**Qué es:** Análisis métrico y búsqueda automática de mejores parámetros

### Análisis de Imagen Individual

**Métricas que calcula:**
- **SNR (Signal-to-Noise Ratio):** Relación señal/ruido en dB
- **Entropía:** Cantidad de información contenida (0-8)
- **Rango Dinámico:** % de histograma usado
- **Píxeles Oscuros:** % de píxeles con valor < 128

**Cómo usarlo:**
1. Carga imagen en "Image Input"
2. Click en "Analyze Image"
3. Ve las métricas calculadas
4. Interpreta: SNR bajo = mucho ruido

### Run Experiment (🌟 Muy Útil)

**Qué hace:** Prueba automáticamente múltiples estrategias de mejora

**Proceso:**
1. Carga imagen problemática
2. Click "Run Experiment"
3. El sistema automáticamente:
   - Prueba Gamma (0.5, 1.0, 1.5, 2.0)
   - Prueba CLAHE (clip_limit 2.0, 4.0)
   - Prueba Log Transform
   - Prueba Equalization
   - Prueba combinaciones
4. Calcula SNR para cada resultado
5. Clasifica por ΔSNRdb (mejora en dB)

**Interpretación de Resultados:**
- **Top 1:** Mejor mejora encontrada
- **Recommended:** Estrategia con ΔSNRdb > 5 dB
- **Good:** ΔSNRdb > 2 dB
- **Marginal:** ΔSNRdb < 2 dB

**Uso Real:**
```
Imagen oscura de vigilancia nocturna:
1. Analyze → SNR = -8 dB, 95% dark pixels
2. Run Experiment
3. Mejor: Log + CLAHE (clip=3.0) con ΔSNRdb = +12 dB
4. Aplica esa combinación manualmente en [Enhancement]
5. Descarga resultado
```

### Run Median Demo (Especial)

**Qué hace:** Demostración completa de filtro de mediana

**Pasos:**
1. Carga imagen limpia
2. Especifica `noise_prob` (0.05 = 5% salt&pepper)
3. Sistema automáticamente:
   - Guarda original
   - Agrega ruido
   - Aplica median filter
   - Calcula diferencia
4. Visualiza antes/después lado a lado

**Ideal para:** Enseñanza de filtros

---

## 7️⃣ Pipelines & Batch Tab ⚙️

**Qué es:** Procesamiento complejo y en lote

### Pipeline (Imagen Individual)

**Qué es:** Secuencia de operaciones guardadas con trazabilidad

**Ejemplo Pipeline:**
```json
[
  {"operation": "log"},
  {"operation": "clahe", "clip_limit": 3.0},
  {"operation": "gaussian", "kernel_size": 3}
]
```

**Qué sucede:**
1. Imagen original
2. ↓ Log Transform
3. ↓ CLAHE (clip=3.0)
4. ↓ Gaussian (k=3)
5. Resultado final

**Salida generada:**
- `00_original.png`
- `01_log.png`
- `02_log_clahe3.png`
- `03_log_clahe3_gauss3.png`
- Reportes visuales para cada paso

**Ventaja:** Ves cada paso intermedio (trazabilidad total)

### Batch Processing

**Qué es:** Aplicar mismo pipeline a múltiples imágenes

**Workflow:**
1. Define pipeline JSON (o usa uno anterior)
2. Selecciona carpeta con 10, 100, 1000+ imágenes
3. Click "Process Batch"
4. Sistema aplica pipeline a TODAS
5. Organiza resultados por carpetas
6. Descarga todo automáticamente

**Ideal para:** Procesar datasets completos

---

## 📊 Comparación Rápida de Herramientas

| Pestaña | Entrada | Salida | Parámetros | Ideal Para |
|---------|---------|--------|-----------|-----------|
| **Enhancement** | 1 imagen | 1 imagen | Sliders | Experimentar |
| **Simulation** | 1 imagen | 1 imagen + ruido | Sliders | Aprender |
| **Arithmetic** | 2 imágenes | 1 imagen | Dropdown | Comparar |
| **Diagnosis** | 1 imagen | Métricas + análisis | Auto | Evaluar |
| **Diagnosis (Exp)** | 1 imagen | Múltiples resultados | Auto | Optimizar |
| **Pipelines** | 1 imagen | N imágenes (pasos) | JSON | Trazabilidad |
| **Batch** | N imágenes | N imágenes mejoradas | JSON pipeline | Producción |

---

## 🎯 Casos de Uso Completos

### Caso 1: "Quiero mejorar mi foto de noche"
```
1. [Enhancement] Carga foto
2. Prueba Log Transform
3. Prueba CLAHE (slider clip_limit)
4. Gaussiana si hay ruido
5. [Diagnosis] Analiza SNR antes/después
6. Download resultado
```
**Tiempo:** 2 minutos

### Caso 2: "Necesito entender cómo funcionan los filtros"
```
1. [Simulation] Carga imagen limpia
2. Agrega Gaussian Noise (sigma=25)
3. [Restoration] Aplica Median Filter
4. [Arithmetic] Sustrae: ruidosa - filtrada
5. Visualiza el ruido removido
6. [Diagnosis] Compara SNR
```
**Tiempo:** 5 minutos

### Caso 3: "Tengo 500 fotos oscuras de una cámara"
```
1. [Diagnosis] Una imagen: Run Experiment
2. Identifica mejor estrategia (ej: Log + CLAHE)
3. [Pipelines] Crea pipeline JSON
4. [Pipelines] Batch Process: carpeta con 500 fotos
5. Espera procesamiento automático
6. Descarga 500 fotos mejoradas
```
**Tiempo:** 30 segundos + espera de proceso

### Caso 4: "Quiero generar datos de entrenamiento"
```
1. [Simulation] Carga imagen limpia
2. Genera 10 versiones con diferentes ruidos
3. [Restoration] Mejora cada una
4. Genera dataset: original + degradado + mejorado
5. Usa para entrenar modelo de denoising
```
**Tiempo:** 10 minutos

---

## 💾 Dónde Van los Resultados

**Directorio base:** `dark_face_app/img/output/`

**Estructura automática:**
```
output/
├── Enhancement/        # Un paso
│   └── gamma, clahe, log, etc.
├── Restoration/        # Un paso
│   └── median, gaussian, etc.
├── Simulation/         # Un paso
│   └── gaussian_noise, downsampling, etc.
├── Experiments/        # Múltiples pasos (auto)
│   └── imagen_TIMESTAMP/
│       └── Todas las estrategias probadas
└── Pipelines/          # Múltiples pasos (manual)
    └── imagen_Flow/
        └── 00_original, 01_op1, 02_op2, ...
```

**Cómo descargar:**
- UI mostrará links de descarga
- También puedes copiar archivos manualmente de `output/`

---

## 🆘 Troubleshooting Visual

| Problema | Causa | Solución |
|----------|-------|----------|
| "No se ve cambio" | Parámetro muy pequeño | Aumenta gamma, clip_limit |
| "Imagen muy borrosa" | Gaussian kernel muy grande | Reduce kernel_size a 3 |
| "SNR no mejora" | Algoritmo no es el correcto para este ruido | Intenta otro en Diagnosis |
| "Descarga no funciona" | Problema del navegador | Intenta otro navegador o copia de output/ |
| "Batch muy lento" | 1000+ imágenes grandes | Acepta que toma tiempo, reduce tamaño |

---

## 📚 Temario Mapeado

| Tema | Pestañas Usadas | Operaciones |
|------|-----------------|------------|
| **Tema 3: Sampling** | Simulation | Downsampling, Quantization |
| **Tema 4: Noise** | Simulation, Restoration, Diagnosis | Gaussian/Salt-Pepper Noise, Median |
| **Tema 5: Filtrado** | Enhancement, Restoration | Median, Gaussian, Equalization |
| **Tema 6: Enhancement** | Enhancement, Experiments | Gamma, CLAHE, Log, Arithmetic |

Cada pestaña tiene referencias a los temas del syllabus.

---

## 🎓 Recomendación para Aprender

**Orden sugerido:**
1. **Primero:** Simulation (entiende qué es ruido)
2. **Segundo:** Restoration (aprende a filtrar)
3. **Tercero:** Enhancement (mejora más allá de denoising)
4. **Cuarto:** Diagnosis (entiende métricas)
5. **Quinto:** Arithmetic (compara resultados)
6. **Finalmente:** Pipelines (combina todo)
7. **Cuando entiendas:** MCP (automatiza)

**Recurso:** Cada operación en la UI tiene descripción, parámetros y tema asociado.
