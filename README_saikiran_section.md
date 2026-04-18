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

`notebooks/saikiran_evaluation.ipynb`

This will:

Load the trained model
Compute IoU, Dice, Precision, Recall
Display prediction results
Save metrics to:
`outputs/results.txt`

---

### Typical outputs:

results.txt — IoU, Dice, Precision, Recall values  
visual outputs — prediction vs ground truth (displayed in notebook)  

---

### Evaluation Details

Model: U-Net (same as training)  
Input: 6 channels (PRE + POST images)  
Output: 1-channel binary segmentation mask  

Metrics used:

- IoU (Intersection over Union) — measures overlap between prediction and ground truth  
- Dice Score — measures similarity between predicted and actual flood regions  
- Precision — measures correctness of predicted flood pixels  
- Recall — measures ability to detect actual flood regions  

Threshold: 0.5 applied on sigmoid output  

---

### Important Notes

The evaluation uses the same dataset structure and split as defined in metadata.csv  
The model checkpoint must exist before running evaluation  
The U-Net architecture must match the training model exactly  
All paths are project-relative  

---

### Author

Saikiran – Evaluation pipeline, metrics computation, visualization, and analysis
