"""Loading scenes described in data/dataset.json."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np

from .pipeline import SIZE

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_manifest(data_dir: Path = DATA_DIR) -> dict:
    return json.loads((data_dir / "dataset.json").read_text())


def read_gray(path: Path) -> np.ndarray:
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(path)
    return cv2.resize(img, (SIZE, SIZE), interpolation=cv2.INTER_CUBIC)


def read_rgb(path: Path) -> np.ndarray:
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(path)
    return cv2.cvtColor(cv2.resize(img, (SIZE, SIZE), interpolation=cv2.INTER_CUBIC),
                        cv2.COLOR_BGR2RGB)


def load_scene(name: str, manifest: dict, data_dir: Path = DATA_DIR):
    entry = manifest[name]
    return read_gray(data_dir / name / entry["IR"]), read_gray(data_dir / name / entry["VIS"])


def load_references(manifest: dict, data_dir: Path = DATA_DIR):
    """Return (scene names, RGB arrays) for every scene that has a daylight photo."""
    names = [n for n, e in manifest.items() if e.get("RGB")]
    return names, [read_rgb(data_dir / n / manifest[n]["RGB"]) for n in names]
