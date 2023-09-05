# Usage

Two options are available to run PGFinder: (i) an online Web User Interface (WebUI) or (ii) a Command Line Interface. 
The [Data Dictionary](data_dictionary.md) describes software inputs and outputs.

## WebUI

An interactive web-page for running your analysis is available at
[mesnage-org.github.io/pgfinder-gui/](https://mesnage-org.github.io/pgfinder-gui/). On first visiting the page you will
have to wait a whilst it sets up in the background (for those curious or interested it is using
[pyodide](mesnage-org.github.io/pgfinder-gui/) a [Web Assembly language (WASM)](https://webassembly.org/) in the
background to install PGFinder and all its Python dependencies). Once loaded the page should look like the image below.

![Initial screenshot of PGFinder GUI](https://github.com/Mesnage-Org/pgfinder/assets/70374280/9537c200-5b48-4d50-ac72-1c8b62d83909)


### Upload a file

You should click on the large button with a dashed border to **Upload a file** and select your Byos (`.ftrs`) or
MaxQuant (`.txt`) file that you wish to analyse. Please note that the versions currently supported for Byos is 3.11 and MaxQuant is 2.4.2.0. 
Please note that this WebUI allows you to upload multiple deconvoluted datasets to perform several searches with the same database in one go. 
Each search output will be downloaded as an individual .csv file.  
If you have no deconvoluted dataset but you want to test PGFinder, you can download a file for a test by clicking on the top left corner of the screen, as indicated below. The test file provided is a .ftrs file corresponding to a dataset described in the PGFinder article (Patel et al., 2021, eLife).

![image](https://github.com/Mesnage-Org/pgfinder/assets/70374280/ffbab2ad-893c-4be5-8c74-891b33d85237)



### Choose a Mass Database

You then have the option to chose which **Mass Database** will be used to compare your sample to. There are several
provisioned for your convenience, from two bacterial species _Clostridium difficile_ and _Escherichia coli_. Each
species has three associated libraries, `Simple` / `Non-Redundant` / `Complex` and you can choose which to select by
clicking on the downwards point arrow next to the species name to expand the options and clicking on on the database you
wish to use, it will turn white to indicate it has been selected as shown below (**NB** hover the mouse of the circle
with an `i` in it and tool-tip box will pop-up describing the database).


![image](https://github.com/Mesnage-Org/pgfinder/assets/70374280/41764585-e64f-4a23-adfd-c7a379d47782)


#### Using a Custom Database

If you have your own database you can choose to upload it by clicking on **Custom** and the the **Upload a file** box
that appears under this and selecting your `.csv` file to upload.

### Advanced Options

A number of advanced options are now available and they can be viewed and set by clicking on the downwards point arrow
next to the text **Advanced Options**.

#### Modifications

A scrollable list of modifications is presented, select by clicking on these. You can select as many modifications as
you like, just click on those you want to enable and the background will turn white to indicate it has been
selected. The list is long but there is slider on the right or you can scroll up and down with your mouse-wheel if you
have one.

#### PPM Tolerance

The Parts Per Million tolerance for matching molecules can be set, enter a number in the box underneath the **PPM
Tolerance** heading.

#### Cleanup Window

The Cleanup Window parameter can also be set.

In the screenshot below we have...

1. Uploaded the ftrs file provided as an example = **E. coli_WT (Patel et al).ftrs**.
2. Selected the _Escherichia coli_ **Non-Redundant** mass database.
3. Enabled Cross-Linked Multimers and Anhydro-MurNAc Modifications.
4. Set the PPM to 15.
5. Set the Cleanup Window to 0.5.
6. Set the consolidation PPM to 1.

![image](https://github.com/Mesnage-Org/pgfinder/assets/70374280/a63e21ff-8276-4bdd-be64-c27b41c4aab1)


### Run Analysis

Once you are ready to run the analysis simply click on the **Run Analysis** button.

### Results

Analysis will run and a CSV file will automatically download, you should see a pop box telling you the file has
downloaded. In most browsers, unless the configuration has been changed, the file will be downloaded to the `Downloads`
directory on your computer. Most browsers let you see a list of files that have been downloaded if you press `Control +
j`.

The results have the same name as the input file but with the extension `.csv`. This can be opened in statistical
software or spreadsheets for subsequent viewing.

The picture below shows the expected content of the output. It contains the following columns:
1. Metadata; describes all relevant information related to the search parameters, including the name of the deconvoluted data file and mass database used, the cleanup window time, modifications enabled, ppm tolerance, ppm consolidation value and PGFinder version used).
2. ID; scan ID
3. RT(min); retention time (in minutes) associated with the theoretical mass matched
4. Charge; charge state of ions detected with the observed mass
5. Obs(Da); deconvoluted mass (in Daltons) of individual molecules
6. Theo(Da); theoretical monoisotoopic mass corresponding to the structure searches
7. Delta_ppm; difference between observed and theoretical masses matched
8. Inferred structure; muropeptide structure searched
9. Intensity; ion intensity corresponding to the molecules with the observed mass matched to a theoretical structure
10. Inferred structure (consolidated); most likely structure displaying the lowest absolute delta_ppm value. if two or more matches have a theoretical mass less than the consolidation ppm apart, then those matches are retained, leaving several possible matches consolidation 
11. Intensity (consolidated); ion intensity corresponding to the molecules with the observed mass matched to a theoretical consolidated structure.     


![image](https://github.com/Mesnage-Org/pgfinder/assets/70374280/309144ee-93a5-4ede-a861-ef18c231954e)


## Command Line

If you wish to use the command line version you will have to follow the [installation](installation.md) instructions to
install PGFinder on your computer.

## `find_pg`

You can also use the command line interface `find_pg` which works with a YAML configuration file (see
`pgfinder/default_config.yaml`) for an example which you can modify. You must supply at least one option on the command line `-c
<path/to/config.yaml>`, so to use the example config you would.

``` bash
find_pg -c pgfinder/default_config.yaml
```

Each option in the configuration file can be over-ridden at the command line, see `find_pg --help` for more
information.
