# Data Dictionary

*This document is a work in progress.*

## Mass Lists

Format: `CSV` (`.csv`)

| Column | Description | Unit |
|---|---|---|
| Structure | Structure code | NA |
| Monoisotopicmass | Monoisotopic mass | *TBD* |

## FTRS Input Files

Format: `.ftrs`

## MaxQuant Input Files

Format: `TSV` (`.txt`)

## FTRS Output Files

Format: `CSV` (`.csv`)

The column name of the first column contains [embedded metadata](#embedded-metadata) on the provenance of the file. Subsequent columns are defined as follows:

| Column | Description | Unit |
|---|---|---|
| ID | *TBD* | *TBD* |
| xicStart | *TBD* | *TBD* |
| xicEnd | *TBD* | *TBD* |
| feature | *TBD* | *TBD* |
| corrMax | *TBD* | *TBD* |
| ionCount | *TBD* | *TBD* |
| chargeOrder | *TBD* | *TBD* |
| maxIsotopeCount | *TBD* | *TBD* |
| rt | *TBD* | *TBD* |
| mwMonoisotopic | *TBD* | *TBD* |
| theo_mwMonoisotopic | *TBD* | *TBD* |
| inferredStructure | *TBD* | *TBD* |
| maxIntensity | *TBD* | *TBD* |

## MaxQuant Output Files

Format: `CSV` (`.csv`)

The column name of the first column contains [embedded metadata](#embedded-metadata) on the provenance of the file. Subsequent columns are defined as follows:

| Column | Description | Unit |
|---|---|---|
| ID | *TBD* | *TBD* |
| rt | *TBD* | *TBD* |
| rt_length | *TBD* | *TBD* |
| mwMonoisotopic | *TBD* | *TBD* |
| theo_mwMonoisotopic | *TBD* | *TBD* |
| inferredStructure | *TBD* | *TBD* |
| maxIntensity | *TBD* | *TBD* |

## Embedded Metadata

| Data | Description |
|---|---|
| file | Input data file |
| masses_file | Mass list file |
| modifications | List of modifications (*TBD*) |
| ppm | ppm tolerance (*TBD*) |
| rt_window | *TBD* |
