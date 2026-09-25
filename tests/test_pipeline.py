import numpy as np
import pytest

from nightvision import color_transfer, false_colour, find_reference, fuse_dwt, histeq, piecewise_stretch
from nightvision.data import DATA_DIR, load_manifest, load_references, load_scene
from nightvision.metrics import average_gradient, colorfulness, entropy, spatial_frequency

rng = np.random.default_rng(0)


def test_piecewise_stretch_breakpoints():
    img = np.array([[0, 39, 40, 120, 199, 200, 255]], dtype=np.uint8)
    out = piecewise_stretch(img, 40, 200, 0, 255)
    assert out.dtype == np.uint8
    assert out[0, 0] == 0 and out[0, 1] == 0      # below x1 -> y1 = 0
    assert out[0, 2] == 0                          # x1 maps to y1
    assert out[0, 3] == round(80 * 255 / 160)      # linear middle segment
    assert out[0, 5] == 255 and out[0, 6] == 255   # above x2 saturates


def test_histeq_spreads_narrow_histogram():
    img = rng.integers(100, 120, size=(64, 64), dtype=np.uint8)
    out = histeq(img)
    assert out.min() < 20 and out.max() > 235


def test_histeq_handles_each_channel():
    img = rng.integers(0, 50, size=(32, 32, 3), dtype=np.uint8)
    assert histeq(img).shape == img.shape


def test_fuse_identical_images_is_identity():
    img = rng.integers(0, 255, size=(64, 64)).astype(float)
    np.testing.assert_allclose(fuse_dwt(img, img), img, atol=1e-8)


def test_fuse_keeps_edges_from_both_inputs():
    a = np.zeros((64, 64)); a[:, 32:] = 255      # vertical edge
    b = np.zeros((64, 64)); b[32:, :] = 255      # horizontal edge
    fused = fuse_dwt(a, b)
    assert fused.shape == a.shape
    assert average_gradient(np.clip(fused, 0, 255).astype(np.uint8)) > 0


def test_false_colour_shape():
    ir = rng.integers(0, 255, size=(64, 64), dtype=np.uint8)
    vis = rng.integers(0, 255, size=(64, 64), dtype=np.uint8)
    fc = false_colour(ir, vis)
    assert fc.shape == (64, 64, 3) and fc.dtype == np.uint8
    np.testing.assert_array_equal(fc[..., 1], fc[..., 2])  # G and B both come from VIS


def test_color_transfer_matches_source_statistics():
    from skimage import color
    src = np.zeros((32, 32, 3), np.uint8); src[..., 1] = 160; src[::2, :, 1] = 120
    tgt = rng.integers(40, 200, size=(32, 32, 3), dtype=np.uint8)
    out = color_transfer(src, tgt)
    s, o = color.rgb2lab(src).reshape(-1, 3), color.rgb2lab(out).reshape(-1, 3)
    np.testing.assert_allclose(o.mean(0), s.mean(0), atol=3)


def test_metrics_on_flat_and_busy_images():
    flat = np.full((32, 32), 128, np.uint8)
    busy = rng.integers(0, 256, size=(32, 32), dtype=np.uint8)
    assert entropy(flat) == 0
    assert entropy(busy) > 7
    assert average_gradient(flat) == 0 and spatial_frequency(flat) == 0
    assert spatial_frequency(busy) > spatial_frequency(flat)
    assert colorfulness(np.dstack([flat] * 3)) == 0


def test_manifest_points_at_real_files():
    manifest = load_manifest()
    assert len(manifest) >= 20
    for scene, entry in manifest.items():
        for key in ("IR", "VIS", "RGB"):
            if entry.get(key):
                assert (DATA_DIR / scene / entry[key]).exists(), (scene, key)


@pytest.mark.slow
def test_end_to_end_retrieves_own_photo():
    manifest = load_manifest()
    names, refs = load_references(manifest)
    ir, vis = load_scene("pancake_house", manifest)
    match = find_reference(false_colour(ir, vis), refs)
    assert names[match.index] == "pancake_house"
