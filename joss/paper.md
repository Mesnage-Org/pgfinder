---
title: PGFinder - A Python package for peptidoglycan analysis
tags:
  - Python
  - proteins
  - peptidoglycan
  - amino acids
authors:
  - name: Neil Shephard
    orcid: 0000-0001-8301-6857
    equal-contrib: true
    corresponding: true
    affiliation: 1
  - name: Ankur Patel
    equal-contrib: true
    affiliation: 2
  - name: Robert Turner
    orcid: 0000-0002-1353-1404
    equal-contrib: true
    affiliation: 1
  - name: Stéphane Mesnage
    orcid: 0000-0003-1648-4890
    equal-contrib: true
    affiliation: 2
affiliations:
 - name: Research Software Engineering, Department of Computer Science, The University of Sheffield
   index: 1
 - name: Mesnage Laboratory, School of Biosciences, The University of Sheffield
   index: 2
date: 30 September 2022
bibliography: paper.bib
---

# Summary

Peptidoglycans are a key components in cell membrane of Gram-positive bacteria and mediate the exchange of DNA between
cells and the response to anti-bacterial drugs. Understanding their biogenesis and structure is key to understanding how
cell surface properties modulate antimicrobial resistance and host-pathogen interactions. The field of
_Peptidoglycomics_ that seeks to model and determine the structure of these molecules based on laboratory based
chromatography is in its infancy but progress will be greatly facilitated by development of software tools such as
`PGFinder` which introduces a streamlined workflow pipelines for analysing and working with laboratory generated data.

# Statement of need

The fields of Proteomics and Glycomics have many software solutions available, but none are currently suited to the
analysis of peptidoglycan molecules which are made from a backbone of glycan chains with peptide side-chains each of
which are themselves composed of unusual sugars and amino acids. As a consequence researchers have traditionally relied
on laborious and error prone manual analysis of data generated from Reversed-Phase High-Pressure Liquid Chromatography
(RP-HPLC) and mass spectroscopy (MS) as no automated tools were available. `PGFinder` is implemented the popular Python
language and addresses this short-coming by introducing an automated workflow of PG structural analysis built on
open-access principles that enable replicable and reproducible analyses to be undertaken and in turn peer-reviewed. As
such `PGFinder` instantiates the field of peptidoglycomics on a firm footing.

# Package Overview

An overview of the iterative search strategy used in the workflow is shown in figure \ref{fig:workflow}.`PGFinder` uses
 a list of theoretical masses for a given set of known molecules based on their molecular structure (Database
 1). Experimental data from mass spectroscopy is matched to these within a defined tolerance to give the matched
 theoretical monomer masses (Library 1). This library forms the basis of a second _in silico_ database of possible
 dimers and trimers that may be formed (Database 2) and these were again compared to the observed masses to generate a
 second library of matched theoretical dimers and trimers (Library 2). A third library (Library 3) is then derived of
 possible modifications that may arise through modifications which contains only modified muropeptides of matched
 monomers, dimers and trimers. Further details of the molecular aspects are given in [@Patel2021Sep].

**TODO** Please review the above, I've attempted to refine and simplify the second paragraph under _Results_ of [@Patel2021Sep].

![Stages undertaken in processing samples using `PGFinder` \label{fig:workflow}](img/flow_diagram.png)

