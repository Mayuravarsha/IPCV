"""Run the pipeline on every scene and write results/ (images + metrics).

    python run_all.py                  # all scenes
    python run_all.py --scenes House   # a subset

Two retrieval settings are evaluated:
  * "database"      - the scene's own daylight photo is among the candidates
                      (what the original MATLAB code does)
  * "leave-one-out" - the scene's own photo is removed, so the colours must
                      come from a different scene (a harder, fairer test)
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import cv2
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from nightvision import enhance  # noqa: E402
from nightvision.data import load_manifest, load_references, load_scene  # noqa: E402
from nightvision.metrics import (  # noqa: E402
    average_gradient,
    colorfulness,
    entropy,
    spatial_frequency,
)

OUT = Path(__file__).resolve().parent / "results"


def gray(rgb: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)


def panel(path: Path, scene: str, images, titles) -> None:
    fig, axes = plt.subplots(1, len(images), figsize=(3 * len(images), 3.3))
    for ax, img, title in zip(axes, images, titles):
        ax.imshow(img, cmap="gray" if img.ndim == 2 else None, vmin=0, vmax=255)
        ax.set_title(title, fontsize=10)
        ax.axis("off")
    fig.suptitle(scene, fontsize=12)
    fig.tight_layout()
    fig.savefig(path, dpi=80)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--scenes", nargs="*", help="scene names (default: all)")
    args = parser.parse_args()

    manifest = load_manifest()
    ref_names, refs = load_references(manifest)
    scenes = args.scenes or list(manifest)
    (OUT / "scenes").mkdir(parents=True, exist_ok=True)

    rows = []
    for scene in scenes:
        ir, vis = load_scene(scene, manifest)
        out, fc, match = enhance(ir, vis, refs)

        loo_idx = [i for i, n in enumerate(ref_names) if n != scene]
        loo_out, _, loo_match = enhance(ir, vis, [refs[i] for i in loo_idx])
        loo_name = ref_names[loo_idx[loo_match.index]]

        panel(
            OUT / "scenes" / f"{scene}.png",
            scene,
            [ir, vis, fc, out, loo_out],
            ["IR", "Visible", "False colour", "Recoloured",
             f"Leave-one-out\n(colours from {loo_name})"],
        )

        fused_gray = gray(fc)
        rows.append({
            "scene": scene,
            "reference": ref_names[match.index],
            "own_photo_retrieved": ref_names[match.index] == scene,
            "sift_matches": match.matches,
            "loo_reference": loo_name,
            "entropy_vis": round(entropy(vis), 3),
            "entropy_ir": round(entropy(ir), 3),
            "entropy_fused": round(entropy(fused_gray), 3),
            "avg_gradient_vis": round(average_gradient(vis), 3),
            "avg_gradient_fused": round(average_gradient(fused_gray), 3),
            "spatial_freq_vis": round(spatial_frequency(vis), 3),
            "spatial_freq_fused": round(spatial_frequency(fused_gray), 3),
            "colorfulness_false": round(colorfulness(fc), 2),
            "colorfulness_recoloured": round(colorfulness(out), 2),
        })
        print(f"{scene:22s} ref={rows[-1]['reference']:22s} matches={match.matches}")

    with open(OUT / "metrics.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    with_photo = [r for r in rows if r["scene"] in ref_names]
    hits = sum(r["own_photo_retrieved"] for r in with_photo)
    mean = lambda k: np.mean([r[k] for r in rows])  # noqa: E731
    summary = (
        f"Scenes: {len(rows)}\n"
        f"Own daylight photo retrieved (top-1): {hits}/{len(with_photo)}\n"
        f"Mean entropy      visible {mean('entropy_vis'):.2f} -> fused {mean('entropy_fused'):.2f}\n"
        f"Mean avg gradient visible {mean('avg_gradient_vis'):.2f} -> fused {mean('avg_gradient_fused'):.2f}\n"
        f"Mean spatial freq visible {mean('spatial_freq_vis'):.2f} -> fused {mean('spatial_freq_fused'):.2f}\n"
        f"Mean colourfulness false colour {mean('colorfulness_false'):.1f} -> recoloured {mean('colorfulness_recoloured'):.1f}\n"
    )
    (OUT / "summary.txt").write_text(summary)
    print(summary)


if __name__ == "__main__":
    main()
