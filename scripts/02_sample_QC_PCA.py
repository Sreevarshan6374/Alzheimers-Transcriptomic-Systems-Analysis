import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.decomposition import PCA

# =========================
# Step 2 - Sample QC + PCA
# =========================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED = PROJECT_ROOT / "data" / "processed"
FIGURES = PROJECT_ROOT / "results" / "figures"

EXPRESSION_FILE = PROCESSED / "GSE132903_expression_matrix.csv"
METADATA_FILE = PROCESSED / "GSE132903_sample_metadata.csv"

FIGURES.mkdir(parents=True, exist_ok=True)

print("Loading processed expression matrix...")

df = pd.read_csv(EXPRESSION_FILE)
metadata = pd.read_csv(METADATA_FILE)

# -------------------------
# Extract expression values
# -------------------------

sample_ids = metadata["sample_id"].tolist()
expression = df[sample_ids]

print(f"Expression matrix: {expression.shape}")

# -------------------------
# Basic expression statistics
# -------------------------

sample_means = expression.mean(axis=0)
sample_medians = expression.median(axis=0)

print("\nSample mean range:")
print(sample_means.min(), "to", sample_means.max())

print("\nSample median range:")
print(sample_medians.min(), "to", sample_medians.max())

# -------------------------
# Expression distribution
# -------------------------

plt.figure(figsize=(12, 6))

plt.boxplot(
    expression.values,
    showfliers=False
)

plt.xlabel("Samples")
plt.ylabel("Normalized expression")
plt.title("GSE132903 Sample Expression Distributions")

plt.tight_layout()

plt.savefig(
    FIGURES / "01_sample_expression_distribution.png",
    dpi=300
)

plt.close()

# -------------------------
# Remove zero-variance probes
# -------------------------

probe_variance = expression.var(axis=1)
variable_mask = probe_variance > 0
expression_variable = expression.loc[variable_mask]

print(
    f"\nVariable probes: "
    f"{expression_variable.shape[0]} / {expression.shape[0]}"
)

# -------------------------
# PCA
# -------------------------

X = expression_variable.T

# Center features without scaling individual probes.
X_centered = X - X.mean(axis=0)

pca = PCA(n_components=10)
principal_components = pca.fit_transform(X_centered)

explained = pca.explained_variance_ratio_ * 100

print("\nPCA explained variance:")

for i, value in enumerate(explained[:5], start=1):
    print(f"PC{i}: {value:.2f}%")

# -------------------------
# PCA dataframe
# -------------------------

pca_df = pd.DataFrame(
    principal_components,
    columns=[f"PC{i}" for i in range(1, 11)]
)

pca_df["sample_id"] = sample_ids
pca_df["group"] = metadata["group"].values

# -------------------------
# PCA plot
# -------------------------

plt.figure(figsize=(9, 7))

for group in ["ND", "AD"]:

    subset = pca_df[pca_df["group"] == group]

    plt.scatter(
        subset["PC1"],
        subset["PC2"],
        label=group,
        alpha=0.7
    )

plt.xlabel(f"PC1 ({explained[0]:.2f}%)")
plt.ylabel(f"PC2 ({explained[1]:.2f}%)")
plt.title("GSE132903 PCA: Alzheimer's Disease vs Control")
plt.legend()

plt.tight_layout()

plt.savefig(
    FIGURES / "02_PCA_AD_vs_ND.png",
    dpi=300
)

plt.close()

# -------------------------
# Save PCA coordinates
# -------------------------

pca_df.to_csv(
    PROCESSED / "GSE132903_PCA_coordinates.csv",
    index=False
)

print("\nQC/PCA completed successfully.")
print(f"Figures saved to: {FIGURES}")