import cv2
import numpy as np
import matplotlib
# Use Agg backend for non-interactive plotting (avoid thread issues)
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import io

def generate_evaluation_plot(image, title="Analysis"):
    """
    Generates a composite image with the input image, its histogram, and metrics.
    Returns: numpy array (RGB image of the plot)
    """
    if image is None: return None
    
    # 1. Calc Metrics
    snr = calculate_snr(image)
    entropy = calculate_entropy(image)
    stats = calculate_advanced_statistics(image)
    
    # 2. Setup Plot
    fig = plt.figure(figsize=(12, 6), constrained_layout=True)
    gs = fig.add_gridspec(2, 2)
    
    # Image Subplot
    ax_img = fig.add_subplot(gs[:, 0])
    # Convert BGR to RGB for plotting
    plot_img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    ax_img.imshow(plot_img_rgb)
    ax_img.set_title(f"Result: {title}")
    ax_img.axis("off")
    
    # Histogram Subplot
    ax_hist = fig.add_subplot(gs[0, 1])
    colors = ('r', 'g', 'b')
    for i, color in enumerate(colors):
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        ax_hist.plot(hist, color=color)
        ax_hist.set_xlim([0, 256])
    ax_hist.set_title("Histogram (RGB)")
    ax_hist.grid(True, alpha=0.3)
    
    # Metrics Text
    ax_text = fig.add_subplot(gs[1, 1])
    text_str = (
        f"METRICS:\n"
        f"---------\n"
        f"SNR: {snr:.2f} dB\n"
        f"Entropy: {entropy:.3f}\n"
        f"Mean Intensity: {stats['mean']:.1f}\n"
        f"Std Dev (Contrast): {stats['std']:.1f}\n"
        f"Dynamic Range: {stats['dynamic_range']:.1f}"
    )
    ax_text.text(0.1, 0.5, text_str, fontsize=14, family='monospace', verticalalignment='center')
    ax_text.axis("off")
    
    # 3. Convert to Image
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100)
    buf.seek(0)
    
    # Decode buffer to cv2 image
    raw_data = np.frombuffer(buf.getvalue(), np.uint8)
    report_img = cv2.imdecode(raw_data, 1)
    
    plt.close(fig)
    return report_img

def apply_gamma(image, gamma=1.0):
    """
    Apply Gamma Correction to an image.
    Formula: O = ((I/255)^gamma) * 255
    
    Tema 6:
    - gamma < 1: Expande rango de píxeles oscuros (aclara la imagen)
    - gamma > 1: Comprime rango de píxeles oscuros (oscurece la imagen)
    - gamma = 1: Sin cambio
    """
    if gamma <= 0: return image
    # Apply gamma directly: O = I^gamma (normalized)
    table = np.array([((i / 255.0) ** gamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def apply_equalization(image):
    """
    Apply global Histogram Equalization.
    Converts to YCrCb to equalize only the Y (Luminance) channel.
    """
    if len(image.shape) == 3:
        # Convert to YCrCb
        ycrcb = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
        channels = list(cv2.split(ycrcb))
        # Equalize Y channel
        channels[0] = cv2.equalizeHist(channels[0])
        # Merge and convert back
        merged = cv2.merge(channels)
        return cv2.cvtColor(merged, cv2.COLOR_YCrCb2RGB)
    else:
        # Grayscale
        return cv2.equalizeHist(image)

def apply_median_filter(image, kernel_size=3):
    """
    Apply Median Blur for noise reduction.
    Kernel size must be odd and >= 3.
    
    Tema 5: Filtro de mediana - Ventana deslizante que reemplaza por la mediana.
    Elimina ruido "sal y pimienta".
    """
    k = int(kernel_size)
    if k < 3:
        return image  # No filter applied for k < 3
    if k % 2 == 0: 
        k += 1  # Ensure odd
    return cv2.medianBlur(image, k)

def apply_negative(image):
    """
    Apply Negative Transformation to an image.
    Formula: T(u) = L - u, where L = 255 for 8-bit images.
    Tema 6: Realza estructuras claras en áreas oscuras.
    """
    return 255 - image

def apply_log_transform(image, c=1.0):
    """
    Apply Logarithmic Transformation to an image.
    Formula: T(u) = C * log(1 + u)
    Tema 6: Expande rango de pixels oscuros, comprime claros.
    
    Args:
        image: Input image (uint8)
        c: Scaling constant (default 1.0, auto-scaled to use full range)
    """
    # Convert to float for calculation
    img_float = image.astype(np.float32)
    
    # Apply log transform: s = c * log(1 + r)
    # c is typically chosen to scale output to [0, 255]
    # c = 255 / log(1 + max_input)
    c_auto = 255 / np.log(1 + 255)
    
    result = c_auto * c * np.log(1 + img_float)
    
    # Clip and convert back to uint8
    result = np.clip(result, 0, 255).astype(np.uint8)
    return result

def apply_clahe(image, clip_limit=2.0, tile_grid_size=8):
    """
    Apply CLAHE (Contrast Limited Adaptive Histogram Equalization).
    Mejora la ecualización estándar evitando sobre-amplificación del ruido.
    
    Args:
        image: Input image
        clip_limit: Threshold for contrast limiting (default 2.0)
        tile_grid_size: Size of grid for histogram equalization (default 8x8)
    """
    if len(image.shape) == 3:
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid_size, tile_grid_size))
        l_clahe = clahe.apply(l)
        
        # Merge and convert back
        lab_clahe = cv2.merge([l_clahe, a, b])
        return cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)
    else:
        # Grayscale
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid_size, tile_grid_size))
        return clahe.apply(image)

