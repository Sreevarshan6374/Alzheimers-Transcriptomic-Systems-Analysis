import pandas as pd
from pathlib import Path

# =========================
# Step 1 - Load and structure GSE132903
# =========================

# Project root = parent directory of /scripts
PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "GSE132903_Matrix_Normalized.xlsx"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

print("Loading GSE132903...")

df = pd.read_excel(
    RAW_FILE,
    sheet_name="Matrix normalized"
)

print(f"Raw matrix shape: {df.shape}")

# -------------------------
# Identify columns
# -------------------------

probe_id_col = "ID_REF"
probe_name_col = "Illumina probe name"

sample_columns = list(df.columns[2:])

# -------------------------
# Create sample metadata
# -------------------------

metadata = pd.DataFrame({
    "sample_id": sample_columns
})

metadata["group"] = (
    metadata["sample_id"]
    .str.extract(r"^(AD|ND)_")[0]
)

# -------------------------
# Integrity checks
# -------------------------

assert len(sample_columns) == 195
assert metadata["group"].value_counts()["AD"] == 97
assert metadata["group"].value_counts()["ND"] == 98
assert metadata["group"].notna().all()

print("\nSample counts:")
print(metadata["group"].value_counts())

# -------------------------
# Extract expression matrix
# -------------------------

expression = df[
    [probe_id_col, probe_name_col] + sample_columns
].copy()

# -------------------------
# Save processed files
# -------------------------

metadata_file = PROCESSED_DIR / "GSE132903_sample_metadata.csv"
expression_file = PROCESSED_DIR / "GSE132903_expression_matrix.csv"

metadata.to_csv(metadata_file, index=False)
expression.to_csv(expression_file, index=False)

print("\nSaved:")
print(metadata_file)
print(expression_file)

print("\nStep 1 completed successfully.")