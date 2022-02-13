# Data Dictionary

*This document is a work in progress.*

## Mass Lists

Format: `CSV` (`.csv`)

| Column | Description | Unit |
|---|---|---|
| Structure | Structure code | NA |
| Monoisotopicmass | Monoisotopic mass | atomic mass unit |

## FTRS Input Files

Format: `.ftrs`

## MaxQuant Input Files

Format: `TSV` (`.txt`)

## FTRS Output Files

Format: `CSV` (`.csv`)

The column name of the first column contains [embedded metadata](#embedded-metadata) on the provenance of the file. Subsequent columns are defined as follows:

| Column | Description | Unit |
|---|---|---|
| ID | Feature identified from ions corresponding to the same mass and retention time | NA |
| xicStart | Extracted ion chromatogram starting time point | min |
| xicEnd | Extracted ion chromatogram starting time point | min |
| ionCount | Number of occurrence for ions corresponding to the same feature | NA |
| chargeOrder | Observed ion charge states | NA |
| rt | Retention time | min |
| mwMonoisotopic | Observed monoisotopic mass | Da |
| theo_mwMonoisotopic | Theoretical monoisotopic mass | Da |
| inferredStructure | Inferred muropeptide structure | NA |
| maxIntensity | Signal intensity calculated from Extracted Ion Chromatograms | NA |

## MaxQuant Output Files

Format: `CSV` (`.csv`)

The column name of the first column contains [embedded metadata](#embedded-metadata) on the provenance of the file. Subsequent columns are defined as follows:

| Column | Description | Unit |
|---|---|---|
| ID | Feature identified from ions corresponding to the same mass and retention time | NA |
| rt | Retention time | min |
| rt_length | Time window used to quantify signal intensity based on Extracted Ion Chromatograms | min |
| mwMonoisotopic | Observed monoisotopic mass | Da |
| theo_mwMonoisotopic | Theoretical monoisotopic mass | Da |
| inferredStructure | Inferred muropeptide structure | NA |
| maxIntensity | Signal intensity calculated from Extracted Ion Chromatograms  | NA |

## Embedded Metadata

| Data | Description |
|---|---|
| file | Input data file |
| masses_file | Mass list file |
| modifications | *See below* |
| ppm | ppm tolerance |
| rt_window | Window used for in-source decay correction (min) |

| Modification | Description |
|---|---|
| Sodium	| Search for masses corresponding to sodium adducts |
| Potassium	| Search for masses corresponding to potassium adducts |
| Anh	| Search for anhydromuropeptides |
| DeAc	| Search for deacetylated muropeptides |
| DeAc_Anh	| Search for deacetylated anhydromuropeptides | 
| Nude	| Search for muropeptides with an extra GlcNAc-MurNAc disaccharide |
| Decay	| Correct output taking into account in-source decay products |
| Amidation | Search for Amidated muropeptides |
| Amidase	| Search for peptides resulting from amidase cleavage (GlcNAc-MurNAc loss) |
| Double Anh	| Search for anhydromuropeptides (2 Anhydro groups) |
| Multimers	| Search for multimers resulting from 3-3 and 4-3 crosslinks |
| Multimers | Glyco	Search for multimers resulting from transglycosylation (no transpeptidation |
|Multimer Lac	| Search for lactyl-peptides multimers |
|O-Ac	| Search for O-acetylated muropeptides |