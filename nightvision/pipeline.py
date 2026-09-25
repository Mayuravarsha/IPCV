"""IR + visible fusion followed by colour transfer from a daylight photo.

Each function mirrors a file in ../matlab so the two versions can be read
side by side:

    piecewise_stretch  <-> pcs.m
    histeq             <-> he.m
    fuse_dwt           <-> fuse.m
    false_colour       <-> first half of enhance.m
    find_reference     <-> find_rgb.m (VLFeat SIFT -> OpenCV SIFT)
    color_transfer     <-> color_transfer.m (Reinhard et al., 2001)
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass
from typing import Sequence

import cv2
import numpy as np
import pywt
from skimage import color

SIZE = 400


def piecewise_stretch(img: np.ndarray, x1=40, x2=200, y1=0, y2=255) -> np.ndarray:
    """Map [0,x1) -> [0,y1), [x1,x2) -> [y1,y2) and [x2,255] -> [y2,255]."""
    f = img.astype(np.float64)
    out = np.where(
        f < x1,
        f * (y1 / x1),
        np.where(
            f < x2,
            (f - x1) * (y2 - y1) / (x2 - x1) + y1,
            (f - x2) * (255 - y2) / (255 - x2) + y2,
        ),
    )
    return np.clip(np.rint(out), 0, 255).astype(np.uint8)


def histeq(img: np.ndarray) -> np.ndarray:
    """Histogram-equalise every channel of a uint8 image independently."""
    if img.ndim == 2:
        return cv2.equalizeHist(img)
    return np.dstack([cv2.equalizeHist(np.ascontiguousarray(img[..., c]))
                      for c in range(img.shape[2])])


def fuse_dwt(a: np.ndarray, b: np.ndarray, wavelet: str = "db2") -> np.ndarray:
    """Single-level DWT fusion: average the approximations, max the details."""
    ca, (ha, va, da) = pywt.dwt2(a.astype(np.float64), wavelet, mode="symmetric")
    cb, (hb, vb, db) = pywt.dwt2(b.astype(np.float64), wavelet, mode="symmetric")
    fused = pywt.idwt2(
        ((ca + cb) / 2, (np.maximum(ha, hb), np.maximum(va, vb), np.maximum(da, db))),
        wavelet,
        mode="symmetric",
    )
    return fused[: a.shape[0], : a.shape[1]]


def false_colour(ir: np.ndarray, vis: np.ndarray) -> np.ndarray:
    """Build the equalised false-colour RGB image (fused+IR, VIS, VIS)."""
    fused = fuse_dwt(piecewise_stretch(ir), histeq(vis))
    fused = np.clip(np.rint(fused), 0, 255).astype(np.uint8)
    # MATLAB: imdivide(imadd(uint8(IR), uint8(r)), 2) -- saturating add first
    red = (np.minimum(ir.astype(np.int32) + fused, 255) / 2).round().astype(np.uint8)
    return histeq(np.dstack([red, vis, vis]))


_sift = None


def _descriptors(rgb: np.ndarray):
    global _sift
    if _sift is None:
        _sift = cv2.SIFT_create()
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    return _sift.detectAndCompute(gray, None)[1]


def count_matches(d1, d2, ratio: float = 1 / 1.5) -> int:
    """Lowe ratio-test matches; ratio 1/1.5 equals vl_ubcmatch's default."""
    if d1 is None or d2 is None or len(d1) < 2 or len(d2) < 2:
        return 0
    pairs = cv2.BFMatcher(cv2.NORM_L2).knnMatch(d1, d2, k=2)
    return sum(1 for p in pairs if len(p) == 2 and p[0].distance < ratio * p[1].distance)


@dataclass
class Match:
    index: int
    matches: int


def find_reference(query: np.ndarray, references: Sequence[np.ndarray]) -> Match:
    """Return the reference photo with the most SIFT matches to ``query``."""
    dq = _descriptors(query)
    best = Match(-1, -1)
    for i, ref in enumerate(references):
        n = count_matches(_descriptors(ref), dq)
        if n > best.matches:
            best = Match(i, n)
    return best


def color_transfer(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    """Give ``target`` the per-channel Lab mean/std of ``source`` (Reinhard 2001)."""
    s = color.rgb2lab(source)
    t = color.rgb2lab(target)
    s_mean, s_std = s.reshape(-1, 3).mean(0), s.reshape(-1, 3).std(0)
    t_mean, t_std = t.reshape(-1, 3).mean(0), t.reshape(-1, 3).std(0)
    out = (t - t_mean) * (s_std / np.maximum(t_std, 1e-6)) + s_mean
    with warnings.catch_warnings():
        # out-of-gamut Lab values are expected and clipped on purpose
        warnings.simplefilter("ignore", UserWarning)
        rgb = color.lab2rgb(out)
    return (np.clip(rgb, 0, 1) * 255).round().astype(np.uint8)


def enhance(ir: np.ndarray, vis: np.ndarray, references: Sequence[np.ndarray]):
    """Full pipeline. Returns (recoloured RGB, false colour RGB, Match)."""
    fc = false_colour(ir, vis)
    match = find_reference(fc, references)
    return color_transfer(references[match.index], fc), fc, match
