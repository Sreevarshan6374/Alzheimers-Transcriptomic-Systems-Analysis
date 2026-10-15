import pandas as pd
from pathlib import Path

# =========================
# NeuroSys14 - Step 5
# Integrate QC + GEO metadata
# =========================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED = PROJECT_ROOT / "data" / "processed"

pca_file = PROCESSED / "GSE132903_PCA_coordinates.csv"
corr_file = PROCESSED / "GSE132903_mean_sample_correlation.csv"
geo_file = PROCESSED / "GSE132903_GEO_metadata.csv"

# -------------------------
# Load files
# -------------------------

pca = pd.read_csv(pca_file)

corr = pd.read_csv(corr_file)
corr.columns = ["sample_id", "mean_correlation"]

geo = pd.read_csv(geo_file)

# -------------------------
# Recover sample ID
# -------------------------

geo["sample_id"] = (
    geo["title"]
    .str.replace("middle_temporal_gyrus_", "", regex=False)
)

# -------------------------
# Merge
# -------------------------

qc = pca.merge(
    corr,
    on="sample_id",
    how="left"
)

qc = qc.merge(
    geo,
    on="sample_id",
    how="left"
)

# -------------------------
# Integrity checks
# -------------------------

print("Integrated dataset shape:", qc.shape)

print("\nMissing metadata:")
print(qc[[
    "gsm",
    "tissue",
    "sex",
    "expired_age (years)",
    "diagnosis"
]].isna().sum())

print("\nDiagnosis:")
print(qc["diagnosis"].value_counts())

print("\nSex:")
print(qc["sex"].value_counts())

# -------------------------
# PCA distance
# -------------------------

qc["PC_distance"] = (
    qc["PC1"]**2 +
    qc["PC2"]**2
) ** 0.5

# -------------------------
# Show most extreme samples
# -------------------------

print("\nTop 15 PCA-extreme samples:")
print(
    qc.sort_values(
        "PC_distance",
        ascending=False
    )[[
        "sample_id",
        "diagnosis",
        "sex",
        "expired_age (years)",
        "PC1",
        "PC2",
        "mean_correlation",
        "PC_distance"
    ]]
    .head(15)
    .to_string(index=False)
)

# -------------------------
# Save
# -------------------------

output = PROCESSED / "GSE132903_integrated_QC_metadata.csv"

qc.to_csv(
    output,
    index=False
)

print("\nSaved:")
print(output)