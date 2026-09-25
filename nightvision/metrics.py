"""No-reference image quality metrics commonly reported for image fusion."""

import numpy as np


def entropy(gray: np.ndarray) -> float:
    """Shannon entropy (bits) of an 8-bit image's histogram."""
    hist = np.bincount(gray.ravel(), minlength=256).astype(np.float64)
    p = hist[hist > 0] / hist.sum()
    return float(-(p * np.log2(p)).sum())


def average_gradient(gray: np.ndarray) -> float:
    """Mean magnitude of the local gradient; higher means sharper detail."""
    g = gray.astype(np.float64)
    gx = np.diff(g, axis=1)[:-1, :]
    gy = np.diff(g, axis=0)[:, :-1]
    return float(np.mean(np.sqrt((gx ** 2 + gy ** 2) / 2)))


def spatial_frequency(gray: np.ndarray) -> float:
    """Overall activity level: sqrt(row frequency^2 + column frequency^2)."""
    g = gray.astype(np.float64)
    rf = np.sqrt(np.mean(np.diff(g, axis=1) ** 2))
    cf = np.sqrt(np.mean(np.diff(g, axis=0) ** 2))
    return float(np.hypot(rf, cf))


def colorfulness(rgb: np.ndarray) -> float:
    """Hasler & Suesstrunk (2003) colourfulness; 0 for a grayscale image."""
    r, g, b = (rgb[..., i].astype(np.float64) for i in range(3))
    rg, yb = r - g, 0.5 * (r + g) - b
    return float(np.hypot(rg.std(), yb.std()) + 0.3 * np.hypot(rg.mean(), yb.mean()))
