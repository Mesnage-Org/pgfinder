# Introduction

This package is a product of work undertaken by the [Mesnage Lab](https://mesnagelab.weebly.com/) to improve the
workflow for the analysis of bacterial peptidoglycans[[1]](#1)

~pgfinder~ automates the analysis pipeline of deconvoluted mass-spectroscopy data from <LAB MACHINE?> comparing peaks to
a database of candidate monomers to identify potential matches. These candidate monomers form the basis of theoretical
dimer and trimer masses which are in turn matched against possible candidates after determining possible
modifications. A more detailed overview of the workflow is provided in the [methods](#methods).

## Background

**FIXME** Background information on Peptidoglycan analysis. I've had a read of the Introduction to [[1]](#1) and think
it would serve as a good basis to go here, but am unsure how much detail to include.

## Methods

```{mermaid}
graph TD;

    A[Monomer Masses Database] --> C[Match monomers]
    B[Deconvoluted MS data] --> C([Match monomers -/+ ppm tolerance])
    C --> D[Matched theoretical monomer masses]
    D --> E([Calculate dimer & trimer masses])
    D --> I([Calculate modified monomers, dimers & trimers])
    D --> K([Match & annotate MS data -/+ ppm tolerance])
    E --> F[Theoretical dimer & trimer masses library]
    F --> G([Match dimers & trimers -/+ ppm tolerance])
    G --> H[Matched theoretical dimers & trimers masses]
    H --> I
    I --> J[Theoertical modified monomers, dimers & trimers masses library]
    J --> K
    K --> L[Raw matched MS data]
    L --> M([Consolidate in source decay products + salt adducts])
    M --> N[Processed MS data]
    N --> O([Write to CSV file])
    style A fill:#FFBB33,stroke:#000000
    style B fill:#FFBB33,stroke:#000000
    style C fill:#FFBB33,stroke:#000000
    style D fill:#FFBB33,stroke:#000000
    style E fill:#95FF80,stroke:#000000
    style F fill:#95FF80,stroke:#000000
    style G fill:#95FF80,stroke:#000000
    style H fill:#95FF80,stroke:#000000
    style I fill:#33BBFF,stroke:#000000
    style J fill:#33BBFF,stroke:#000000
    style K fill:#FF6666,stroke:#000000
    style L fill:#FF6666,stroke:#000000
    style M fill:#FF6666,stroke:#000000
    style N fill:#FF6666,stroke:#000000
    style O fill:#FF6666,stroke:#000000
```


## References

<a id="1">[1]</a> [PGFinder, a novel analysis pipeline for the consistent, reproducible, and high-resolution structural analysis of bacterial peptidoglycans | eLife](https://elifesciences.org/articles/70597)
