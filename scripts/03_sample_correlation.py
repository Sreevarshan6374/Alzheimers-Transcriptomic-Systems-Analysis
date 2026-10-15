import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(r"D:\Neurosys14")
PROCESSED = BASE / "data" / "processed"
FIGURES = BASE / "results" / "figures"

expression_file = PROCESSED / "GSE132903_expression_matrix.csv"
metadata_file = PROCESSED / "GSE132903_sample_metadata.csv"

print("Loading expression matrix...")

df = pd.read_csv(expression_file)
metadata = pd.read_csv(metadata_file)

sample_ids = metadata["sample_id"].tolist()
expression = df[sample_ids]

print("Expression matrix:", expression.shape)

print("Calculating Pearson correlations...")

correlation = expression.corr(method="pearson")

# Remove self-correlations when calculating mean correlation
mean_correlation = correlation.copy()

for sample in mean_correlation.index:
    mean_correlation.loc[sample, sample] = float("nan")

mean_correlation = mean_correlation.mean(axis=1).sort_values()

print()
print("Lowest mean-correlated samples:")
print()

for sample, value in mean_correlation.head(10).items():

    group = metadata.loc[
        metadata["sample_id"] == sample,
        "group"
    ].iloc[0]

    print(sample, group, round(value, 4))

# Save results
correlation.to_csv(
    PROCESSED / "GSE132903_sample_correlation.csv"
)

mean_correlation.to_csv(
    PROCESSED / "GSE132903_mean_sample_correlation.csv",
    header=["mean_correlation"]
)

# Heatmap
plt.figure(figsize=(12, 10))

plt.imshow(
    correlation.values,
    aspect="auto",
    interpolation="nearest"
)

plt.colorbar(label="Pearson correlation")

plt.title("GSE132903 Sample-to-Sample Correlation")
plt.xlabel("Samples")
plt.ylabel("Samples")

plt.tight_layout()

plt.savefig(
    FIGURES / "03_sample_correlation_heatmap.png",
    dpi=300
)

plt.close()

print()
print("Sample correlation analysis completed successfully.")