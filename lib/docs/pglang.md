# PGLang

To represent complex, branched peptidoglycan structures using text, PGLang was developed. Both the Mass Calculator and
Fragmenter modules of the WebUI take PGLang as an input. Below, you can see a number of cartoon muropeptide structures
and their PGLang representations. Note that, when representing multimers, the donor must always come first!

![A set of example structures and their PGLang representations](/img/pglang.png)

## Syntax

A more complete description of the syntax can be seen in the railroad diagram below:

![A railroad diagram describing PGLang's syntax](/img/railroad.png)

A more interactive and detailed version of the above can be [found here](/_static/pglang.html).

## Residues

The following residues are built into the PGLang provided via the WebUI and can be referred to by their abbreviations:

|Symbol|Name                        |Formula     |Monoisotopic Mass|
|------|----------------------------|------------|-----------------|
|g     |N-Acetylglucosamine         |`C8H15NO6`  |`221.089937`     |
|m     |N-Acetylmuramic Acid        |`C11H19NO8` |`293.111066`     |
|x     |Unknown Monosaccharide      |            |`0`              |
|A     |Alanine                     |`C3H7NO2`   |`89.047678`      |
|B     |Diaminobutyric Acid         |`C4H10N2O2` |`118.074227`     |
|C     |Cysteine                    |`C3H7NO2S`  |`121.019749`     |
|D     |Aspartic Acid               |`C4H7NO4`   |`133.037507`     |
|E     |Glutamic Acid               |`C5H9NO4`   |`147.053157`     |
|F     |Phenylalanine               |`C9H11NO2`  |`165.078978`     |
|G     |Glycine                     |`C2H5NO2`   |`75.032028`      |
|H     |Histidine                   |`C6H9N3O2`  |`155.069476`     |
|I     |Isoleucine                  |`C6H13NO2`  |`131.094628`     |
|J     |Diaminopimelic Acid         |`C7H14N2O4` |`190.095356`     |
|K     |Lysine                      |`C6H14N2O2` |`146.105527`     |
|L     |Leucine                     |`C6H13NO2`  |`131.094628`     |
|M     |Methionine                  |`C5H11NO2S` |`149.051049`     |
|N     |Asparagine                  |`C4H8N2O3`  |`132.053492`     |
|O     |Ornithine                   |`C5H12N2O2` |`132.089877`     |
|P     |Proline                     |`C5H9NO2`   |`115.063328`     |
|Q     |Glutamine                   |`C5H10N2O3` |`146.069142`     |
|R     |Arginine                    |`C6H14N4O2` |`174.111675`     |
|S     |Serine                      |`C3H7NO3`   |`105.042593`     |
|T     |Threonine                   |`C4H9NO3`   |`119.058243`     |
|U     |Homoserine                  |`C4H9NO3`   |`119.058243`     |
|V     |Valine                      |`C5H11NO2`  |`117.078978`     |
|W     |Tryptophan                  |`C11H12N2O2`|`204.089877`     |
|X     |Unknown Amino Acid          |            |`0`              |
|Y     |Tyrosine                    |`C9H11NO3`  |`181.073893`     |
|Z     |Threo-3-Hydroxyglutamic Acid|`C5H9NO5`   |`163.048072`     |

## Modifications

The following modifications are built into the PGLang provided via the WebUI and can be referred to by their
abbreviations:

|Symbol|Name                |Lost Atoms|Gained Atoms|Net Monoisotopic Mass|Targeted Functional Groups                               |
|------|--------------------|----------|------------|---------------------|---------------------------------------------------------|
|Ac    |O-Acetylation       |`H`       |`C2H3O`     |`42.010564`          |`"Hydroxyl" at="6-Position"`                             |
|Am    |Amidation           |`OH`      |`NH2`       |`-0.984015`          |`"Carboxyl" at="Sidechain"`                              |
|Anh   |1,6-Anhydro         |`H2O`     |            |`-18.010564`         |`"Hydroxyl" at="Reducing End" of="N-Acetylmuramic Acid"` |
|DeAc  |De-N-Acetylation    |`C2H3O`   |`H`         |`-42.010564`         |`"Acetyl" at="Secondary Amide"`                          |
|Glyc  |Glycolylation       |`CH3`     |`CH2OH`     |`15.994914`          |`"Acetyl" at="Secondary Amide" of="N-Acetylmuramic Acid"`|
|Poly  |Wall Polymer Linkage|`H`       |`PO3`       |`77.95068`           |`"Hydroxyl" at="6-Position"`                             |
|Red   |Reduced             |          |`H2`        |`2.01565`            |`"Hydroxyl" at="Reducing End"`                           |

The "Targeted Functional Groups" column describes which residues these modifications can be legally attached to.
