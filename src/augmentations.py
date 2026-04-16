from pathlib import Path
import random

import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import rasterio
import albumentations as A


# -----------------------------
# Project paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
METADATA_PATH = PROJECT_ROOT / "data" / "processed" / "metadata.csv"
OUT_DIR = PROJECT_ROOT / "outputs" / "augmentations"

OUT_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Path helpers
# -----------------------------
def normalize_rel_path(p):
    p = Path(str(p).replace("\\", "/"))
    parts = list(p.parts)
    if parts and parts[0] == "src":
        p = Path(*parts[1:])
    return p


def to_abs_path(p):
    p = normalize_rel_path(p)
    if p.is_absolute():
        return p
    return (PROJECT_ROOT / p).resolve()


def to_rel_str(p):
    p = normalize_rel_path(p)
    if p.is_absolute():
        try:
            return str(p.resolve().relative_to(PROJECT_ROOT.resolve())).replace("\\", "/")
        except Exception:
            return str(p).replace("\\", "/")
    return str(p).replace("\\", "/")


# -----------------------------
# Image / mask loading
# -----------------------------
def percentile_stretch(arr: np.ndarray) -> np.ndarray:
    arr = arr.astype(np.float32)

    if arr.ndim == 2:
        lo, hi = np.percentile(arr, (2, 98))
        return np.clip((arr - lo) / (hi - lo + 1e-6), 0, 1)

    out = np.zeros_like(arr, dtype=np.float32)
    for c in range(arr.shape[2]):
        lo, hi = np.percentile(arr[:, :, c], (2, 98))
        out[:, :, c] = np.clip((arr[:, :, c] - lo) / (hi - lo + 1e-6), 0, 1)
    return out


def read_tif_rgb(path_str: str) -> np.ndarray:
    """
    Read a .tif image and return an RGB-style preview array.
    If the image has >=3 bands, use the first 3 bands.
    If it has 1 band, repeat it to 3 channels.
    """
    path = to_abs_path(path_str)

    with rasterio.open(path) as src:
        if src.count >= 3:
            arr = src.read([1, 2, 3])  # (C, H, W)
            arr = np.transpose(arr, (1, 2, 0))  # (H, W, C)
        else:
            arr = src.read(1)
            arr = np.stack([arr] * 3, axis=-1)

    arr = percentile_stretch(arr)
    arr = (arr * 255).astype(np.uint8)
    return arr


def read_mask_png(path_str: str) -> np.ndarray:
    """
    Read a PNG mask as 2D uint8.
    Converts any non-zero pixel to 1.
    """
    path = to_abs_path(path_str)
    mask = Image.open(path).convert("L")
    mask = np.array(mask, dtype=np.uint8)
    mask = (mask > 0).astype(np.uint8)
    return mask


# -----------------------------
# Augmentation definition
# -----------------------------
def build_train_transform():
    """
    Image and mask are transformed together.
    """
    return A.Compose([
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.5),
        A.RandomRotate90(p=0.5),
        A.RandomBrightnessContrast(p=0.5),
        A.GaussNoise(p=0.3),
    ])


# -----------------------------
# Saving helpers
# -----------------------------
def save_img(img: np.ndarray, out_path: Path, cmap=None):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6, 6))
    if img.ndim == 2:
        plt.imshow(img, cmap=cmap or "gray")
    else:
        plt.imshow(img)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(out_path, dpi=180, bbox_inches="tight", pad_inches=0)
    plt.close()


def save_overlay(image: np.ndarray, mask: np.ndarray, out_path: Path, color=(0, 1, 1), alpha=0.35):
    """
    Save an overlay of a binary mask on top of an RGB image.
    """
    img = image.astype(np.float32) / 255.0
    color = np.array(color, dtype=np.float32).reshape(1, 1, 3)

    overlay = np.where(mask[..., None] > 0, (1 - alpha) * img + alpha * color, img)
    overlay = np.clip(overlay, 0, 1)

    save_img((overlay * 255).astype(np.uint8), out_path)


# -----------------------------
# Main preview generation
# -----------------------------
def main():
    if not METADATA_PATH.exists():
        raise FileNotFoundError(f"metadata.csv not found: {METADATA_PATH}")

    df = pd.read_csv(METADATA_PATH)

    required_cols = {"sample_id", "split", "post_path", "mask_path"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"metadata.csv is missing required columns: {missing}")

    # Use only successfully generated masks
    if "mask_status" in df.columns:
        df = df[df["mask_status"] == "OK"].copy()

    # Use train split for augmentation preview
    train_df = df[df["split"] == "train"].copy()

    if train_df.empty:
        raise ValueError("No training rows found in metadata.csv")

    # Choose up to 5 random training samples
    n_samples = min(10, len(train_df))
    sample_df = train_df.sample(n=n_samples, random_state=42)

    transform = build_train_transform()

    preview_rows = []

    print("Generating augmentation previews for", n_samples, "training samples")

    for row in sample_df.itertuples(index=False):
        sample_id = row.sample_id

        # Read original post image + mask
        image = read_tif_rgb(row.post_path)
        mask = read_mask_png(row.mask_path)

        # Apply augmentation
        augmented = transform(image=image, mask=mask)
        aug_image = augmented["image"]
        aug_mask = augmented["mask"]

        # Output paths
        orig_img_out = OUT_DIR / f"{sample_id}_orig_post.png"
        orig_mask_out = OUT_DIR / f"{sample_id}_orig_mask.png"
        aug_img_out = OUT_DIR / f"{sample_id}_aug_post.png"
        aug_mask_out = OUT_DIR / f"{sample_id}_aug_mask.png"
        orig_overlay_out = OUT_DIR / f"{sample_id}_orig_overlay.png"
        aug_overlay_out = OUT_DIR / f"{sample_id}_aug_overlay.png"

        # Save originals
        save_img(image, orig_img_out)
        save_img(mask * 255, orig_mask_out, cmap="gray")
        save_overlay(image, mask, orig_overlay_out)

        # Save augmented versions
        save_img(aug_image, aug_img_out)
        save_img(aug_mask * 255, aug_mask_out, cmap="gray")
        save_overlay(aug_image, aug_mask, aug_overlay_out)

        preview_rows.append({
            "sample_id": sample_id,
            "orig_post_preview": to_rel_str(orig_img_out),
            "orig_mask_preview": to_rel_str(orig_mask_out),
            "aug_post_preview": to_rel_str(aug_img_out),
            "aug_mask_preview": to_rel_str(aug_mask_out),
            "orig_overlay_preview": to_rel_str(orig_overlay_out),
            "aug_overlay_preview": to_rel_str(aug_overlay_out),
        })

    preview_df = pd.DataFrame(preview_rows)
    preview_csv = OUT_DIR / "augmentation_preview_summary.csv"
    preview_df.to_csv(preview_csv, index=False)

    print("Saved preview summary:", preview_csv)
    print(preview_df.head())


if __name__ == "__main__":
    main() 