def apply_contrast_stretching(image, low_percentile=2, high_percentile=98):
    """
    Apply Contrast Stretching (Linear Normalization).
    Tema 6: Función a trozos lineal - expande el rango [min, max] a [0, 255].
    
    Args:
        image: Input image
        low_percentile: Lower percentile to clip (default 2%)
        high_percentile: Upper percentile to clip (default 98%)
    
    Returns:
        Stretched image with enhanced contrast
    """
    if len(image.shape) == 3:
        # Apply per channel for color images
        result = np.zeros_like(image)
        for i in range(3):
            channel = image[:, :, i]
            low = np.percentile(channel, low_percentile)
            high = np.percentile(channel, high_percentile)
            if high - low > 0:
                stretched = (channel - low) * 255.0 / (high - low)
                result[:, :, i] = np.clip(stretched, 0, 255).astype(np.uint8)
            else:
                result[:, :, i] = channel
        return result
    else:
        low = np.percentile(image, low_percentile)
        high = np.percentile(image, high_percentile)
        if high - low > 0:
            stretched = (image - low) * 255.0 / (high - low)
            return np.clip(stretched, 0, 255).astype(np.uint8)
        return image

def apply_gaussian_filter(image, kernel_size=5, sigma=0):
    """
    Apply Gaussian Blur for noise reduction.
    Tema 5: Suavizado gaussiano - reduce ruido preservando estructura general.
    
    Args:
        image: Input image
        kernel_size: Size of the kernel (must be odd, default 5)
        sigma: Standard deviation (0 = auto-calculated from kernel size)
    """
    k = int(kernel_size)
    if k < 3:
        return image
    if k % 2 == 0:
        k += 1
    return cv2.GaussianBlur(image, (k, k), sigma)





def calculate_difference(img1, img2):
    """
    Calculate absolute difference between two images.
    """
    # Ensure same size
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    return cv2.absdiff(img1, img2)

def apply_arithmetic_ops(image1, image2, operation="add"):
    """
    Applies point-wise arithmetic operations between two images.
    Tema 6: Operaciones Aritméticas (Suma, Resta, Multiplicación, División).
    
    Args:
        image1: Primary image (uint8)
        image2: Secondary image (uint8) - will be resized to match image1
        operation: 'add', 'subtract', 'multiply', 'divide'
    """
    # 1. Resize image2 to match image1
    if image1.shape != image2.shape:
        image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
    
    # Ensure types
    img1 = image1.astype(float)
    img2 = image2.astype(float)
    
    if operation == "add":
        # Average / Fusion (prevents overflow)
        res = cv2.addWeighted(image1, 0.5, image2, 0.5, 0)
        return res
        
    elif operation == "subtract":
        # Absolute difference (Change detection)
        # Tema 6.4: C(x,y) = |A(x,y) - B(x,y)|
        return cv2.absdiff(image1, image2)
        
    elif operation == "multiply":
        # Masking / ROI selection
        # Normalized multiplication: (A * B) / 255
        res = (img1 * img2) / 255.0
        return np.clip(res, 0, 255).astype(np.uint8)
        
    elif operation == "divide":
        # Background normalization / Change detection
        # Avoid division by zero
        res = (img1 / (img2 + 1.0)) * 255.0
        # Normalize to visualize
        res = cv2.normalize(res, None, 0, 255, cv2.NORM_MINMAX)
        return res.astype(np.uint8)
    
    else:
        raise ValueError(f"Unknown arithmetic operation: {operation}")

