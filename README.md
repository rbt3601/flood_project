# CNN-Based Flood Damage Assessment from Satellite Imagery Using Semantic Segmentation

## Module
AI for Space – Group Coursework

## Repository
`https://github.com/rbt3601/flood_project`

---

## 1. Project Overview

This project studies **flood damage assessment from satellite imagery using semantic segmentation**.

The main idea is simple:

- we use a **pre-event image** (before flood)
- we use a **post-event image** (after flood)
- we use **ground-truth flood labels**
- we train segmentation models to identify **flood-affected regions at pixel level**

The project workflow is:

1. dataset setup and inspection  
2. preprocessing and mask generation  
3. baseline model training  
4. evaluation of baseline results  
5. improved model experiment  
6. comparison and error analysis  

---

## 2. Team Contributions

### rbt3 – Rajesh Bennegere Theertheswara
Responsible for the **data preparation and preprocessing stage**.

Completed work:
- project setup
- dataset inspection
- valid pre/post/label pair creation
- train / validation / test split creation
- `metadata.csv` creation
- GeoJSON to mask PNG generation
- processed dataset folder structure creation
- augmentation preview generation

Main files:
- `notebooks/01_data_inspection.ipynb`
- `src/preprocess_dataset.ipynb`
- `src/generate_masks.ipynb`
- `src/augmentations.ipynb`

---

### Prajwal
Responsible for the **baseline model and training pipeline**.

Completed work:
- metadata-based dataset loading
- 6-channel input creation using pre + post images
- baseline U-Net model setup
- baseline training pipeline
- checkpoint saving
- training logs and curves

Main notebook:
- `notebooks/02_prajwal_baseline_training_updated.ipynb`

Main outputs:
- `outputs/prajwal/`

---

### Saikiran
Responsible for the **evaluation stage**.

Completed work:
- validation and test evaluation
- IoU, Dice/F1, Precision, Recall, Accuracy
- prediction visualization
- confusion matrix
- evaluation summaries

Main notebook:
- `notebooks/03_saikiran_evaluation.ipynb`

Main outputs:
- `outputs/saikiran/`

---

### Divya
Responsible for the **improved model experiment**.

Completed work:
- improved model design using Attention U-Net
- training of improved model
- comparison against baseline
- improved-model logs and checkpoints

Main notebook:
- `notebooks/04_divya_improved_model.ipynb`

Main outputs:
- `outputs/divya/`

> Note: the improved model was explored and compared fairly. Under the current setup, it did not outperform the baseline on all major metrics, which is a valid experimental result.

---

### Reginald / Chimeka Praise
Responsible for the **comparison and error analysis stage**.

Completed work:
- baseline vs improved comparison
- per-sample analysis
- failure categorization
- error analysis visualizations
- final comparison figures and summaries

Main notebook:
- `notebooks/05_reginald_comparison_error_analysis.ipynb`

Main outputs:
- `outputs/reginald/`

---

## 3. What This Project Uses

### Input data
- pre-event satellite images
- post-event satellite images
- GeoJSON flood annotations

### Current implementation
The current implementation uses **optical RGB imagery** from pre-event and post-event images.

The training pipeline uses:
- 3 channels from pre-event image
- 3 channels from post-event image

Total model input:
- **6-channel input**

### Labels
The original flood annotations are polygon-based GeoJSON files.  
These are converted into **binary mask PNGs** so they can be used for semantic segmentation.

---

## 4. Folder Structure

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
│   ├── 01_data_inspection.ipynb
│   ├── 02_prajwal_baseline_training_updated.ipynb
│   ├── 03_saikiran_evaluation.ipynb
│   ├── 04_divya_improved_model.ipynb
│   └── 05_reginald_comparison_error_analysis.ipynb
├── outputs/
│   ├── inspection/
│   ├── augmentations/
│   ├── prajwal/
│   ├── saikiran/
│   ├── divya/
│   └── reginald/
├── src/
│   ├── preprocess_dataset.ipynb
│   ├── generate_masks.ipynb
│   └── augmentations.ipynb
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 5. What Each Folder Does

### `data/raw/`
Stores the original downloaded dataset:
- pre-event images
- post-event images
- annotation files
- mapping/reference CSV files

### `data/processed/`
Stores the model-ready dataset:
- split into `train`, `val`, and `test`
- each split has:
  - `pre/`
  - `post/`
  - `mask/`
- also contains `metadata.csv`

### `metadata.csv`
This is the **source of truth** for the whole project.

It stores:
- sample ID
- split
- pre image path
- post image path
- label path
- mask path
- mask generation status

### `notebooks/`
Stores the main notebooks used by each team member.

### `outputs/`
Stores generated results such as:
- inspection visuals
- augmentation previews
- training logs
- checkpoints
- evaluation metrics
- prediction images
- comparison charts
- error analysis outputs

### `src/`
Stores reusable preprocessing scripts created during the data-preparation stage.

### `docs/`
Stores supporting project notes and write-ups if needed.

---

## 6. Environment Setup

### Step 1 – Clone the repository
```bash
git clone https://github.com/rbt3601/flood_project.git
cd flood_project
```

### Step 2 – Create a virtual environment

