\# Running the NeuroSys14 Analysis



\## Overview



NeuroSys14 analyzes transcriptomic data from Alzheimer's disease (AD) and non-demented (ND) samples using the GEO dataset GSE132903.



The Python scripts cover expression-matrix preparation, sample quality control, principal component analysis (PCA), sample correlation, probe-to-gene processing, GEO metadata retrieval, and QC metadata integration.



\## Requirements



\- Python 3.10 or later recommended

\- Packages listed in `requirements.txt`

\- The original GSE132903 normalized expression Excel file



Install the dependencies from the repository root:



```bash

python -m pip install -r requirements.txt

```



\## Required input data



Place the original Excel file at:



`data/raw/GSE132903\_Matrix\_Normalized.xlsx`



The Excel workbook must contain the sheet `Matrix normalized`.



This raw file is excluded from the Git repository because of its size. Obtain it from the original GEO dataset or the project's original data source before running the preparation script.



The probe annotation file required by the probe-collapsing script is:



`data/processed/GSE132903\_probe\_annotation.csv`



The repository also contains `data/processed/GPL10558\_probe\_annotation.csv`. Confirm that the expected annotation file is available before running probe collapsing.



\## Running the scripts



Run commands from the repository root.



\### 1. Prepare the expression matrix



```bash

python scripts/01\_prepare\_GSE132903.py

```



Expected outputs:



\- `data/processed/GSE132903\_sample\_metadata.csv`

\- `data/processed/GSE132903\_expression\_matrix.csv`



The script checks for 195 samples: 97 AD and 98 ND.



\### 2. Run sample QC and PCA



```bash

python scripts/02\_sample\_QC\_PCA.py

```



This script uses the prepared expression matrix and sample metadata. It generates PCA/QC outputs in the processed-data and figures directories.



\### 3. Calculate sample correlations



```bash

python scripts/03\_sample\_correlation.py

```



Expected outputs include:



\- `data/processed/GSE132903\_sample\_correlation.csv`

\- `data/processed/GSE132903\_mean\_sample\_correlation.csv`

\- A sample-correlation figure under `results/figures/`



\### 4. Download GEO metadata



```bash

python scripts/04\_download\_GEO\_metadata.py

```



This step connects to GEO and downloads the GSE132903 metadata using GEOparse.



Expected output:



\- `data/processed/GSE132903\_GEO\_metadata.csv`



An internet connection is required.



\### 5. Collapse probes to gene-level expression



```bash

python scripts/04\_collapse\_probes.py

```



This step requires the prepared expression matrix and probe annotation file.



Expected outputs:



\- `data/processed/GSE132903\_gene\_expression\_matrix.csv`

\- `data/processed/GSE132903\_probe\_selection.csv`



\### 6. Integrate QC and GEO metadata



```bash

python scripts/05\_integrate\_QC\_metadata.py

```



This step requires the PCA coordinates, mean sample correlations, and downloaded GEO metadata.



Expected output:



\- `data/processed/GSE132903\_integrated\_QC\_metadata.csv`



\## Output directories



\- `data/processed/` — prepared matrices, annotations, metadata, and QC tables

\- `results/figures/` — generated figures



\## Reproducibility notes



\- Run commands from the repository root.

\- Some input datasets are excluded from GitHub because of their size.

\- GEO metadata retrieval requires an internet connection.

\- The repository's Python scripts document the Python preprocessing and QC workflow. Any downstream differential-expression, enrichment, GSEA, or independent-validation analyses that rely on separate R scripts or other tools must be run separately according to their own instructions.

\- Check each script's input paths and output filenames if the pipeline is modified.



