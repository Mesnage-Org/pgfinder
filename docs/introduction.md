# Introduction

This package is a product of work undertaken by the [Mesnage Lab](https://mesnagelab.weebly.com/) to improve the
workflow for the analysis of bacterial peptidoglycans [[1]](#1)

`PGFinder` automates the structural analysis of peptidoglycan LC-MS (Liquid Chromatography coupled to Mass Spectrometry) data. It compares  deconvoluted
masses from LC-MS datasets to a database of theoretical monoisotopic masses corresponding to monomeric peptidoglycan fragments. Matched monomers are then used to build more complex databases made of theoretical multimeric and modified structures, in turn matched against observed masses. A
detailed overview of the workflow is provided in the [methods](#methods).

## Background

Peptidoglycan is a ubiquitous and essential component of the bacterial cell envelope and its synthesis is the target of
beta-lactams, the most widely used antibiotics. Peptidoglycan fragments represent a key mediator during pathogenesis and
acute and chronic inflammation and their perception by the host contributes to the regulation of neurodevelopmental and
psychiatric disorders in animal models. Studying the structure and composition of peptidoglycan is therefore of
paramount importance to understand antibiotic resistance, chronic inflammatory diseases and neurodevelopmental and
psychiatric disorders.

Traditionally, peptidoglycan analysis involved a manual inspection of individual mass spectra to identify peptidoglycan
fragments based on their theoretical mass. PGFinder is an open-source Python package that can be run through a web
GUI or via the command line to perform an unbiased and automated analysis of LC-MS data. This enables a consistent and
reproducible workflow, opening new perspectives to develop "peptidoglycomics" as a new discipline.

## Methods

The identification of muropeptides was carried out using 4 successive steps, indicated by different colours (orange,
green, blue, red, respectively). As a first step, observed masses in the dataset are compared to a list of theoretical
masses corresponding to monomers. Matched masses within the ppm tolerance set (10ppm for Orbitrap data) are used to
build a list of inferred monomeric structures and their corresponding theoretical masses (database 1). This is then used
to generate a list of theoretical multimers (dimers and trimers) and their masses. A second matching round is carried
out to build a list of inferred multimers (database 2). At this stage, matched monomers and multimers are combined to
generate a list of modified muropeptides (database 3). Three databases of theoretical masses (monomers, dimers, trimers
and their modified counterparts) are used to search the dataset. Muropeptide structures are inferred from a match within
tolerance between theoretical and observed masses. This data is then “cleaned up” by combining the intensities of ions
corresponding to in-source decay and salt adducts to those of parent ions. The final matched MS data is then written to
a .csv file.

```{mermaid}

    graph TD;
        A[Monomer Masses Database] --> C[Match monomers]
        B[Deconvoluted MS data] --> C([Match monomers -/+ ppm tolerance])
        C --> D[DATABASE 1 Matched theoretical monomer masses]
        D --> E([Calculate dimer & trimer masses])
        D --> I([Calculate modified monomers, dimers & trimers])
        D --> K([Match & annotate MS data -/+ ppm tolerance])
        E --> F[DATABASE 2 Theoretical dimer & trimer masses library]
        F --> G([Match dimers & trimers -/+ ppm tolerance])
        G --> H[Matched theoretical dimers & trimers masses]
        H --> I
        I --> J[DATABASE 3 Theoertical modified monomers, dimers & trimers masses library]
        J --> K
        K --> L[Raw matched MS data]
        L --> M([Consolidate in source decay products + salt adducts])
        M --> N[Processed MS data]
        N --> O([Write to CSV file])
        style A fill:#FFBB33
        style B fill:#FFBB33
        style C fill:#FFBB33
        style D fill:#FFBB33
        style E fill:#95FF80
        style F fill:#95FF80
        style G fill:#95FF80
        style H fill:#95FF80
        style I fill:#FF6666
        style J fill:#FF6666
        style K fill:#33BBFF
        style L fill:#33BBFF
        style M fill:#33BBFF
        style N fill:#33BBFF
        style O fill:#33BBFF
```

## References

<a id="1">[1]</a> [PGFinder, a novel analysis pipeline for the consistent, reproducible, and high-resolution structural analysis of bacterial peptidoglycans | eLife](https://elifesciences.org/articles/70597)