#### Windows (Git Bash)
```bash
py -m venv .venv
source .venv/Scripts/activate
```

### Step 3 – Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 – Optional package check
```bash
python -c "import torch, rasterio, pandas, sklearn, seaborn; print('Environment OK')"
```

---

## 7. Step-by-Step: How to Run the Project

## Stage A – Data inspection
Open and run:

```text
notebooks/01_data_inspection.ipynb
```

What it does:
- checks the dataset structure
- reads mapping CSV
- creates valid pre/post/label pairs
- inspects image metadata
- inspects annotations
- generates preview images and overlays

Main outputs:
- `outputs/inspection/valid_pairs.csv`
- sample images
- overlays
- summary CSV files

---

## Stage B – Create the processed dataset split
Run from project root:

```bash
python src/preprocess_dataset.ipynb
```

What it does:
- reads `outputs/inspection/valid_pairs.csv`
- creates train / val / test split
- creates `data/processed/metadata.csv`
- creates processed split folders

---

## Stage C – Generate masks and processed files
Run from project root:

```bash
python src/generate_masks.ipynb
```

What it does:
- reads `data/processed/metadata.csv`
- copies matching pre/post images into processed split folders
- converts GeoJSON labels into binary mask PNG files
- updates metadata paths to point to processed files

Expected processed structure:
```text
data/processed/train/pre/sample_00000.tif
data/processed/train/post/sample_00000.tif
data/processed/train/mask/sample_00000.png
```

The same structure is used for `val` and `test`.

---

## Stage D – Generate augmentation previews
Run from project root:

```bash
python src/augmentations.ipynb
```

What it does:
- reads processed training rows from `metadata.csv`
- applies augmentations to image-mask pairs
- saves preview images to verify alignment

Main outputs:
- `outputs/augmentations/`
- `augmentation_preview_summary.csv`

---

## Stage E – Run baseline training
Open and run:

```text
notebooks/02_prajwal_baseline_training_updated.ipynb
```

What it does:
- reads `data/processed/metadata.csv`
- loads train and validation samples
- builds a 6-channel input using pre + post images
- trains a baseline U-Net
- saves checkpoints and training logs

Main outputs:
- `outputs/prajwal/checkpoints/`
- training history CSV
- loss curve

---

## Stage F – Run evaluation
Open and run:

```text
notebooks/03_saikiran_evaluation.ipynb
```

What it does:
- loads Prajwal’s trained checkpoint
- evaluates baseline model on validation and test data
- computes segmentation metrics
- saves visual results and summary files

Main outputs:
- `outputs/saikiran/metrics_summary.csv`
- prediction visuals
- confusion matrix
- evaluation charts

---

## Stage G – Run improved model experiment
Open and run:

```text
notebooks/04_divya_improved_model.ipynb
```

What it does:
- trains an improved model (Attention U-Net)
- compares improved model against the baseline
- saves improved checkpoints and logs

Main outputs:
- `outputs/divya/`
- comparison summary
- improved-model charts and logs

---

## Stage H – Run comparison and error analysis
Open and run:

```text
notebooks/05_reginald_comparison_error_analysis.ipynb
```

What it does:
- compares baseline vs improved results
- performs per-sample analysis
- categorizes failure cases
- generates final comparison figures and summary visuals

Main outputs:
- `outputs/reginald/`
- final comparison tables
- error analysis figures
- presentation-ready visuals

---

## 8. Recommended Execution Order

Run the project in this order:

1. `notebooks/01_data_inspection.ipynb`
2. `python src/preprocess_dataset.ipynb`
3. `python src/generate_masks.ipynb`
4. `python src/augmentations.ipynb`
5. `notebooks/02_prajwal_baseline_training_updated.ipynb`
6. `notebooks/03_saikiran_evaluation.ipynb`
7. `notebooks/04_divya_improved_model.ipynb`
8. `notebooks/05_reginald_comparison_error_analysis.ipynb`

---

## 9. Important Notes

- Always run from the **project root folder**
- Use only **project-relative paths**
- Do not hardcode personal laptop paths
- Use `data/processed/metadata.csv` as the source of truth
- If a notebook depends on another member’s outputs, run the earlier notebook first
- If packages are missing, install them inside the same virtual environment

---

## 10. Expected Outputs by Stage

### Rajesh outputs
- processed split structure
- `metadata.csv`
- masks
- inspection visuals
- augmentation previews

### Prajwal outputs
- baseline checkpoints
- training history
- baseline loss curve

### Saikiran outputs
- evaluation metrics
- prediction visuals
- confusion matrix
- test/validation summaries

### Divya outputs
- improved-model checkpoints
- improved training history
- baseline vs improved comparison

### Reginald outputs
- final comparison tables
- failure categories
- worst-case examples
- presentation-ready figures

---

## 11. Current Project Status

Completed:
- dataset setup
- data inspection
- valid pair creation
- processed dataset creation
- mask generation
- augmentation preview generation
- baseline training
- evaluation
- improved model experiment
- comparison and error analysis

Remaining coursework items outside the repo:
- final report
- final presentation video

---

## 12. Authors

- rbt3 – Rajesh Bennegere Theertheswara
- Prajwal
- Saikiran
- Divya
- Reginald / Chimeka Praise
