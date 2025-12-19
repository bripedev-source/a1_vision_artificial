# 📚 Ideas Clave del Temario de Visión Artificial (Ampliado)

## Índice
1. [Tema 1: Introducción a los Sistemas de Percepción](#tema-1)
2. [Tema 2: Elementos de un Sistema de Percepción](#tema-2)
3. [Tema 3: Captura y Digitalización de Señales](#tema-3)
4. [Tema 4: Fuentes y Tipos de Ruido](#tema-4)
5. [Tema 5: Detección y Cancelación de Anomalías](#tema-5)
6. [Tema 6: Procesamiento de Imagen - Operaciones Elementales](#tema-6)

---

## Tema 1: Introducción a los Sistemas de Percepción {#tema-1}

| Concepto | Descripción |
|----------|-------------|
| Sistema Auditivo | El sonido es una perturbación mecánica del medio (onda). Se mide en W/m² y dB. |
| Estructura del oído | Oído externo (pabellón, conducto, tímpano) → Oído medio (martillo, yunque, estribo, ventana oval) → Oído interno (cóclea, nervio auditivo) |
| Rango audible | 20 Hz - 20 kHz. Voz humana: 300 Hz - 3.4 kHz |
| Sistema Visual | La visión resulta de la incidencia de luz (onda electromagnética) sobre la retina |
| Células fotosensibles | **Conos** (visión diurna, color) y **Bastones** (visión nocturna, sin color) |
| Tipos de conos | L (560nm, rojo), M (530nm, verde), S (420nm, azul) |
| **Ley de Weber** | ΔI/I = λ → La diferencia mínima perceptible (JND) es proporcional a la intensidad. **Respuesta logarítmica** del sistema visual. |
| Inhibición lateral | Filtro paso-alto que realza bordes y contrastes |
| Frecuencia de fusión | ~30 Hz para percibir movimiento continuo |
| Síntesis de color | RGB: cualquier color se sintetiza con 3 primarios (rojo, verde, azul) |

---

## Tema 2: Elementos de un Sistema de Percepción {#tema-2}

| Concepto | Descripción |
|----------|-------------|
| 3 funciones principales | 1. Captura de información, 2. Procesamiento, 3. Toma de decisión y aprendizaje |
| Parámetros de sensores | Especificidad, Precisión, Sensibilidad, Consumo, Tamaño |
| Conversión A/D | **Muestreo** (fotos a intervalos) + **Cuantificación** (valores numéricos) + **Codificación** (binario) |
| Ventajas digital | Menor almacenamiento, filtrado por software, compresión, encriptación |
| Preprocesamiento | **Eliminación de ruido**, detección de anomalías, corrección de errores |
| Procesamiento | Filtrado/suavizado, Segmentación, Extracción de características |
| Segmentación | División de imagen en regiones con propiedades similares |
| Extracción de características | Vector de características para comparar regiones/objetos |

---

## Tema 3: Captura y Digitalización de Señales {#tema-3}

| Concepto | Descripción |
|----------|-------------|
| Analogía del mosaico | Número de colores = niveles de cuantificación; Tamaño de tesela = frecuencia de muestreo |
| **Teorema de Nyquist** | f_muestreo ≥ 2·f_señal (frecuencia mínima para capturar una señal sin pérdida) |
| Señal analógica | Continua, todo el detalle, almacenamiento complejo |
| Señal digital | Discreta, reducción de información, fácil almacenamiento |
| Conversor A/D | Muestreador → Cuantificador → Codificador |
| Submuestreo (aliasing) | Muestrear bajo Nyquist → distorsión, señal aparenta ir más lento |
| Sobremuestreo | Capturar información de más, reconstrucción errónea |
| Cuantificación | Mayor número de bits → mayor fidelidad (ej: 8 bits = 256 niveles) |

---

## Tema 4: Fuentes y Tipos de Ruido {#tema-4}

### Definición de Ruido
El ruido es toda señal **no deseada y de naturaleza aleatoria** que modifica la intensidad de la señal original:

$$S(t) = f(t) + r(t)$$

Donde:
- $S(t)$: Señal recibida
- $f(t)$: Señal original
- $r(t)$: Componente de ruido

### Entropía de Shannon
La entropía mide la **cantidad de información/incertidumbre** de una fuente:

$$H(X) = -\sum_{i=1}^{M} P(X_i) \log_2[P(X_i)]$$

**Interpretación**:
- **Alto ruido → Alta entropía** (mayor desorden)
- **Bajo ruido → Baja entropía** (patrones repetitivos)
- Máxima entropía cuando todos los eventos son equiprobables

### Relación Señal a Ruido (SNR)

$$SNR = 10 \cdot \log_{10}\left(\frac{P_{señal}}{P_{ruido}}\right) \text{ dB}$$

O equivalentemente:

$$SNR = 20 \cdot \log_{10}\left(\frac{\mu}{\sigma}\right) \text{ dB}$$

Donde $\mu$ es la media y $\sigma$ la desviación estándar.

**Interpretación**: Mayor SNR = **mejor calidad** de señal.

### Clasificación del Ruido

| Tipo | Origen | Características |
|------|--------|-----------------|
| **Atmosférico** | Descargas naturales (ionosfera, tormentas) | Mayor impacto en bajas frecuencias (AM) |
| **Industrial** | Automóviles, motores, líneas alto voltaje | Predomina en zonas urbanas (1-600 MHz) |
| **Impulsivo (Shot)** | Rayos, chispas, interferencias breves | Valores pico bruscos de corta duración |
| **Galáctico** | Sol y otras estrellas | Variación cíclica (~11 años) |
| **Térmico** | Agitación de electrones en circuitos | Inevitable, solo se cancela a 0K absoluto |
| **Flicker (1/f)** | Transistores, resistencias | Mayor impacto < 1 kHz |

### Procesos Estocásticos
Las señales ruidosas se modelan como **procesos estocásticos**:
- **Estacionario en sentido estricto**: La función de densidad no varía con el tiempo
- **Estacionario en sentido amplio**: Media y varianza constantes en el tiempo

---

## Tema 5: Detección y Cancelación de Anomalías {#tema-5}

### Definición de Anomalía (Outlier)
Patrón inusual que **no se ajusta al comportamiento esperado**. Indica ruido impulsivo o inestabilidades en la captura.

### Tipos de Anomalías

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Puntual** | Valor individual extremadamente diferente al resto | Transacción de tarjeta con monto absurdamente alto |
| **Contextual** | Atípico solo en su contexto/vecindad | Temperatura de 30°C es normal en verano, anómala en invierno |
| **Colectiva** | Conjunto de valores que juntos son anómalos | Señal ECG plana durante tiempo prolongado |

### Métodos de Identificación

| Método | Descripción | Ejemplo de uso |
|--------|-------------|----------------|
| **Supervisado** | Clasificador entrenado con etiquetas (anomalía/normal) | Detección de fraude con tarjetas |
| **Semisupervisado** | Aprende solo lo "normal", detecta desviaciones | One-class SVM, Autoencoders |
| **No supervisado** | Sin etiquetas, basado en distancias/densidades | Detección de ruido en señales |

### Filtro de Mediana

El filtro de mediana es una **ventana deslizante** que reemplaza cada punto por la mediana de su vecindad.

**Propiedades**:
- Elimina ruido **"sal y pimienta"** (picos impulsivos)
- Preserva bordes mejor que el promedio
- Tamaño de ventana debe ser **impar** (3, 5, 7...)

**Aplicación**:
- Serie temporal: ventana de longitud N
- Imagen: ventana de tamaño N×N

**Ejemplo** (ventana=5, punto en negrita):
```
Serie: [2, 1, 3, 45, 2, 3, 1, 2]
                 ↑
Vecindad = [1, 3, 45, 2, 3] → Ordenada = [1, 2, 3, 3, 45] → Mediana = 3
```

### Técnicas Estadísticas

Basadas en la **función de densidad de probabilidad** $f(x)$:
- Valores poco probables → Candidatos a anomalías
- Se puede aplicar **global** (toda la imagen) o **local** (ventana)

#### Estimación del Histograma
Regla de Freedman-Diaconis para número óptimo de intervalos:

$$T = 2 \cdot IQR(x) / \sqrt[3]{n}$$

Donde $IQR$ es el rango intercuartil (P75 - P25) = P50.

**Aplicación**: Útil para visualizar espectros de Fourier (rango dinámico amplio).

---

## Tema 6: Procesamiento de Imagen - Operaciones Elementales {#tema-6}

### Principio Fundamental
Las operaciones de realce buscan **capturar la información relevante** de la imagen:
- Remarcar el contenido
- Aumentar el nivel de contraste
- Enfatizar y delimitar transiciones (bordes)

### Operaciones Punto a Punto
El valor de salida depende **únicamente** del valor de entrada en ese mismo píxel:

$$B(x, y) = T(A(x, y))$$

Donde:
- $A$: Imagen original
- $B$: Imagen procesada
- $T$: Función de transformación

### Transformaciones de Intensidad

#### 1. Negativo de una Imagen

$$T(u) = L - u$$

Donde $L = 255$ para imágenes de 8 bits.

**Uso**: Realza estructuras claras encerradas en áreas oscuras.

#### 2. Transformación Logarítmica

$$T(u) = C \cdot \log(1 + u)$$
**Donde u es el valor de entrada y C es un factor de escala**
**Efectos**:
- El logaritmo **expande los píxeles oscuros** y **comprime los píxeles claros**.
- La constante **C** ajusta la intensidad de esa expansión/compresión:
  - **C pequeño (<1)**: menor contraste global.
  - **C grande (>1)**: mayor contraste en zonas oscuras, aunque los claros siguen comprimidos.
**Aplicación**: Útil para visualizar espectros de Fourier (rango dinámico amplio)

#### 3. Corrección Gamma (Ley de Potencia)

$$T(u) = C \cdot u^{\gamma}$$

| Valor de γ | Efecto | Aplicación |
|------------|--------|------------|
| **γ < 1** | Expande oscuros, comprime claros | **Aclarar imágenes oscuras** |
| **γ = 1** | Sin cambio (identidad) | - |
| **γ > 1** | Comprime oscuros, expande claros | Oscurecer imágenes sobreexpuestas |

**Ventaja**: Genera una familia amplia de transformaciones variando un solo parámetro.

#### 4. Funciones Definidas a Trozos
Transformaciones personalizadas por rangos de intensidad. Requieren intervención manual del usuario.

**Uso**: Realce de contraste cuando la imagen tiene rango dinámico reducido.

### Procesamiento del Histograma

#### Histograma
Estimación de la **función de densidad de probabilidad** de intensidades.

$$p_l = \frac{n_l}{N}$$

Donde:
- $n_l$: Número de píxeles con intensidad $l$
- $N$: Número total de píxeles

#### Ecualización del Histograma
Convierte la distribución a **uniforme** → Aumenta contraste automáticamente.

$$X_i = F_Y(Y_i) = \sum_{k=0}^{l} p_k$$

Donde $F_Y$ es la función de distribución acumulada estimada con el histograma.

**Resultado**: Mayor dispersión en los valores de intensidad → Mejor contraste.

### Operadores Aritméticos

#### Operador Resta (Diferencia)

$$C(x, y) = B(x, y) - A(x, y)$$

**Uso**: Realza **diferencias** entre dos imágenes.

**Aplicación médica**: Sustracción de imagen de referencia para visualizar movimiento de sustancia de contraste.

#### Operador Suma (Promediado)

$$C(x, y) = \frac{1}{M} \sum_{i=1}^{M} A_i(x, y)$$

**Uso**: **Reduce ruido de captación** cuando se tienen múltiples exposiciones de la misma escena.

**Propiedad clave**: La varianza del ruido se atenúa por factor $M$:

$$\sigma_C^2 = \frac{\sigma^2}{M}$$

**Requisito**: Las instantáneas deben estar perfectamente alineadas.