def calculate_entropy(image):
    """
    Calculate Shannon Entropy of the image.
    H = -sum(p * log2(p))
    """
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    hist = hist.ravel() / hist.sum()
    
    logs = np.log2(hist + 1e-7) # Add epsilon to avoid log(0)
    entropy = -1 * (hist * logs).sum()
    return entropy

def calculate_snr(image):
    """
    Calculate Signal-to-Noise Ratio (SNR).
    Formula: SNR = 20 * log10(Mean / Std)
    
    Tema 4: SNR = 10·log₁₀(P_señal/P_ruido) en dB. Mayor = mejor calidad.
    """
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    mean_val = np.mean(image)
    std_val = np.std(image)
    
    # Handle edge cases
    if std_val == 0:
        return float('inf') if mean_val > 0 else 0  # Constant image
    if mean_val <= 0:
        return 0  # Completely black image
    
    # SNR = 20 * log10(mean / std)
    snr = 20 * np.log10(mean_val / std_val)
    return snr

def generate_histogram_plot(image, title="Histograma"):
    """
    Generate a histogram plot of the image.
    Returns a numpy array representing the plot image.
    """
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.hist(image.ravel(), 256, [0, 256], color='black')
    ax.set_title(title)
    ax.set_xlim([0, 256])
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("Nivel de Gris")
    ax.set_ylabel("Frecuencia")
    
    # Convert plot to numpy array
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    # Use buffer_rgba() instead of deprecated tostring_rgb()
    img_plot = np.asarray(canvas.buffer_rgba())
    # Convert RGBA to RGB
    img_plot = img_plot[:, :, :3]
    
    plt.close(fig)
    return img_plot

def calculate_freedman_diaconis_bins(image):
    """
    Calculate optimal number of histogram bins using Freedman-Diaconis rule.
    Tema 5: T = 2·IQR(x) / ∛n
    
    Returns: (n_bins, bin_width)
    """
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    data = image.ravel()
    n = len(data)
    
    q75, q25 = np.percentile(data, [75, 25])
    iqr = q75 - q25
    
    if iqr == 0:
        return 256, 1  # Default for constant images
    
    bin_width = 2 * iqr / np.cbrt(n)
    n_bins = int(np.ceil((data.max() - data.min()) / bin_width))
    n_bins = max(1, min(n_bins, 256))  # Clamp to reasonable range
    
    return n_bins, bin_width

