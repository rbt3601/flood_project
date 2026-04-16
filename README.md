# CNN-Based Flood Damage Assessment from Satellite Imagery Using Semantic Segmentation

## Module
AI for Space – Assignment 2 Group Research Project

## Project Overview
This project investigates the application of Convolutional Neural Networks (CNNs) to a remote sensing problem using satellite imagery. Our selected problem is **flood damage assessment from satellite imagery using semantic segmentation**. The goal is to prepare a clean and reproducible pipeline for dataset inspection, preprocessing, mask generation, augmentation, model training, evaluation, and reporting.

## Selected Problem
**Flood damage assessment using satellite imagery**

The project uses **pre-event** and **post-event** satellite images together with annotations to identify flood-affected regions through a semantic segmentation workflow.

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

## Work Completed So Far
The following stages have been completed:

### 1. Dataset setup
- Project directory created
- Python virtual environment created
- Required packages installed
- Raw Germany training dataset downloaded and extracted

### 2. Data inspection (T03)
- Verified presence of:
  - pre-event images
  - post-event images
  - GeoJSON annotations
  - mapping CSV
  - reference CSV
- Loaded and inspected the mapping CSV
- Built exact image-label pairs using the mapping CSV
- Verified valid pairs
- Inspected raster metadata
- Inspected GeoJSON annotation structure
- Generated inspection outputs:
  - sample pre-event images
  - sample post-event images
  - sample mask previews
  - sample overlays
  - metadata summaries
  - quality check summaries

### 3. Preprocessing (T04)
- Split dataset into:
  - train
  - validation
  - test
- Created `metadata.csv`
- Generated segmentation masks from GeoJSON annotations
- Copied matching pre-event and post-event images into processed split folders
- Updated metadata so that paths point to processed files
- Kept all paths as **project-relative paths** for portability across laptops

### 4. Augmentation (T05)
- Implemented augmentation preview pipeline
- Generated before/after augmentation samples
- Verified that masks and images transform together

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
│   ├── preprocess_dataset.py
│   ├── generate_masks.py
│   └── augmentations.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Environment Setup

### 1. Clone the repository
```bash
git clone <YOUR_REPOSITORY_URL>
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
Typical packages used in this project include:

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

## How to Run the Current Pipeline

## Step 1 – Data inspection notebook
Open and run:

```text
notebooks/01_data_inspection.ipynb
```

This notebook:
- checks dataset structure
- loads the mapping CSV
- builds exact pairs
- verifies valid samples
- inspects metadata and annotations
- saves inspection previews and summaries

### Inspection outputs are saved in:
```text
outputs/inspection/
```

Typical outputs:
- `valid_pairs.csv`
- `image_metadata_summary.csv`
- `quality_check_summary.csv`
- `t03_summary.csv`
- sample images and overlays

---

## Step 2 – Preprocess and create dataset split
Run:

```bash
python src/preprocess_dataset.py
```

This script:
- reads valid pairs from `outputs/inspection/valid_pairs.csv`
- creates train/val/test split
- creates `data/processed/metadata.csv`

---

## Step 3 – Generate masks and processed split files
Run:

```bash
python src/generate_masks.py
```

This script:
- reads `data/processed/metadata.csv`
- rasterizes GeoJSON annotations into mask PNG files
- copies matching pre/post images into the correct split folders
- updates metadata paths to point to processed files

After running this step, each sample should exist in this form:

```text
data/processed/train/pre/sample_00000.tif
data/processed/train/post/sample_00000.tif
data/processed/train/mask/sample_00000.png
```

and similarly for `val` and `test`.

---

## Step 4 – Generate augmentation previews
Run:

```bash
python src/augmentations.py
```

This script:
- reads training samples from `metadata.csv`
- applies augmentation to image-mask pairs
- saves preview outputs for verification

### Augmentation outputs are saved in:
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

All paths are stored as **project-relative paths** such as:

```text
data/processed/train/pre/sample_00000.tif
data/processed/train/post/sample_00000.tif
data/processed/train/mask/sample_00000.png
```

This makes the project portable across laptops as long as the same folder structure is preserved.

---

## Important Notes for the Next Team Member
The next teammate responsible for model development should use:

```text
data/processed/metadata.csv
```

as the source of truth.

The model pipeline should load:
- pre-event image from `pre_path`
- post-event image from `post_path`
- segmentation mask from `mask_path`

The current outputs already support:
- train/validation/test separation
- segmentation mask availability
- augmentation preview verification

---

## What Is Still To Be Done
The following stages remain for the next parts of the group project:

### Model stage
- baseline model selection
- dataloader creation
- CNN model implementation
- training loop
- validation loop

### Evaluation stage
- IoU / Dice / Precision / Recall
- visual prediction inspection
- error analysis
- baseline vs improved model comparison

### Final deliverables
- report writing
- presentation video
- README final polishing
- code cleanup and documentation review

---

## Reproducibility Notes
- Keep the same folder structure
- Do not hardcode personal laptop paths
- Use only project-relative paths
- Run scripts from the project root folder
- Make sure `metadata.csv` is updated after each preprocessing stage

---

## AI Use Declaration
Generative AI tools were used to support:
- code drafting
- pipeline planning
- documentation structuring
- debugging support

All generated outputs were reviewed, corrected, and adapted manually before use.

---

## Authors / Team
Group members:
- Rajesh Bennegere Theertheswara
- Prajwal
- Saikiran
- Divya
- Reginald, Chimeka Praise

---

## Current Status Summary
Completed:
- dataset setup
- data inspection
- valid pair generation
- split creation
- mask generation
- augmentation preview generation

Next:
- model implementation and training
- evaluation
- final report and presentation
