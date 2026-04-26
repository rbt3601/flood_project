# Comparison and Error Analysis — Auto-Generated Summary

_Comparison and error analysis by Reginald. Baseline trained by Prajwal, evaluated by Saikiran. Improved model by Divya._

## Model Comparison

| Metric | Baseline (Val) | Baseline (Test) | Attention U-Net (Val) | Change |
|--------|---------------|----------------|----------------------|--------|
| IoU | 0.3377 | 0.3260 | 0.3891 | +0.0514 |
| Dice/F1 | 0.5049 | 0.4917 | 0.5602 | +0.0553 |
| Precision | 0.4129 | 0.4209 | 0.4824 | +0.0695 |
| Recall | 0.6496 | 0.5912 | 0.6679 | +0.0183 |
| Accuracy | 0.9842 | 0.9767 | 0.9870 | +0.0028 |

## Analysis

The Attention U-Net improved **Recall** from 0.6496 to 0.6679 (+0.0183), indicating it detects more flood pixels. However, **IoU** decreased slightly from 0.3377 to 0.3891, suggesting the attention mechanism increases sensitivity at the cost of some precision on this small dataset (141 train samples).

## Failure Case Analysis (Baseline, Test Split)

Total test samples scored: **31**

| Category | Count | Share | Description |
|----------|-------|-------|-------------|
| `correct_empty` | 11 | 35% | No flood in GT, model correctly predicts none (true negative scene) |
| `false_alarm` | 10 | 32% | Model predicts flood on a clean (empty GT) scene |
| `poor` | 5 | 16% | IoU < 0.30 with no specific pattern |
| `acceptable` | 5 | 16% | IoU in [0.30, 0.50) — mediocre but reasonable |

## Top Failure Modes and Suggested Fixes

1. **false_alarm** — Add more clean-scene training examples; raise decision threshold; use difference channel.
2. **poor** — Mix of the above — inspect qualitatively.

## Visuals

- `final_comparison_chart.png` — metric bar chart across all models
- `training_curves_comparison.png` — loss and IoU curves
- `failure_analysis/score_distributions.png` — IoU/precision/recall histograms
- `failure_analysis/category_counts.png` — failure category bar chart
- `failure_analysis/worst_cases.png` — worst prediction examples
- `failure_analysis/precision_recall_scatter.png` — P vs R coloured by category