## Reginald - Failure-Case Analysis

### Work Completed by Reginald

#### Failure-case analysis of the baseline U-Net
Completed:
- consumed Saikiran's per-sample prediction PNGs from
  `outputs/saikiran/prediction_masks/` (no re-training, no re-running of
  inference)
- evaluated predictions at the same 256×256 resolution used by the baseline
  model (ground-truth masks are resized to match, with nearest-neighbour
  interpolation so labels are preserved)
- re-derived pixel-level metrics (IoU, Dice, Precision, Recall, Accuracy,
  Boundary-IoU) per test sample and cross-checked the micro-averaged
  numbers against Saikiran's `metrics_summary.csv`
- categorised each test sample into one of 11 failure / quality buckets
  (`no_gt_with_fp`, `missed_detection`, `over_segmentation`,
  `under_segmentation`, `small_object_miss`, `fragmented_prediction`,
  `boundary_error`, `poor`, `acceptable`, `good`, `correct_empty`)
- produced a 5-panel figure per test sample (pre / post / GT overlay /
  prediction overlay / TP-FP-FN error map)
- produced grid figures of the N worst samples and of the top samples
  per failure category, for direct inclusion in the report
- auto-generated a written summary (`summary.md`) that maps each dominant
  failure mode to a concrete fix for Divya's improved-model iteration

#### Findings (to be written into the report)

Saikiran's headline numbers already indicate the failure profile:

| Metric     | Test   |
|------------|--------|
| IoU        | 0.3138 |
| Dice / F1  | 0.4777 |
| Precision  | 0.3867 |
| Recall     | 0.6246 |
| Accuracy   | 0.9740 |

`Recall` is ~62% while `Precision` is ~39% — the baseline **over-predicts**
flood pixels. The categorisation step therefore expects
`over_segmentation` and `no_gt_with_fp` to dominate, with some
`boundary_error` on otherwise-well-localised scenes. The notebook produces
the exact breakdown and writes the concrete examples that back up this
claim.

---

## How to Run – Reginald Failure-Case Analysis

### Prerequisites
Saikiran's evaluation must have been run first so that the prediction
masks are on disk:

```text
outputs/saikiran/prediction_masks/sample_XXXXX_pred.png
```

If the checkpoint is not on disk yet, obtain `best_model.pth` from the
shared Google Drive (see Saikiran's section), drop it into
`outputs/prajwal/checkpoints/`, and run `saikiran_evaluation.ipynb` once.

Open and run:

```text
notebooks/reginald_failure_analysis.ipynb
```

This notebook:
- reads `data/processed/metadata.csv` and filters the `test` split
- loads each prediction from `outputs/saikiran/prediction_masks/`
- resizes ground-truth masks to 256×256 (nearest-neighbour) to match
  Saikiran's prediction resolution
- computes per-sample and aggregate metrics
- cross-checks aggregate metrics against Saikiran's `metrics_summary.csv`
- categorises each sample into a failure / quality bucket
- saves all figures and the auto-generated summary under
  `outputs/reginald/failure_analysis/`

### Inputs
```text
data/processed/metadata.csv
data/processed/test/pre/
data/processed/test/post/
data/processed/test/mask/
outputs/saikiran/prediction_masks/
outputs/saikiran/metrics_summary.csv     # used for cross-check (optional)
```

### Outputs saved in:
```text
outputs/reginald/failure_analysis/
```

Typical outputs:
- `per_sample_metrics.csv` — IoU, Dice, Precision, Recall, area stats, category (one row per test sample)
- `aggregate_metrics.json` — mean / median / micro-averaged scores + cross-check against Saikiran
- `confusion_matrix.png` — pixel-level confusion matrix (test, micro)
- `score_distributions.png` — per-sample IoU / Dice / Precision / Recall histograms
- `category_counts.png` — number of samples per failure / quality category
- `cases/sample_XXXXX.png` — 5-panel figure per test sample (pre, post, GT, pred, error map)
- `grids/worst_by_iou.png` — grid of the N worst samples on the test split
- `grids/category_<name>.png` — grid of up to 6 representative samples per failure category
- `summary.md` — auto-generated written summary to paste into the group report

---

## Methodology

Full methodology, metric definitions, failure-category rules, and
interpretation guide live in:

```text
docs/failure_analysis.md
```

Short version: each test sample receives a single **primary failure label**
from a first-match-wins rule stack (thresholds exposed in one config cell
of the notebook). Rules are ordered from most-specific-symptom to
least-specific:

```text
no_gt_with_fp → missed_detection → over_segmentation →
under_segmentation → small_object_miss → fragmented_prediction →
boundary_error → good / acceptable / poor / correct_empty
```

The error map uses `TP = green`, `FP = red`, `FN = blue` with the
post-event image passing through in the true-negative regions.

---

## Important Notes
- **No training or re-inference is performed here.** The notebook only
  reads existing prediction PNGs.
- If Saikiran's prediction resolution changes (e.g. Divya's improved model
  uses a different `IMG_SIZE`), update `EVAL_SIZE` in the notebook's
  configuration cell to match.
- If a future model saves **soft probability maps** instead of binary
  PNGs, the notebook auto-detects this and uses `PROB_THRESHOLD` — no
  code changes required.
- All paths are project-relative. Run from the project root or from
  inside the `notebooks/` folder — the root is auto-detected.
- Outputs are written under `outputs/reginald/`, which is gitignored (same
  as `outputs/prajwal/` and `outputs/saikiran/`).

---

## Author
- Reginald – Failure-case analysis, per-sample metric computation,
  failure categorisation, qualitative examples, and auto-generated summary.
