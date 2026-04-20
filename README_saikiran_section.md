## Saikiran - Model Evaluation and Predictions

### Work Completed by Saikiran

#### Evaluation of Baseline U-Net Model
Completed:
- loaded the trained U-Net baseline model checkpoint from Prajwal's training output
- implemented full evaluation pipeline on both validation and test splits
- computed IoU, Dice/F1, Precision, Recall, and Accuracy metrics using sklearn
- generated confusion matrices for both splits
- saved per-sample binary prediction masks as PNG files
- produced side-by-side visual comparisons of POST image, ground truth mask, and predicted mask
- generated per-image IoU distribution histograms
- saved full metrics summary as CSV

#### Evaluation Results

| Metric     | Validation | Test   |
|------------|------------|--------|
| IoU        | 0.3258     | 0.3138 |
| Dice/F1    | 0.4915     | 0.4777 |
| Precision  | 0.3842     | 0.3867 |
| Recall     | 0.6818     | 0.6246 |
| Accuracy   | 0.9825     | 0.9740 |

---

## How to Run – Saikiran Evaluation

### Prerequisite
Use `best_model.pth`  from
```text
outputs/prajwal/checkpoints/best_model.pth
```

Open and run:

```text
notebooks/saikiran_evaluation.ipynb
```

This notebook:
- loads the trained U-Net model from Prajwal's checkpoint
- reads `data/processed/metadata.csv` and uses the pre-defined val/test split
- evaluates the model on both validation (30 samples) and test (31 samples) splits
- computes all segmentation metrics per split
- saves prediction masks, visual comparisons, confusion matrices, and IoU distributions

### Inputs
```text
outputs/prajwal/checkpoints/best_model.pth
data/processed/metadata.csv
data/processed/val/pre/
data/processed/val/post/
data/processed/val/mask/
data/processed/test/pre/
data/processed/test/post/
data/processed/test/mask/
```

### Outputs saved in:
```text
outputs/saikiran/
```

Typical outputs:
- `metrics_summary.csv` — IoU, Dice, Precision, Recall, Accuracy for val and test
- `confusion_matrix.png` — confusion matrices for both splits
- `val_visual_comparisons.png` — POST image vs ground truth vs prediction (val)
- `test_visual_comparisons.png` — POST image vs ground truth vs prediction (test)
- `iou_distribution.png` — per-image IoU histogram for val and test
- `prediction_masks/` — per-sample binary prediction PNGs

---

## Model Performance Analysis

The baseline U-Net model achieves a Test IoU of **0.3138** and Dice/F1 of **0.4777**,
indicating moderate overlap between predicted and ground truth flood regions.

**Recall (0.6246)** is notably higher than **Precision (0.3867)**, meaning the model
successfully detects a large proportion of actual flood pixels but also produces
false positives — predicting flood in areas that are not flooded. This is a common
behaviour in baseline segmentation models trained on imbalanced datasets where
flood pixels are the minority class.

**Accuracy (0.9740)** is high but misleading — since the majority of pixels are
non-flood, even a model biased toward the background class will score highly on
accuracy. IoU and Dice are more meaningful metrics for this task.

**Validation vs Test consistency** — Val IoU (0.3258) and Test IoU (0.3138) are
close, indicating the model generalises reasonably and is not overfitted to the
validation split.

Overall, the baseline establishes a solid reference point. The higher recall
suggests the model is learning flood patterns, but precision needs improvement —
this is the motivation for the improved model (Divya's notebook).

---

## Important Notes
- The model checkpoint (`best_model.pth`) is not stored in the repository due to GitHub's 100MB file size limit.
- Request the checkpoint file from Prajwal via the shared Google Drive link.
- All paths are project-relative. Do not hardcode personal laptop paths.
- Run from the project root or from inside the `notebooks/` folder — the root is auto-detected.

---

## Author
- Saikiran – Model evaluation, metric computation, prediction mask generation, and visual analysis
