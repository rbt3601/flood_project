## Prajwal - Baseline Model and Training

### Work Completed by Prajwal

#### Baseline U-Net Segmentation Model
Completed:
- built a U-Net segmentation model with 6-channel input (PRE + POST satellite image concatenated)
- implemented combined BCE + Dice loss for handling class imbalance in flood pixels
- trained the baseline model for 30 epochs using the pre-defined train/val split from metadata.csv
- saved best model checkpoint based on validation loss
- saved final model checkpoint after all epochs
- generated loss curves (train loss, val loss, validation IoU per epoch)
- saved full training log as CSV

#### Training Results
- Model: U-Net (6-channel input, binary flood mask output)
- Parameters: 31,039,361
- Epochs: 30
- Best Val Loss: 1.0160
- Best Val IoU: 0.3199

---

## How to Run – Prajwal Baseline Training

Open and run:

```text
notebooks/prajwal_baseline_training.ipynb
```

This notebook:
- reads `data/processed/metadata.csv`
- loads PRE and POST GeoTIFF images and binary flood masks
- builds a 6-channel PyTorch Dataset and DataLoader using the pre-defined train/val split
- defines and trains a U-Net baseline segmentation model
- saves best and final model checkpoints
- saves loss curves and training log

### Inputs
```text
data/processed/metadata.csv
data/processed/train/pre/
data/processed/train/post/
data/processed/train/mask/
data/processed/val/pre/
data/processed/val/post/
data/processed/val/mask/
```

### Outputs saved in:
```text
outputs/prajwal/
```

Typical outputs:
- `checkpoints/best_model.pth` — best model by validation loss
- `checkpoints/final_model.pth` — model after all 30 epochs
- `loss_curve.png` — train/val loss and IoU curves
- `training_log.csv` — per-epoch metrics

---

## Model Architecture

The baseline model is a standard **U-Net** with:
- 4 encoder levels: 64 → 128 → 256 → 512 channels
- Bottleneck: 1024 channels
- Skip connections between encoder and decoder
- Final 1×1 convolution to binary logit output
- Input: 6 channels (3-band PRE + 3-band POST concatenated)
- Output: 1 channel binary flood mask (sigmoid applied at inference)

Loss function: **BCE + Soft Dice** (handles flood pixel class imbalance)  
Optimiser: **Adam** (lr=1e-4) with ReduceLROnPlateau scheduler

---

## Important Notes
- The notebook uses the `split` column in `metadata.csv` directly — no re-splitting is done.
- All paths are project-relative. Do not hardcode personal laptop paths.
- Run from the project root or from inside the `notebooks/` folder — the root is auto-detected.
- Training on CPU takes approximately 180 seconds per epoch (30 epochs ≈ 90 minutes).
- The saved `best_model.pth` checkpoint is intended for use by Saikiran's evaluation notebook.

---

## Author
- Prajwal – Baseline model design, training, and checkpoint generation