**TODO** - Render flow diagram in PDF from Mermaid if possible (see
[pandoc-mermaid-filter](https://github.com/timofurrer/pandoc-mermaid-filter) which requires
[mermaid-cli](https://github.com/mermaid-js/mermaid-cli)).

<!-- ```mermaid -->
<!-- graph TD; -->
<!--     A[Monomer Masses Database] -\-> C[Match monomers] -->
<!--     B[Deconvoluted MS data] -\-> C([Match monomers -/+ ppm tolerance]) -->
<!--     C -\-> D[DATABASE 1 Matched theoretical monomer masses] -->
<!--     D -\-> E([Calculate dimer & trimer masses]) -->
<!--     D -\-> I([Calculate modified monomers, dimers & trimers]) -->
<!--     D -\-> K([Match & annotate MS data -/+ ppm tolerance]) -->
<!--     E -\-> F[DATABASE 2 Theoretical dimer & trimer masses library] -->
<!--     F -\-> G([Match dimers & trimers -/+ ppm tolerance]) -->
<!--     G -\-> H[Matched theoretical dimers & trimers masses] -->
<!--     H -\-> I -->
<!--     I -\-> J[DATABASE 3 Theoertical modified monomers, dimers & trimers masses library] -->
<!--     J -\-> K -->
<!--     K -\-> L[Raw matched MS data] -->
<!--     L -\-> M([Consolidate in source decay products + salt adducts]) -->
<!--     M -\-> N[Processed MS data] -->
<!--     N -\-> O([Write to CSV file]) -->
<!--     style A fill:#FFBB33 -->
<!--     style B fill:#FFBB33 -->
<!--     style C fill:#FFBB33 -->
<!--     style D fill:#FFBB33 -->
<!--     style E fill:#95FF80 -->
<!--     style F fill:#95FF80 -->
<!--     style G fill:#95FF80 -->
<!--     style H fill:#95FF80 -->
<!--     style I fill:#FF6666 -->
<!--     style J fill:#FF6666 -->
<!--     style K fill:#33BBFF -->
<!--     style L fill:#33BBFF -->
<!--     style M fill:#33BBFF -->
<!--     style N fill:#33BBFF -->
<!--     style O fill:#33BBFF -->
<!-- ``` -->

# Resources and Examples

`PGFinder` is available on [PyPI](https://pypi.org/project/pgfinder/) and the development code is openly available on
[GitHub](https://pypi.org/project/pgfinder/). Documentation is also available
[online](https://mesnage-org.github.io/pgfinder/) and example Jupyter Notebooks are available in Google Colab for users
to test and use. An example of command line usage is provided below

```bash
$ pip install pgfinder
$ find_pg --config config/example.yaml
[Fri, 04 Nov 2022 10:24:02] [INFO    ] [pgfinder] Loaded parameters from file : config/parameters.yaml
[Fri, 04 Nov 2022 10:24:02] [INFO    ] [pgfinder] All parameters converted to decimal
[Fri, 04 Nov 2022 10:24:02] [INFO    ] [pgfinder] Configuration file loaded from     : config/example.yaml
[Fri, 04 Nov 2022 10:24:02] [INFO    ] [pgfinder] Input file                         : data/ftrs_test_data.ftrs
[Fri, 04 Nov 2022 10:24:02] [INFO    ] [pgfinder] NB : All warnings have been turned off for this run.
[Fri, 04 Nov 2022 10:24:02] [INFO    ] [pgfinder] Mass spectroscopy file loaded from : data/ftrs_test_data.ftrs
[Fri, 04 Nov 2022 10:24:02] [INFO    ] [pgfinder] Theoretical masses loaded from      : data/masses/e_coli_monomer_masses.csv
[Fri, 04 Nov 2022 10:24:02] [INFO    ] [pgfinder] PPM Tolerance                      : 0.5
[Fri, 04 Nov 2022 10:24:02] [INFO    ] [pgfinder] Time Delta                         : 10
[Fri, 04 Nov 2022 10:24:02] [INFO    ] [pgfinder] Filtering theoretical masses by observed masses
[Fri, 04 Nov 2022 10:24:03] [INFO    ] [pgfinder] Building multimers from obs muropeptides
[Fri, 04 Nov 2022 10:24:03] [INFO    ] [pgfinder] Building features for multimer type : 1
[Fri, 04 Nov 2022 10:24:03] [INFO    ] [pgfinder] Filtering theoretical multimers by observed
[Fri, 04 Nov 2022 10:24:06] [INFO    ] [pgfinder] Building custom search file
[Fri, 04 Nov 2022 10:24:06] [INFO    ] [pgfinder] Generating variants
[Fri, 04 Nov 2022 10:24:06] [INFO    ] [pgfinder] Matching
[Fri, 04 Nov 2022 10:24:08] [INFO    ] [pgfinder] Cleaning data
[Fri, 04 Nov 2022 10:24:08] [INFO    ] [pgfinder] Processing 13 Sodium Adducts
[Fri, 04 Nov 2022 10:24:08] [INFO    ] [pgfinder] No ^K+ found
[Fri, 04 Nov 2022 10:24:08] [INFO    ] [pgfinder] Processing 26 in source decay products
[Fri, 04 Nov 2022 10:24:08] [INFO    ] [pgfinder] Processing complete!
[Fri, 04 Nov 2022 10:24:08] [INFO    ] [pgfinder] Metadata save to                   : output
[Fri, 04 Nov 2022 10:24:08] [INFO    ] [pgfinder] Results saved to                   : output/results.csv
```

# Citations


# Acknowledgements

Funding to develop and improve documentation and accessibility to `PGFinder` was
provided by the [Unleash Your Data and Software](https://www.sheffield.ac.uk/library/rdm/unleashdatasoftware)
initiative at The University of Sheffield.


# References
