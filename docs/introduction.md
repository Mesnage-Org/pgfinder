# Introduction

This package is a product of work undertaken by the [Mesnage Lab](https://mesnagelab.weebly.com/) to improve the
workflow for the analysis of bacterial peptidoglycans[[1]](#1)

**FIXME** : Write an introductory overview of what pgfinder does and how it works.

## Background

**FIXME** Background information on Peptidoglycan analysis.

## Methods

**FIXME** Mermaid diagram doesn't render when Sphinx documentation is built on GitHub.

``` mermaid
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
    style A fill:#914800,stroke:#000000
    style B fill:#914800,stroke:#000000
    style C fill:#914800,stroke:#000000
    style D fill:#914800,stroke:#000000
    style E fill:#009110,stroke:#000000
    style F fill:#009110,stroke:#000000
    style G fill:#009110,stroke:#000000
    style H fill:#009110,stroke:#000000
    style I fill:#002191,stroke:#000000
    style J fill:#002191,stroke:#000000
    style K fill:#910007,stroke:#000000
    style L fill:#910007,stroke:#000000
    style M fill:#910007,stroke:#000000
    style N fill:#910007,stroke:#000000
    style O fill:#910007,stroke:#000000
```

**FIXME** Will be useful to include a flow diagram similar to that on [slide 24](https://docs.google.com/presentation/d/1qoA56Wr2qJDOBp7v_lnNiYYFScitYRwo/edit#slide=id.p24)

## References

<a id="1">[1]</a> [PGFinder, a novel analysis pipeline for the consistent, reproducible, and high-resolution structural analysis of bacterial peptidoglycans | eLife](https://elifesciences.org/articles/70597)
