# Failure-Case Analysis

## Purpose

This step reviews the baseline U-Net's **prediction failures** on the
held-out test split and groups them into a small set of recurring
**segmentation mistakes**, each illustrated with concrete examples. The
goal is to explain *where* and *why* the current baseline is wrong, so the
next modelling iteration (Divya's improved model) can target the right
weakness.

The analysis is implemented as a single notebook:

```text
notebooks/reginald_failure_analysis.ipynb
```

It is **purely an evaluation step**, it does not train, re-train, or re-run  
inference. It consumes the per-sample prediction masks already produced by  
Saikiran's evaluation notebook.

---

## Inputs

The notebook expects three things to already exist on disk:

1. `data/processed/metadata.csv` — produced by the preprocessing step.
2. The processed test split:
  ```text
   data/processed/test/pre/sample_XXXXX.tif
   data/processed/test/post/sample_XXXXX.tif
   data/processed/test/mask/sample_XXXXX.png    # ground-truth mask
  ```
3. Model predictions from Saikiran's notebook:
  ```text
   outputs/saikiran/prediction_masks/sample_XXXXX_pred.png
  ```
   — one binary PNG per test sample, saved at `IMG_SIZE × IMG_SIZE`
   (256×256 by default).

### Resolution handling

The baseline model was trained and evaluated at **256×256**, and
Saikiran's prediction PNGs are therefore 256×256. Ground-truth masks on
disk are at the **original raster resolution** (≈1300×1300 for SpaceNet-8
tiles). For a fair comparison this notebook:

1. loads the 256×256 prediction as-is, and
2. resizes the ground-truth mask down to 256×256 with **nearest-neighbour**
  interpolation (so label values are preserved).

Visual panels use the post-event image downsampled to the same 256×256
grid, so every overlay lines up pixel-for-pixel with the prediction.

### Prediction PNG format

The PNGs are written by Saikiran's pipeline as `(pred > 0.5) * 255`, so the
values are `{0, 255}`. The notebook also auto-handles:


| Format          | Pixel values                         | Threshold used      |
| --------------- | ------------------------------------ | ------------------- |
| Binary mask     | `{0, 255}` (or `{0, 1}`)             | `> 0`               |
| Probability map | `0..255` grayscale (soft prediction) | `>= PROB_THRESHOLD` |


so if the next modelling iteration decides to save soft probabilities
instead of binary masks, the same notebook still works.

---

## Metrics

Per test sample, the notebook computes a pixel-level confusion matrix and
derives:

- **IoU** (Jaccard) — primary ranking metric
- **Dice** (F1)
- **Precision** (TP / (TP + FP))
- **Recall**    (TP / (TP + FN))
- **Pixel accuracy**
- **Prediction area fraction** and **GT area fraction**
- **Boundary-IoU** — IoU restricted to a 3-pixel-wide boundary band, used
to separate *boundary errors* from *area errors*
- **Number of connected components** in GT and in prediction

Aggregate scores on the test split:

- mean / median IoU / Dice / precision / recall
- micro-averaged pixel confusion matrix (TP / FP / FN / TN)
- per-sample score-distribution histograms

These numbers are cross-checked against the headline figures already
reported by Saikiran (Test IoU 0.3138, Dice 0.4777, Precision 0.3867,
Recall 0.6246) to catch any accidental pipeline drift.

---

## Failure Categorisation

Each test sample is assigned **one primary label** by the following rules,
evaluated top-to-bottom (first match wins). All thresholds are exposed in
a single config cell at the top of the notebook and can be tuned without
hunting through code.


| Label                   | Rule (defaults)                                                              |
| ----------------------- | ---------------------------------------------------------------------------- |
| `no_gt_with_fp`         | GT is empty **and** prediction has positives (hallucination on clean scenes) |
| `correct_empty`         | GT is empty **and** prediction is empty (true negative scene; not a failure) |
| `missed_detection`      | GT has positives **and** recall < 0.05 (model saw nothing)                   |
| `over_segmentation`     | `pred_area ≥ 3 × gt_area` **and** precision < 0.4                            |
| `under_segmentation`    | `pred_area ≤ 0.33 × gt_area` **and** recall < 0.5                            |
| `small_object_miss`     | GT contains only small components (mean area < 200 px) and recall < 0.3      |
| `fragmented_prediction` | prediction has > 3× more connected components than GT and IoU < 0.5          |
| `boundary_error`        | IoU ∈ [0.4, 0.7] **and** boundary-IoU noticeably worse than mask-IoU         |
| `good`                  | IoU ≥ 0.7                                                                    |
| `acceptable`            | IoU ∈ [0.4, 0.7]                                                             |
| `poor`                  | IoU < 0.4 and no more specific pattern matched                               |


Given the baseline's reported behaviour (high recall, low precision, heavy
over-prediction), we expect the dominant categories on the test split to
be `**over_segmentation`** and `**no_gt_with_fp**`, with some
`**boundary_error**` cases on the well-localised scenes.

---

## Visual outputs

All figures are written under:

```text
outputs/reginald/failure_analysis/
├── per_sample_metrics.csv          # one row per test sample
├── aggregate_metrics.json          # mean/median/micro scores + cross-check
├── confusion_matrix.png
├── score_distributions.png
├── category_counts.png
├── cases/
│   └── sample_XXXXX.png            # 5-panel figure per sample
├── grids/
│   ├── worst_by_iou.png
│   ├── category_over_segmentation.png
│   ├── category_no_gt_with_fp.png
│   └── ...
└── summary.md                      # auto-generated written summary
```

### Per-sample 5-panel figure

For every scored sample a single PNG is produced with:

1. Pre-event RGB (percentile-stretched to 2–98%)
2. Post-event RGB (percentile-stretched to 2–98%)
3. Ground truth overlaid on the post-event image
4. Prediction overlaid on the post-event image
5. **Error map** — `TP = green`, `FP = red`, `FN = blue`, `TN = pass-through`

### Category grids

For every failure category one grid image is produced showing up to 6
representative samples (sorted by IoU ascending — most instructive first),
so the report can drop them in directly.

---

## How to run

1. Make sure Prajwal's preprocessing has been completed (test masks exist
  under `data/processed/test/mask/`).
2. Make sure Saikiran's evaluation has been run so that the prediction
  PNGs exist under `outputs/saikiran/prediction_masks/`. If not:
  - request the checkpoint `best_model.pth` from the shared Google Drive
  and drop it into `outputs/prajwal/checkpoints/`,
  - then run `saikiran_evaluation.ipynb` (it will populate
  `outputs/saikiran/prediction_masks/`).
3. Open and run:
  ```text
   notebooks/reginald_failure_analysis.ipynb
  ```
4. Read `outputs/reginald/failure_analysis/summary.md` and include the
  generated figures in the group report.

---

## Interpreting results in the report

When writing up the failure-case section, use this structure:

1. **Cross-check** with Saikiran's headline numbers (mean IoU / Dice) so
  the reader can trust the analysis is measuring the same thing.
2. **Score distribution** — point out the left tail of the IoU histogram;
  that is where the failure cases live.
3. **Category breakdown** — highlight the *two or three* most frequent
  failure modes from `category_counts.png`.
4. **Concrete examples** — pick one representative grid per dominant
  category from `grids/` and walk through *why* the model failed
   (cloud / shadow confusion, small buildings, thin roads, river vs.
   flood discrimination, etc.).
5. **Recommendations for Divya's improved model** — each frequent failure
  mode in the auto-generated summary already carries a suggested fix
   (e.g. class re-weighting, targeted augmentation, boundary loss, higher
   input resolution). Tighten those and cite them as motivation for the
   next iteration.

