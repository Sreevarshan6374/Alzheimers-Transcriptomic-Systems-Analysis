import GEOparse
import pandas as pd
from pathlib import Path

# =========================
# NeuroSys14 - Step 4
# Download GSE132903 metadata
# =========================

BASE = Path(r"D:\Neurosys14")
PROCESSED = BASE / "data" / "processed"

print("Downloading GSE132903 metadata from GEO...")

gse = GEOparse.get_GEO(
    geo="GSE132903",
    destdir=str(PROCESSED),
    silent=False
)

print("GEO dataset loaded.")

records = []

for gsm_name, gsm in gse.gsms.items():

    metadata = {
        "gsm": gsm_name,
        "title": gsm.metadata.get("title", [""])[0]
    }

    characteristics = gsm.metadata.get("characteristics_ch1", [])

    for item in characteristics:

        if ":" in item:

            key, value = item.split(":", 1)

            key = key.strip().lower()
            value = value.strip()

            metadata[key] = value

    records.append(metadata)

metadata_df = pd.DataFrame(records)

output = PROCESSED / "GSE132903_GEO_metadata.csv"

metadata_df.to_csv(
    output,
    index=False
)

print()
print("Metadata saved to:")
print(output)

print()
print("Number of GEO samples:")
print(len(metadata_df))

print()
print("Metadata columns:")
print(metadata_df.columns.tolist())