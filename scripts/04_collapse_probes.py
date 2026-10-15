import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED = PROJECT_ROOT / "data" / "processed"

EXPR_FILE = PROCESSED / "GSE132903_expression_matrix.csv"
ANN_FILE = PROCESSED / "GSE132903_probe_annotation.csv"

OUT_EXPR = PROCESSED / "GSE132903_gene_expression_matrix.csv"
OUT_MAP = PROCESSED / "GSE132903_probe_selection.csv"

print("Loading expression matrix...")
expr = pd.read_csv(EXPR_FILE)

print("Expression matrix:", expr.shape)

# Identify the probe and sample columns
probe_col = "Illumina probe name"
sample_cols = [c for c in expr.columns if c not in ["ID_REF", probe_col]]

# Load annotation
print("Loading probe annotation...")
ann = pd.read_csv(ANN_FILE)

# Keep only required annotation columns
ann = ann[["probe_id", "gene_symbol"]].copy()

# Remove missing gene symbols
ann = ann.dropna(subset=["gene_symbol"])

# Convert probe IDs to strings for safe matching
expr[probe_col] = expr[probe_col].astype(str)
ann["probe_id"] = ann["probe_id"].astype(str)

# Merge expression with annotation
merged = expr.merge(
    ann,
    left_on=probe_col,
    right_on="probe_id",
    how="inner"
)

print("Annotated expression matrix:", merged.shape)

# Calculate variance for each probe
print("Calculating probe variance...")

merged["probe_variance"] = merged[sample_cols].var(axis=1)

# Select highest-variance probe for each gene
print("Selecting highest-variance probe per gene...")

selected = (
    merged.sort_values(
        ["gene_symbol", "probe_variance"],
        ascending=[True, False]
    )
    .drop_duplicates(subset="gene_symbol", keep="first")
    .copy()
)

print("Unique genes:", selected["gene_symbol"].nunique())

# Create gene-level expression matrix
gene_expr = selected[["gene_symbol"] + sample_cols].copy()

# Set gene symbol as index
gene_expr = gene_expr.set_index("gene_symbol")

# Save gene expression matrix
gene_expr.to_csv(OUT_EXPR)

# Save probe-selection record
selection = selected[
    ["gene_symbol", probe_col, "probe_variance"]
].copy()

selection.columns = [
    "gene_symbol",
    "selected_probe",
    "probe_variance"
]

selection.to_csv(OUT_MAP, index=False)

print()
print("Gene-level matrix:", gene_expr.shape)
print("Saved:")
print(OUT_EXPR)
print(OUT_MAP)
print()
print("Probe collapsing completed successfully.")