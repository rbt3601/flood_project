from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALID_PAIRS_PATH = PROJECT_ROOT / "outputs" / "inspection" / "valid_pairs.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

TRAIN_DIR = PROCESSED_DIR / "train"
VAL_DIR = PROCESSED_DIR / "val"
TEST_DIR = PROCESSED_DIR / "test"

def to_rel_str(p):
    p = Path(p)
    try:
        return str(p.resolve().relative_to(PROJECT_ROOT.resolve())).replace("\\", "/")
    except Exception:
        return str(p).replace("\\", "/")

for split_dir in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
    (split_dir / "pre").mkdir(parents=True, exist_ok=True)
    (split_dir / "post").mkdir(parents=True, exist_ok=True)
    (split_dir / "mask").mkdir(parents=True, exist_ok=True)

df = pd.read_csv(VALID_PAIRS_PATH)
print("Loaded valid pairs:", len(df))

keep_cols = ["pre_path", "post_path", "label_path"]
df = df[keep_cols].copy()

for col in keep_cols:
    df[col] = df[col].apply(to_rel_str)

df["sample_id"] = [f"sample_{i:05d}" for i in range(len(df))]

train_df, temp_df = train_test_split(df, test_size=0.30, random_state=42, shuffle=True)
val_df, test_df = train_test_split(temp_df, test_size=0.50, random_state=42, shuffle=True)

train_df["split"] = "train"
val_df["split"] = "val"
test_df["split"] = "test"

final_df = pd.concat([train_df, val_df, test_df], ignore_index=True)
final_df = final_df[["sample_id", "split", "pre_path", "post_path", "label_path"]]

print("Train samples:", len(train_df))
print("Val samples:", len(val_df))
print("Test samples:", len(test_df))

metadata_path = PROCESSED_DIR / "metadata.csv"
final_df.to_csv(metadata_path, index=False)

print("Saved metadata to:", metadata_path)
print(final_df.head())