from pathlib import Path
import json
import shutil

import numpy as np
import pandas as pd
from PIL import Image

import rasterio
from rasterio.features import rasterize
from shapely.geometry import shape


PROJECT_ROOT = Path(__file__).resolve().parents[1]
METADATA_PATH = PROJECT_ROOT / "data" / "processed" / "metadata.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def normalize_rel_path(p):
    """
    Normalize a path string so it becomes project-relative and
    does not accidentally keep a leading 'src/'.
    """
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


# Ensure processed folders exist
for split in ["train", "val", "test"]:
    (PROCESSED_DIR / split / "pre").mkdir(parents=True, exist_ok=True)
    (PROCESSED_DIR / split / "post").mkdir(parents=True, exist_ok=True)
    (PROCESSED_DIR / split / "mask").mkdir(parents=True, exist_ok=True)


def rasterize_geojson_to_mask(label_path, ref_image_path):
    label_path = to_abs_path(label_path)
    ref_image_path = to_abs_path(ref_image_path)

    with rasterio.open(ref_image_path) as src:
        out_shape = (src.height, src.width)
        transform = src.transform

    with open(label_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    shapes = []
    for feat in data.get("features", []):
        geom = feat.get("geometry")
        if geom is None:
            continue
        try:
            shapes.append((shape(geom), 1))
        except Exception:
            continue

    if not shapes:
        return np.zeros(out_shape, dtype=np.uint8)

    mask = rasterize(
        shapes=shapes,
        out_shape=out_shape,
        transform=transform,
        fill=0,
        dtype="uint8"
    )
    return mask


def save_mask_png(mask, out_path):
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    mask_img = (mask * 255).astype(np.uint8)
    Image.fromarray(mask_img).save(out_path)


def copy_image(src_path, dst_path):
    src_path = to_abs_path(src_path)
    dst_path = Path(dst_path)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dst_path)


def main():
    if not METADATA_PATH.exists():
        raise FileNotFoundError(f"metadata.csv not found: {METADATA_PATH}")

    df = pd.read_csv(METADATA_PATH)

    required_cols = {"sample_id", "split", "pre_path", "post_path", "label_path"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"metadata.csv is missing required columns: {missing}")

    # Clean existing metadata paths before use
    for col in ["pre_path", "post_path", "label_path"]:
        df[col] = df[col].apply(to_rel_str)

    new_pre_paths = []
    new_post_paths = []
    new_mask_paths = []
    statuses = []

    print("Loaded rows:", len(df))

    for row in df.itertuples(index=False):
        sample_id = row.sample_id
        split = row.split
        pre_path = row.pre_path
        post_path = row.post_path
        label_path = row.label_path

        try:
            # Keep original file extension for images
            pre_ext = to_abs_path(pre_path).suffix
            post_ext = to_abs_path(post_path).suffix

            out_pre_path = PROCESSED_DIR / split / "pre" / f"{sample_id}{pre_ext}"
            out_post_path = PROCESSED_DIR / split / "post" / f"{sample_id}{post_ext}"
            out_mask_path = PROCESSED_DIR / split / "mask" / f"{sample_id}.png"

            # Copy pre and post images into processed split folders
            copy_image(pre_path, out_pre_path)
            copy_image(post_path, out_post_path)

            # Generate mask using the original post image as reference
            mask = rasterize_geojson_to_mask(label_path, post_path)
            save_mask_png(mask, out_mask_path)

            new_pre_paths.append(to_rel_str(out_pre_path))
            new_post_paths.append(to_rel_str(out_post_path))
            new_mask_paths.append(to_rel_str(out_mask_path))
            statuses.append("OK")

        except Exception as e:
            new_pre_paths.append(None)
            new_post_paths.append(None)
            new_mask_paths.append(None)
            statuses.append(f"ERROR: {e}")
            print(f"Failed for {sample_id}: {e}")

    # Update metadata to point to processed split folders
    df["pre_path"] = new_pre_paths
    df["post_path"] = new_post_paths
    df["mask_path"] = new_mask_paths
    df["mask_status"] = statuses

    df.to_csv(METADATA_PATH, index=False)

    print("\nProcessing complete.")
    print("Successful rows:", (df["mask_status"] == "OK").sum())
    print("Failures:", (df["mask_status"] != "OK").sum())
    print("Updated metadata saved to:", METADATA_PATH)

    print("\nExample rows:")
    print(df[["sample_id", "split", "pre_path", "post_path", "label_path", "mask_path", "mask_status"]].head())


if __name__ == "__main__":
    main()