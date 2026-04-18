## 👤 Saikiran – Evaluation Module

### 📌 Role
Responsible for evaluating the trained U-Net model for flood damage segmentation.

---

### ⚙️ Work Done
- Loaded trained model (`best_model.pth`)
- Reconstructed U-Net architecture from training notebook
- Built evaluation pipeline using PyTorch
- Processed dataset (6-channel input: pre + post images)
- Implemented evaluation metrics:
  - IoU (Intersection over Union)
  - Dice Score
  - Precision
  - Recall
- Generated prediction outputs
- Visualized:
  - Input image
  - Ground truth mask
  - Predicted mask
- Saved results to `outputs/results.txt`

---

### 📊 Results (Baseline Model)
- IoU: ~0.07  
- Dice Score: ~0.13  
- Precision: ~0.08  
- Recall: ~0.47  

---

### How to Run – Saikiran – Evaluation Module
Open and run:

notebooks/saikiran_evaluation.ipynb

This will:

Load the trained model
Compute IoU, Dice, Precision, Recall
Display prediction results
Save metrics to:
outputs/results.txt

---

### 🚀 Notes
- Model uses 6-channel input (pre + post disaster images)
- Evaluation performed using dataset from `metadata.csv`
- Results highlight scope for further model optimization
