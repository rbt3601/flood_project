# CNN-Based Flood Damage Assessment from Satellite Imagery Using Semantic Segmentation

## Module
AI for Space – Assignment 2 Group Research Project

## Project Overview
This project focuses on **flood damage assessment from satellite imagery using semantic segmentation**.  
The current work completed in this repository covers the **data preparation pipeline**, including:

- dataset setup
- data inspection
- train/validation/test split creation
- mask generation from GeoJSON annotations
- augmentation preview generation

Later stages such as model training, evaluation, comparison, report writing, and presentation will be added by other team members.

---

## Selected Problem
**Flood damage assessment using satellite imagery**

The project uses:
- **pre-event satellite images**
- **post-event satellite images**
- **GeoJSON annotations**

to prepare a segmentation-ready dataset for CNN-based flood analysis.

---

## Dataset
The dataset used is the **Germany Training Public** portion of the extracted SpaceNet 8 flood dataset.

### Raw dataset structure
```text
data/raw/
├── PRE-event/
├── POST-event/
├── annotations/
├── Germany_Training_Public_label_image_mapping.csv
└── Germany_Training_Public_reference.csv
```

---

## Work Completed by Rajesh

### 1. Dataset setup
Completed:
- project directory creation
- Python virtual environment setup
- dependency installation
- raw dataset download and extraction

### 2. Data inspection
Completed:
- verified pre-event, post-event, annotation, mapping, and reference files
- loaded and inspected the mapping CSV
- created exact image-label pairs
- checked valid pairs
- inspected raster metadata
- inspected GeoJSON label structure
- generated sample previews and summary outputs

### 3. Preprocessing
Completed:
- created train / validation / test split
- generated `metadata.csv`
- copied split-wise pre/post images into processed folders
- generated mask PNG files from GeoJSON annotations
- updated metadata to point to processed files
- used project-relative paths for portability

### 4. Augmentation preview
Completed:
- created augmentation preview pipeline
- generated original vs augmented image-mask examples
- verified that masks and images transform together

---

## Current Project Structure
```text
flood_project/
├── data/
│   ├── raw/
│   │   ├── PRE-event/
│   │   ├── POST-event/
│   │   ├── annotations/
│   │   ├── Germany_Training_Public_label_image_mapping.csv
│   │   └── Germany_Training_Public_reference.csv
│   └── processed/
│       ├── train/
│       │   ├── pre/
│       │   ├── post/
│       │   └── mask/
│       ├── val/
│       │   ├── pre/
│       │   ├── post/
│       │   └── mask/
│       ├── test/
│       │   ├── pre/
│       │   ├── post/
│       │   └── mask/
│       └── metadata.csv
├── docs/
├── notebooks/
│   └── 01_data_inspection.ipynb
├── outputs/
│   ├── inspection/
│   └── augmentations/
├── src/
│   ├── preprocess_dataset.ipynb
│   ├── generate_masks.ipynb
│   └── augmentations.ipynb
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Environment Setup

### 1. Clone the repository
```bash
git clone https://github.com/rbt3601/flood_project.git
cd flood_project
```

### 2. Create and activate virtual environment

#### Windows (Git Bash)
```bash
py -m venv .venv
source .venv/Scripts/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Required Python Packages
This project currently uses:

- pandas
- numpy
- matplotlib
- pillow
- rasterio
- shapely
- scikit-learn
- albumentations
- opencv-python

---

## How to Run the Completed Pipeline

## Step 1 – Run data inspection
Open and run:

```text
notebooks/01_data_inspection.ipynb
```

This notebook:
- checks dataset structure
- loads mapping CSV
- builds exact pairs
- verifies valid samples
- inspects metadata and annotations
- saves sample previews and summaries

### Outputs saved in:
```text
outputs/inspection/
```

Typical outputs:
- `valid_pairs.csv`
- `image_metadata_summary.csv`
- `quality_check_summary.csv`
- `t03_summary.csv`
- sample previews and overlays

---

## Step 2 – Create dataset split
Open and run:

```text
src/preprocess_dataset.ipynb
```

This script:
- reads valid pairs from `outputs/inspection/valid_pairs.csv`
- creates train / val / test split
- saves `data/processed/metadata.csv`

---

## Step 3 – Generate masks and processed split files
Open and run:

```text
src/generate_masks.ipynb
```

This script:
- reads `data/processed/metadata.csv`
- generates mask PNG files from GeoJSON annotations
- copies matching pre/post images into processed split folders
- updates metadata paths to point to processed files

After running this step, sample files should exist like:

```text
data/processed/train/pre/sample_00000.tif
data/processed/train/post/sample_00000.tif
data/processed/train/mask/sample_00000.png
```

---

## Step 4 – Generate augmentation previews
Open and run:

```text
src/augmentations.ipynb
```

This script:
- reads training rows from `metadata.csv`
- applies augmentation to image-mask pairs
- saves preview outputs for verification

### Outputs saved in:
```text
outputs/augmentations/
```

Typical outputs:
- original post image preview
- original mask preview
- augmented post image preview
- augmented mask preview
- original overlay
- augmented overlay
- `augmentation_preview_summary.csv`

---

## Metadata Format
The processed metadata file is:

```text
data/processed/metadata.csv
```

Typical columns:
- `sample_id`
- `split`
- `pre_path`
- `post_path`
- `label_path`
- `mask_path`
- `mask_status`

All paths are stored as **project-relative paths**, for example:

```text
data/processed/train/pre/sample_00000.tif
data/processed/train/post/sample_00000.tif
data/processed/train/mask/sample_00000.png
```

---

## Important Notes
- Use `data/processed/metadata.csv` as the source of truth.
- Do not hardcode personal laptop paths.
- Use only project-relative paths.
- Run scripts from the project root folder.
- Keep the same folder structure across laptops.

---

## Current Status
Completed in this repository:
- dataset setup
- data inspection
- valid pair generation
- train/validation/test split creation
- mask generation
- augmentation preview generation

Remaining work will be added later by other team members.

---

## Author
Completed current data pipeline work by:

- rbt3 - Rajesh Bennegere Theertheswara

## Prajwal - Baseline Model and Training
- Notebook: notebooks/prajwal_baseline_training.ipynb
- Purpose: Trains a U-Net baseline segmentation model for flood detection
- Input: data/processed/metadata.csv
- How to run: open the notebook and run all cells top to bottom
- Outputs: outputs/prajwal/checkpoints/best_model.pth, outputs/prajwal/loss_curve.png, outputs/prajwal/training_log.csv
