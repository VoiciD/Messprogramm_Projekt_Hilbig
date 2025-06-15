import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.optimize import curve_fit

def analysiere_schwerpunkt(Ixy, pixel_size=0.0106, threshold=80, show=True):
    """
    Führt Schwerpunkt- und Momentenanalyse mit Darstellung inkl. Gaussprofil durch.

    Parameter:
        Ixy (ndarray): Graustufenbild als 2D NumPy-Array
        pixel_size (float): Pixelgröße in mm
        threshold (int): Schwellwert für die Maske
        show (bool): Ob das Ergebnis geplottet werden soll

    Rückgabe:
        dict mit Schwerpunkt (in px & mm), Varianzen und 1D-Gauss-Fits
    """

    image_np = Ixy
    image_inverted = 255 - image_np
    mask = image_inverted < threshold

    # Nur größte zusammenhängende Region
    labeled, num_features = ndimage.label(mask)
    sizes = ndimage.sum(mask, labeled, range(1, num_features + 1))
    if len(sizes) == 0:
        raise ValueError("Keine erkennbare Region im Bild gefunden.")
    largest_label = (np.argmax(sizes) + 1)
    mask = labeled == largest_label

    # Schwerpunkt
    cy, cx = ndimage.center_of_mass(mask)
    y_indices, x_indices = np.where(mask)
    var_x = np.var(x_indices)
    var_y = np.var(y_indices)

    # In mm umrechnen
    cx_mm = cx * pixel_size
    cy_mm = cy * pixel_size
    var_x_mm = var_x * pixel_size**2
    var_y_mm = var_y * pixel_size**2

    # 1D-Profil durch Schwerpunkt
    row = image_np[int(round(cy)), :]
    col = image_np[:, int(round(cx))]

    def gauss(x, A, mu, sigma, offset):
        return A * np.exp(-(x - mu)**2 / (2 * sigma**2)) + offset

    x = np.arange(len(row))
    y = np.arange(len(col))

    try:
        popt_row, _ = curve_fit(gauss, x, row, p0=[255, cx, 10, 0])
        popt_col, _ = curve_fit(gauss, y, col, p0=[255, cy, 10, 0])
    except:
        popt_row = [0, 0, 0, 0]
        popt_col = [0, 0, 0, 0]

    return {
        "cx_px": cx,
        "cy_px": cy,
        "cx_mm": cx_mm,
        "cy_mm": cy_mm,
        "var_x_mm2": var_x_mm,
        "var_y_mm2": var_y_mm,
        "gauss_x": popt_row,
        "gauss_y": popt_col,
    }

def analysiere_schwerpunkt_mit_gaussprofil(Ixy, pixel_size=0.0106, threshold=80, show=True):
    """
    Führt Schwerpunkt- und Momentenanalyse mit Darstellung inkl. Gaussprofil durch.

    Parameter:
        Ixy (ndarray): Graustufenbild als 2D NumPy-Array
        pixel_size (float): Pixelgröße in mm
        threshold (int): Schwellwert für die Maske
        show (bool): Ob das Ergebnis geplottet werden soll

    Rückgabe:
        dict mit Schwerpunkt (in px & mm), Varianzen und 1D-Gauss-Fits
    """

    image_np = Ixy
    image_inverted = 255 - image_np
    mask = image_inverted < threshold

    # Nur größte zusammenhängende Region
    labeled, num_features = ndimage.label(mask)
    sizes = ndimage.sum(mask, labeled, range(1, num_features + 1))
    if len(sizes) == 0:
        raise ValueError("Keine erkennbare Region im Bild gefunden.")
    largest_label = (np.argmax(sizes) + 1)
    mask = labeled == largest_label

    # Schwerpunkt
    cy, cx = ndimage.center_of_mass(mask)
    y_indices, x_indices = np.where(mask)
    var_x = np.var(x_indices)
    var_y = np.var(y_indices)

    # In mm umrechnen
    cx_mm = cx * pixel_size
    cy_mm = cy * pixel_size
    var_x_mm = var_x * pixel_size**2
    var_y_mm = var_y * pixel_size**2

    # 1D-Profil durch Schwerpunkt
    row = image_np[int(round(cy)), :]
    col = image_np[:, int(round(cx))]

    def gauss(x, A, mu, sigma, offset):
        return A * np.exp(-(x - mu)**2 / (2 * sigma**2)) + offset

    x = np.arange(len(row))
    y = np.arange(len(col))

    try:
        popt_row, _ = curve_fit(gauss, x, row, p0=[255, cx, 10, 0])
        popt_col, _ = curve_fit(gauss, y, col, p0=[255, cy, 10, 0])
    except:
        popt_row = [0, 0, 0, 0]
        popt_col = [0, 0, 0, 0]

    if show:
        # Bild mit Schwerpunkt
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        plt.imshow(image_np, cmap='gray')
        plt.scatter(cx, cy, color='red', s=100, marker='x', label='Schwerpunkt')
        plt.title(f"Schwerpunkt (rot)\nx={cx_mm} mm, y={cy_mm} mm")
        plt.axis('off')
        plt.legend()

        # 1D-Gaussprofil
        plt.subplot(1, 2, 2)
        plt.plot(x * pixel_size, row, label="X-Profil")
        plt.plot(x * pixel_size, gauss(x, *popt_row), '--', label="Gaussfit X")
        plt.plot(y * pixel_size, col, label="Y-Profil")
        plt.plot(y * pixel_size, gauss(y, *popt_col), '--', label="Gaussfit Y")
        plt.xlabel("Position [mm]")
        plt.ylabel("Intensität")
        plt.legend()
        plt.title("1D-Gaussprofil durch Schwerpunkt")
        plt.tight_layout()
        plt.show()

    return {
        "cx_px": cx,
        "cy_px": cy,
        "cx_mm": cx_mm,
        "cy_mm": cy_mm,
        "var_x_mm2": var_x_mm,
        "var_y_mm2": var_y_mm,
        "gauss_x": popt_row,
        "gauss_y": popt_col,
    }