def detect_outliers_iqr(image, k=1.5):
    """
    Detect outliers using IQR method.
    Tema 5: Valores fuera de [Q1 - k*IQR, Q3 + k*IQR] son outliers.
    
    Args:
        image: Input image
        k: IQR multiplier (default 1.5 for mild outliers, 3.0 for extreme)
    
    Returns: dict with outlier statistics
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image
    
    data = gray.ravel()
    q75, q25 = np.percentile(data, [75, 25])
    iqr = q75 - q25
    
    lower_bound = q25 - k * iqr
    upper_bound = q75 + k * iqr
    
    outliers_low = np.sum(data < lower_bound)
    outliers_high = np.sum(data > upper_bound)
    total_outliers = outliers_low + outliers_high
    outlier_percentage = (total_outliers / len(data)) * 100
    
    return {
        'q25': q25,
        'q75': q75,
        'iqr': iqr,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'outliers_low': outliers_low,
        'outliers_high': outliers_high,
        'total_outliers': total_outliers,
        'outlier_percentage': outlier_percentage
    }

def calculate_advanced_statistics(image):
    """
    Calculate comprehensive image statistics for analysis.
    Includes percentiles, skewness, and distribution metrics.
    
    Returns: dict with all statistics
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image
    
    data = gray.ravel().astype(float)
    
    # Basic statistics
    mean_val = np.mean(data)
    std_val = np.std(data)
    median_val = np.median(data)
    
    # Percentiles
    p5, p25, p50, p75, p95 = np.percentile(data, [5, 25, 50, 75, 95])
    
    # Dynamic range usage
    actual_min = np.min(data)
    actual_max = np.max(data)
    dynamic_range = actual_max - actual_min
    dynamic_usage = (dynamic_range / 255) * 100  # % of possible range used
    
    # Skewness (asymmetry)
    if std_val > 0:
        skewness = np.mean(((data - mean_val) / std_val) ** 3)
    else:
        skewness = 0
    
    # Dark/Bright balance
    dark_percentage = (np.sum(data < 128) / len(data)) * 100
    
    return {
        'mean': mean_val,
        'std': std_val,
        'median': median_val,
        'min': actual_min,
        'max': actual_max,
        'p5': p5,
        'p25': p25,
        'p50': p50,
        'p75': p75,
        'p95': p95,
        'iqr': p75 - p25,
        'dynamic_range': dynamic_range,
        'dynamic_usage_pct': dynamic_usage,
        'skewness': skewness,
        'dark_percentage': dark_percentage
    }

def apply_image_averaging(images):
    """
    Compute the average of a list of images.
    Tema 4: Image averaging for noise reduction.
    Formula: g(x,y) = (1/M) * sum(f_i(x,y))
    
    Args:
        images: List of numpy arrays (images)
    
    Returns:
        Averaged image (uint8)
    """
    if not images:
        raise ValueError("No images provided for averaging")
    
    # Initialize accumulator with float precision
    first_shape = images[0].shape
    accum = np.zeros(first_shape, dtype=np.float32)
    count = 0
    
    for img in images:
        # Resize if dimensions differ (robustness)
        if img.shape != first_shape:
            img = cv2.resize(img, (first_shape[1], first_shape[0]))
            
        accum += img.astype(np.float32)
        count += 1
        
    avg = accum / count
    return np.clip(avg, 0, 255).astype(np.uint8)

def add_gaussian_noise(image, mean=0, sigma=25):
    """
    Add Gaussian Noise to an image.
    Tema 4: Ruido térmico/electrónico (distribución normal).
    """
    row, col, ch = image.shape if len(image.shape) == 3 else (*image.shape, 1)
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    gauss = gauss.reshape(image.shape)
    noisy = image + gauss
    return np.clip(noisy, 0, 255).astype(np.uint8)

def add_salt_pepper_noise(image, prob=0.05):
    """
    Add Salt and Pepper Noise.
    Tema 4: Ruido impulsivo (valores extremos aleatorios).
    """
    noisy = np.copy(image)
    # Salt (White)
    num_salt = np.ceil(prob * image.size * 0.5)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
    noisy[tuple(coords)] = 255

    # Pepper (Black)
    num_pepper = np.ceil(prob * image.size * 0.5)
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
    noisy[tuple(coords)] = 0
    
    return noisy

def simulate_downsampling(image, factor=0.5):
    """
    Simulate Downsampling (Resolution Reduction).
    Tema 3: Muestreo. Simula aliasing/pixelado al reducir resolución.
    """
    if factor >= 1.0: return image
    
    height, width = image.shape[:2]
    new_h, new_w = int(height * factor), int(width * factor)
    
    # Resize down (loss of information)
    small = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_NEAREST)
    
    # Resize back up to keep original size for comparison
    restored = cv2.resize(small, (width, height), interpolation=cv2.INTER_NEAREST)
    return restored

def simulate_quantization(image, bits=3):
    """
    Simulate Color Quantization (Bit Depth Reduction).
    Tema 3: Cuantificación. Reduce la paleta de colores (posterización).
    """
    levels = 2 ** bits
    step = 255 / (levels - 1)
    
    quantized = np.round(image / step) * step
    return np.clip(quantized, 0, 255).astype(np.uint8)
