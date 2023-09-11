# Usage

Two options are available to run PGFinder: (i) an online Web User Interface (WebUI) or (ii) a Command Line Interface.
The [Data Dictionary](data_dictionary.md) describes software inputs and outputs.

## WebUI

An interactive web-page for running your analysis is available at
[mesnage-org.github.io/pgfinder/](https://mesnage-org.github.io/pgfinder/). On first visiting the page you will
have to wait awhile whilst it sets up in the background (for those curious or interested, it is using
[Pyodide](https://pyodide.org/en/stable/) running on [Web Assembly (WASM)](https://webassembly.org/) It'll take
some time to install PGFinder and all its Python dependencies. Once loaded, the page should look like the image below.

![Initial screenshot of PGFinder GUI](https://github.com/Mesnage-Org/pgfinder/assets/70374280/9537c200-5b48-4d50-ac72-1c8b62d83909)


### Upload a file

You should click on the large button with a dashed border to **Upload a file** and select your Byos (`.ftrs`) or
MaxQuant (`.txt`) file that you wish to analyse. Please note which versions of these programs are currently supported — the tooltip contains specific version numbers
Please note that this WebUI allows you to upload multiple deconvoluted datasets to perform several searches with the same database and settings in one go.
Each search output will be downloaded as an individual .csv file.
If you have no deconvoluted dataset but you want to test PGFinder, you can download a file for testing by clicking on the top left corner of the screen as indicated below. The test file provided is a `.ftrs` file corresponding to a dataset described in the PGFinder article (Patel et al., 2021, eLife).

![Downloading test ftrs file](https://github.com/Mesnage-Org/pgfinder/assets/70374280/ffbab2ad-893c-4be5-8c74-891b33d85237)



### Choose a Mass Database

You then have the option to choose which **Mass Database** will be used to search your sample. There are several
provisioned for your convenience, from both _Clostridium difficile_ and _Escherichia coli_. Each
species has three associated libraries (`Simple` / `Non-Redundant` / `Complex`), and you can choose which to select by
clicking on the downwards pointing arrow next to the species name to expand the options, and then clicking on on the database you
wish to use. It will turn white to indicate it has been selected as shown below (**NB** hover the mouse over the circle
with an `i` in it, and a tooltip describing the database will appear).


![Choosing mass libraries](https://github.com/Mesnage-Org/pgfinder/assets/70374280/41764585-e64f-4a23-adfd-c7a379d47782)


#### Using a Custom Database

If you have your own database, you can choose to upload it by clicking on **Custom** and then the **Upload a file** box
that appears under this. Then you can select which `.csv` file to upload.

### Advanced Options

A number of advanced options are now available, and they can be viewed and set by clicking on the downwards pointing arrow
next to the text **Advanced Options**.

#### Modifications

A scrollable list of modifications is presented; select by clicking on these. You can select as many modifications as
you'd like, just click on those you want to enable and the background will turn white to indicate that it has been
selected. The list is long, but there is slider on the right or you can scroll up and down with your mouse-wheel / touchpad.

#### PPM Tolerance

The Parts Per Million tolerance for matching molecules can be set by entering a number in the box underneath the **PPM
Tolerance** heading.

#### Cleanup Window

This is the retention-time window (in minutes) that PGFinder will search when looking for salt adducts and decay products
of each identified structure. These adducts and decay products are then removed from the search output, and their intensities
are transferred to the parent ion / structure.

#### Consolidation PPM

During consolidation, structures with the lowest absolute ppm are selected over those farther from the theoretical mass.
However, if two or more matches have a theoretical mass less than the consolidation ppm apart, then all of those matches are retained.
This parameter defines the minimal difference in absolute ppm below which no consolidation is made.


In the screenshot below we have...

1. Uploaded the ftrs file provided as an example = **E. coli_WT (Patel et al).ftrs**.
2. Selected the _Escherichia coli_ **Non-Redundant** mass database.
3. Enabled Cross-Linked Multimers and Anhydro-MurNAc Modifications.
4. Set the PPM to 15.
5. Set the Cleanup Window to 0.5.
6. Set the consolidation PPM to 1.

![Setting Advanced Options in PGFinder](https://github.com/Mesnage-Org/pgfinder/assets/70374280/a63e21ff-8276-4bdd-be64-c27b41c4aab1)


### Run Analysis

Once you are ready to run the analysis, simply click on the **Run Analysis** button.

### Results

After the analysis has run, a CSV file will be automatically downloaded. In most browsers, unless the configuration has been changed, the file will be downloaded to the `Downloads`
directory on your computer. Most browsers let you see a list of files that have been downloaded if you press `Control + j`.

The result file has the same name as the input file but with the extension `.csv`. This can be opened in statistical
software or spreadsheets for subsequent viewing.

The picture below shows the expected content of the output. It contains the following columns:
1. Metadata; describes all relevant information related to the search parameters, including the name of the deconvoluted data file and mass database used, the cleanup window time, modifications enabled, ppm tolerance, ppm consolidation value, and PGFinder version used.
2. ID; scan ID
3. RT(min); retention time (in minutes) associated with the theoretical mass matched
4. Charge; charge state of ions detected with the observed mass
5. Obs(Da); deconvoluted mass (in Daltons) of individual molecules
6. Theo(Da); theoretical monoisotoopic mass corresponding to the structure searches
7. Delta_ppm; difference between observed and theoretical masses matched
8. Inferred structure; muropeptide structure searched
9. Intensity; ion intensity corresponding to the molecules with the observed mass matched to a theoretical structure
10. Inferred structure (consolidated); most likely structure displaying the lowest absolute delta_ppm value. if two or more matches have a theoretical mass less than the consolidation ppm apart, then those matches are retained, leaving several possible matches.
11. Intensity (consolidated); ion intensity corresponding to the molecules with the observed mass matched to a theoretical consolidated structure.


![Sample output from PGFinder](https://github.com/Mesnage-Org/pgfinder/assets/70374280/309144ee-93a5-4ede-a861-ef18c231954e)


## Command Line

If you wish to use the command line version you will have to follow the [installation](installation.md) instructions to
install PGFinder on your computer.

## `find_pg`

You can also use the command line interface `find_pg` which works with a YAML configuration file (see
`lib/pgfinder/default_config.yaml`) for an example which you can modify. You must supply at least one option on the command line `-c
<path/to/config.yaml>`, so to use the example config you would.

``` bash
find_pg -c pgfinder/default_config.yaml
```

Each option in the configuration file can be overridden at the command line, see `find_pg --help` for more
information.
