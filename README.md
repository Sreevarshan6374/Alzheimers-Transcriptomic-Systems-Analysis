# Systems-Level Analysis of Molecular Alterations in Alzheimer's Disease Using Transcriptomic Data

## Overview

NeuroSys14 is a transcriptomic analysis project investigating molecular alterations associated with Alzheimer's disease (AD). The project combines differential gene-expression analysis, sample-level quality control, functional enrichment, pathway analysis, and independent validation to identify biological patterns associated with disease.

The primary objective is to connect gene-expression changes with broader biological processes and develop evidence-based, testable hypotheses about Alzheimer's disease biology.

## Research Objectives

- Identify differentially expressed molecular features associated with Alzheimer's disease.
- Investigate biological processes and pathways enriched among altered genes.
- Integrate complementary pathway-analysis approaches to identify convergent biological signals.
- Examine potential relationships between transport processes and lipid metabolism.
- Distinguish discovery findings from results supported by independent validation.

## Dataset

**Primary dataset:** [GSE132903](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE132903)

The analysis uses the normalized expression matrix associated with this Gene Expression Omnibus (GEO) dataset.

- Platform: Illumina HumanHT-12 V4.0 expression beadchip (GPL10558)
- Alzheimer’s disease samples: 97
- Non-demented control samples: 98

The processed analysis matrix contains 195 samples. Dataset provenance and sample-level metadata should be consulted when interpreting the findings.

## Methodology

1. **Data preparation:** Process the normalized expression matrix and organize sample metadata.
2. **Quality control:** Assess sample-level expression characteristics, principal component analysis (PCA), and sample correlations.
3. **Differential expression:** Use the limma framework to identify differentially expressed features.
4. **Probe-to-gene processing:** Collapse probe-level results to gene-level summaries where appropriate.
5. **Functional interpretation:** Investigate Gene Ontology biological processes and Reactome pathways.
6. **Ranked pathway analysis:** Use gene-set enrichment analysis to examine coordinated pathway-level changes.
7. **Network and validation analysis:** Investigate leading-edge overlaps and assess whether selected findings reproduce in an independent dataset.

## Key Findings

### 1. Reduced synaptic and neuronal signalling programmes

Functional enrichment analyses consistently identify downregulated synaptic and neuronal processes, including synaptic vesicle transport, synaptic vesicle cycling, chemical synaptic transmission, and neurotransmitter signalling.

The convergence of GO enrichment, Reactome analysis, and ranked pathway analysis supports neuronal and synaptic dysfunction as a major signal in the discovery dataset.

### 2. Increased metal-response and stress-associated programmes

Upregulated genes show enrichment for metal-ion responses and metallothionein-associated processes. These results suggest altered metal handling or stress-response activity, although the analysis alone does not establish the underlying mechanism.

### 3. A hypothesis linking transport and lipid metabolism

Leading-edge analysis identified a potential connection between ABC-family transport and fatty-acid metabolism involving ABCD1.

This relationship is treated as a discovery-derived hypothesis rather than a confirmed disease mechanism.

### 4. Independent validation

The selected ABC-family transport and fatty-acid metabolism pathways did not achieve statistically significant pathway-level replication in the independent validation analysis. Independent gene-level validation of ABCD1 was also not established.

These limitations are retained in the interpretation rather than treating discovery results as independently confirmed findings.

## Statistical Analysis

Differential expression analysis used limma with the following criteria:

- Adjusted p-value < 0.05
- Absolute log2 fold change ≥ 0.5

The discovery analysis identified 939 significant probes and 737 gene-level results under the project's specified filtering and probe-collapsing procedures.

## Repository Structure

- `data/` — dataset-related files and processed data, subject to repository exclusions
- `notebooks/` — exploratory and analytical notebooks
- `results/` — analysis outputs, tables, and figures
- `scripts/` — scripts for data preparation, quality control, correlation analysis, probe collapsing, metadata retrieval, and integration

## Reproducibility

The repository includes analysis scripts and selected outputs to support transparency and reproducibility.

Before reproducing the analysis, review the relevant scripts, dataset access requirements, package dependencies, and input-file paths. Large input and processed dataset files may be excluded from Git and may need to be obtained or generated locally.

## Limitations

- Transcriptomic associations do not establish causation.
- Functional enrichment results depend on the input data, background gene set, and analysis settings.
- The transport–lipid hypothesis requires further independent investigation.
- Failure to replicate a pathway does not by itself prove that the biological process is irrelevant to Alzheimer's disease.

## Acknowledgements

This project uses publicly available transcriptomic data from the NCBI Gene Expression Omnibus.

## Author

**S. Sreevarshan**

Biotechnology undergraduate | Transcriptomics | Bioinformatics | Computational Biology
