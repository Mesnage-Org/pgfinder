# Svelte

The website uses the [Svelte][svelte] framework which is written in [JavaScript][js] and [TypeScript][ts] and uses
[WebASsembly][wa] to run the PGFinder Python code and Smithereens Rust code in the users browser rather than relying on
a server.


## Development

To add sections to the website you need to understand the structure of the [Svelte][svelte] framework. The pages
components reside under the `src/` directory. There are two sub-directories `src/` and `lib/`.

``` bash
❱ tree src
[4.0K Jan 10 10:11]  src
├── [ 767 Jan 10 10:11]  src/app.d.ts
├── [ 592 Jan 10 10:11]  src/app.html
├── [ 252 Jan 10 10:11]  src/app.postcss
├── [4.0K Mar 20 08:09]  src/lib
│   ├── [ 165 Jan 10 10:11]  src/lib/constants.ts
│   ├── [  75 Jan 10 10:11]  src/lib/index.ts
│   └── [2.1K Mar 20 08:09]  src/lib/pgfinder.ts
└── [4.0K Mar  6 15:40]  src/routes
    ├── [2.1K Jan 10 10:11]  src/routes/AdvancedOptions.svelte
    ├── [1015 Jan 10 10:11]  src/routes/BuiltinLibrarySelector.svelte
    ├── [1.6K Jan 10 10:11]  src/routes/ErrorModal.svelte
    ├── [ 352 Jan 10 10:11]  src/routes/Footer.svelte
    ├── [1.1K Feb 14 16:49]  src/routes/Header.svelte
    ├── [  31 Jan 10 10:11]  src/routes/+layout.js
    ├── [2.2K Feb 14 16:49]  src/routes/LinksAndDownloads.svelte
    ├── [1.5K Jan 10 10:11]  src/routes/MassLibraryUploader.svelte
    ├── [ 684 Jan 10 10:11]  src/routes/ModificationSelector.svelte
    ├── [1.2K Jan 10 10:11]  src/routes/MsDataUploader.svelte
    ├── [3.9K Jan 10 10:11]  src/routes/+page.svelte
    ├── [   0 Mar  6 15:40]  src/routes/SmithereensUploader.svelte
    └── [ 694 Feb 14 16:49]  src/routes/Tooltip.svelte

3 directories, 19 files
```

### `src/lib`

The `src/lib/` directory contains [TypeScript][ts] files. These are imported automatically via the `$lib` alias as noted
in `index.ts`. Currently PGFinder has three files `constants.ts`, `pgfinder.ts` and `smithereens.ts`

#### `src/lib/constants.ts`

This exports a set of parameters that are set as defaults for the Python components and are stored in the `defaultPyio`
variable. It includes...

| Variable               | Value                              |
|:-----------------------|------------------------------------|
| `msData`               | Undefined, defaults loaded by xxx. |
| `massLibrary`          | Undefined, defaults loaded by xxx. |
| `enabledModifications` | Default is none.                   |
| `ppmTolerance`         | `10`                               |
| `cleanupWindow`        | `0.5` seconds.                     |
| `consolidationPpm`     | `1`.                               |

#### `src/lib/pgfinder.ts`

This script imports [Pyodide][pyodide], a [WebAssembly][wa] library that allows PGFinder to run in the browser as well
as the constants that are defined in `src/lib/constants.ts`.

``` typescript
import type { PyProxy, PythonError } from 'pyodide/ffi';       // Imports Python modules
import { loadPyodide, type PyodideInterface } from 'pyodide';  // Imports pyodide
import { defaultPyio } from '$lib/constants';                  // Imports src/lib/constants.ts

const pyio: Pyio = { ...defaultPyio };    // Stores constants in pyio
let pyodide: PyodideInterface;            // Aliases PyodideInterface to pyodide
```

It then installs the dependencies and PGFinder package with the section below, note the `micropip.install()` commands
and loads the available reference masses and target structures/muropeptides for the `smithereens` component and the mass
library used by PGFinder. These are loaded via `pyodide.runPythonAsync()` which calls functions which are in the
`pgfinder/gui/shim.py` module

``` typescript
(async () => {
	// NOTE: This version needs to match the version of pyodide installed by npm!
	// These files can also be hosted locally from `/static` if something ever
	// happens to this CDN, but there will be some build-system demons to battle.
	pyodide = await loadPyodide({
		indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.23.4/full/'
	});
	pyodide.registerJsModule('pyio', pyio);
	await pyodide.loadPackage(['micropip', 'sqlite3']);
	const micropip = pyodide.pyimport('micropip');
	await micropip.install('pgfinder==1.2.0-rc1');
	await pyodide.runPythonAsync('import pgfinder; from pgfinder.gui.shim import *');

	const pgfinderVersion = await pyodide.runPythonAsync('pgfinder.__version__');

	const proxy = await pyodide.runPythonAsync('allowed_modifications()');
	const allowedModifications = proxy.toJs();
	proxy.destroy();

    // Load lib/pgfinder/masses/index.json which details the available mass databases
	const json = await pyodide.runPythonAsync('mass_library_index()');
	const massLibraries = JSON.parse(json);

    // Load lib/pgfginder/reference_masses/index.json which details the available reference masses
    const jsonFragments = await pyodide.runPythonAsync('reference_mass_library_index()');
    const fragmentsLibraries = JSON.parse(jsonFragments);

    // Load lib/pgfginder/target_structures/index.json which details the available target_structures/muropeptides
    const jsonMuropeptides = await pyodide.runPythonAsync('target_structure_library_index()');
    const muropeptidesLibraries = JSON.parse(jsonMuropeptides);

	postMessage({
		type: 'Ready',
		content: {
			pgfinderVersion,
			allowedModifications,
			massLibraries,
            fragmentsLibraries,
            muropeptidesLibraries
		}
	});
})();
```

#### `src/lib/smithereens.ts`

**WORK IN PROGRESS** This is _highly_ experimental and requires manual building of the `smithereens` package from the
[`TheLostLambda/smithereens@wasm-pilot`](https://github.com/TheLostLambda/smithereens/tree/wasm-pilot/pkg) branch. In
due course this situation will be improved and the WebAssembly built and compiled in an automated manner.

The `smithereens` package needs to be compiled under [WebAssembly][wa]. Doing so results in a number of files being
built and saved in the `pkg/` subdirectory. Currently these are copied from the
[`TheLostLambda/smithereens@wasm-pilot`](https://github.com/TheLostLambda/smithereens/tree/wasm-pilot/pkg) branch to the
`web/src/lib/` directory as attempts to build them elsewhere have failed.

#### `src/routes/*`

The `src/routes` directory contains the source for the pages and how they are displayed. The main page layout is defined
in `+page.svelte` which imports content from the other files in this directory as well as the [WebAssembly][wa] setup
and libraries defined under the `web/src/lib` directory. These later items are imported using the prefix `$lib/`.

Typically these files have a header which contains a [TypeSciprt][ts] section for importing and loading functions and
variables. This is delimited by `<script lang="ts">...</script>` and is followed by HTML which defines the layout of the
page/components.

The [div][div] element of class [card][card] is used to layout the components of PGFinder WebUI.

#### Adding a New Card

To define a new card for inclusion you need to add a section to the `+page.svelte` of type `<div class="card*">`. As an
example the [smithereens][smithereens] functionality for building fragments from components was added by including the
following import in the [TypeScript][ts] section at the top of the file.

``` typescript
<script lang="ts">
    ...
    //Svelte Component Imports
    ...
    import FragmentsDataUploader from './FragmentsDataUploader.svelte'
    ...
</script>
```

HTML markup is then used to define the card itself which displays the content defined in the
`src/routes/FragmentsDataUploader.svelte` file.

``` html
        <!-- Smithereens -->
		<div class="card m-2 w-[20rem] {uiWidth} max-w-[90%] {animateWidth}">
			<section class="flex flex-col space-y-4 justify-center p-4">
				<FragmentsDataUploader bind:value={pyio.fragmentsData} />
				<button type="button" class="btn variant-filled" on:click={runAnalysis} disabled={!ready}>
					Build database
				</button>
				{#if processing}
					<ProgressBar />
				{/if}
			</section>
		</div>
```

The `src/routes/FragmentsDataUploader.svelte` file, like its parent `src/routes/+page.svelte` also starts with a
[TypeScript][ts] script header which imports components and exports objects which are used in the HTML body (two
[`<div>`][div] sections) which contain the contents of the [card][card]. The first [`<div>`][div] defines the _Building
block components_ which allows users to choose which file is used for the reference masses that muropeptides are built
out of. There is a header for the section (`<h5>...</h5>`) followed by a short paragraph (`<p>...</p>`). A
`<TabGroup>...</TabGroup`] is then defined which has two `<Tab>...</Tab>` one which determine whether the "_Built-In_"
or "_Custom_" libraries are used and binds these to the `customFragmentsLibrary`.

A section `<svelte:fragment>...</svelte:fragment>` then follows which defines further the layout, logic and behaviour.

``` html
<div class="flex flex-col items-center">
	<h5 class="pb-1 h5">Building block components</h5>
    <p>(list of sugars and amino-acids)</p>
	<TabGroup class="w-full" justify="justify-center">
		<Tab bind:group={customFragmentsLibrary} name="built-in" value={false}>Built-In</Tab>
		<Tab bind:group={customFragmentsLibrary} name="custom" value={true}>Custom</Tab>
		<svelte:fragment slot="panel">
			{#if customFragmentsLibrary}
				<FileDropzone name="fragments-library" bind:files on:change={dataUploaded} accept=".csv">
					<svelte:fragment slot="message">
						{#if value === undefined}
							<p><b>Upload a file</b> or drag and drop</p>
						{:else}
							<p>{value.name}</p>
						{/if}
					</svelte:fragment>
					<svelte:fragment slot="meta">
						{#if !value}
							Fragments (.csv)
						{/if}
					</svelte:fragment>
				</FileDropzone>
			{:else if fragmentsLibraries !== undefined}
				<BuiltinFragmentsSelector bind:value {fragmentsLibraries} />
			{:else}
				<div class="flex justify-center">
					<ProgressRadial />
				</div>
			{/if}
		</svelte:fragment>
	</TabGroup>
</div>

```

Here we are adding buttons to load files automatically or allow users to upload their own. These files are part of the
Python package and reside under `lib/pgfinder/target_structures` and `lib/pgfinder/reference_masses` (there is already a
series of files under `lib/pgfinder/masses` that form the basis of the mass library). In each of these folders there
should be an `index.json` the structure of which is defined below.

##### `lib/pgfinder/reference_masses`

The reference masses are the masses of the components of proteins, amino acids, sugars and di-aminoacids. The file
itself is described in the [data dictionary](data_dictionary#reference_masses).

##### `lib/pgfinder/target_structures`

The target structures are the structures for which the masses are to be determined, they contain details of the
components which correspond to items in the reference masses file. The structure of these files is described in the
[data dictionary](data_dictionary#target_strucutres).

##### `index.json`

Each of the sets of reference files needs an accompanying `index.json` which defines (in [Java Script Object
Notation][json]) each of the files within the directory. The structure is a key (typically a bacterial species) with a
`File` and `Descriptor` field. The single entry for _E. coli_ in the `lib/pgfinder/reference_masses/index.json` is shown
below.

``` json
{
  "Escherichia coli": {
    "File": "escherichia_coli.csv",
    "Description": "Contains the reference masses of sugars, amino acids and Diaminoacids for E. coli."
  }
}
```

These files are loaded by Svelte and provide the information that is displayed in the website and so a corresponding
type definition is required in the `web/src/app.d.ts` file. For both the reference masses and target structures the
entries have an index (of type `string`) with two entries, a `File` which is a string pointing to the file associated
with that entry and a `Description` describing the file. The mapping of the [TypeScript][ts] definition to the
`index.json` is hopefully transparent.

``` typescript
declare type FragmentsLibraryIndex = {
	[index: string]: {
		File: string;
		Description: string;
	};
};
declare type MuropeptidesLibraryIndex = {
	[index: string]: {
		File: string;
		Description: string;
	};
};
```

How they are loaded is somewhat obfuscated, at least at the time of writing, hopefully the following helps clarify.

The `pgfinder.gui` sub-module has itself two sub-modules `pgfinder.gui.internal` and `pgfinder.gui.shim`. The
`internal` sub-module (in file `lib/pgfinder/gui/internal.py`) includes the functions `ms_upload_reader()` and
`theo_masses_upload_reader` which are to be replaced by the generic `upload_reader()`. This later function takes two
arguments the `upload` which is a dictionary or byte stream if a file is being uploaded by the user and the path to a
`lib_dir` (library directory). The three possible library directories are defined as constants of object type
[`Path()`][pathlib]. These functions and library paths are imported by the `shim` module and used in the
`run_analysis()` function (`ms_upload_reader()` and `theo_masses_upload_reader`) for loading the user provided Mass
Spectroscopy results and the theoretical masses (either a selected default file or a user provided one).

The `upload_reader()` is used in the `load_libraries()` function to load the fragments and muropeptides from either the
selected list or the user provided files. These are returned as a dictionary with keys `fragments` and `muropeptides`
which contain the respective data as [Pandas DataFrames][pandas]. These in turn are written passed to `smithereens` for
building the masses of the target structures.

Both the `run_analysis()` and `load_libraries()` functions import from a Python library `Pyio` what this is was a bit of
a mystery until I found it was defined, of sorts, in `web/src/lib/pgfinder.ts` which imports `defaultPyio` from
`web/src/lib/constants.ts` and uses this to define a constant `pyio` of type `defaultPyio`.

`pgfinder.ts` also has functions to load the `index.json` that define the files available in each library

## Testing

In order to test the website locally we need to _not_ attempt to install PGFinder from [PyPI][pypi], to achieve this we
need to do two things.

1. Build a wheel (`.whl`) from the current development version of `lib/`.
2. Place the `.whl` in the `web/src/lib/` directory and point `micropip.install()` (in `src/lib/pgfinder.ts`) to use it.

### Building PGFinder Wheel

A "wheel" is like a compressed archive of a Python package that contains everything that is required to use and run the
code. To build the wheel make sure you have the necessary dependencies installed and use the following commands. A
`.tar.gz` and `.whl` file will be created in the `dist/` directory. The version will reflect the current Git tag and a
combination of the git commits as typically you will be ahead of the last tag.

``` bash
cd pgfinder/lib
pip install -e .[pypi]
python -m build --no-isolation
ls -lha dist/
drwxr-xr-x neil neil 4.0 KB Thu Apr  4 10:06:59 2024  .
drwxr-xr-x neil neil  20 KB Thu Apr  4 10:06:58 2024  ..
.rw-r--r-- neil neil  38 KB Thu Apr  4 10:06:59 2024  pgfinder-1.2.0rc2.dev32+gf23930e.d20240404-py3-none-any.whl
.rw-r--r-- neil neil  22 MB Thu Apr  4 10:06:58 2024  pgfinder-1.2.0rc2.dev32+gf23930e.d20240404.tar.gz
```

### Using the Wheel

Copy the wheel to `pgfinder/web/src/lib/` and edit `pgfinder/web/src/lib/pgfinder.ts` so that `micropip.install()` loads
this file.  **NB** the leading `./` is important it says to look in the current directory as both the `pgfinder.ts` and
`.whl` are in the `pgfinder/web/src/lib/` directory.

``` typescript
//	await micropip.install('pgfinder==1.2.0-rc1');
	await micropip.install('./pgfinder-1.2.0rc2.dev32+gf23930e.d20240404-py3-none-any.whl');
```


### What is Happening?

How do you see what is going on with all this code? There isn't much output in the console where you started the `pnpm
dev` server unless you mess up the Svelte structure so how do you find out whether the [WebAssembly][wa] that is loading
PGFinder and Smithereens is working? Well because WebAssembly runs the code in your browser you need to look
there. Opening `https://localhost:5173/` you see the PGFinder page, the version listed should reflect that which you
have built and copied to `pgfinder/web/src/lib/` and modified `pgfinder.ts` to upload.

All modern browsers have ability to "Inspect Element" a web-page, in Firefox and Opera this is accessed via `Ctrl + Shift + C`
in Vivaldi its `Ctrl + Shift + I`. This opens up a dialog with lots of tabs, _Elements_, _Console_, _Sources_,
_Network_, _Performance_, _Memory_, _Application_, _Security_ and so forth and gives you a window into what the website
is doing.

#### Elements

This shows the raw HTML that lays out the page. Not a huge amount to see or use here.

#### Console

This is the useful part for development as it shows the commands that are run by JavaScript, TypeScript and WebAssembly
and it is here you can find information warnings and errors about what has happened

## State Diagram

In an attempt to make sense of how everything hangs together and interacts the following [Mermaid State
Diagram](https://mermaid.js.org/syntax/stateDiagram.html) has been created. Its probably not currently accurate due to
my lack of understanding


<!--
https://mermaid.live/edit?gist=https://gist.github.com/ns-rse/59f7fd4e221c858056e449bd72340673#pako:eNqtV21PIzcQ_ivWSgjQhZSQQEk-FNED2qq8ieSKWkWKnN3ZxL1de2V7Cdso_71j7_tmA_lwCHG3nmc8nmcej-214woPnJFzcLBmnOkRWR_qJYRwOCKHvpCg9OGUk_xnM-Wbg4N0IP2rNNVww-hC0vDk7WzK02E3oErdgE88qinxWRCM3IQ2jSuYxyy1Rox_b1gjKVxQivFFCkkgCMRqKzgZv0GA_6yrlgd1g4G_RYGgHkhycvIL-RLRBXSVBacgLtBNssVSE-HX7KTM-Z4miohYE6SFPCMkT9H8_MHdIPZAkUkSgXIliwyOasLCSEityKhCHvlCrr03yl3wniLNBFfElyIk3Z8aw7VF5q53Alcrc4_0qxX4O9iUM2D61Qq8R8rVNfduxIobnorlbBla3R-wTPdsLqlMDM-VmA3LzgU0ipR710YLx9L1Kw0CRZ5_u2PcuB2tlsxdEhkjn7EdeYX5tVIQzoPkmFDukTS7Ri2ihW8n-AukQtbrRmqkBt6D8JjPXGrLUkeERZIMGiZf0kUIXJd2csS40fMCN5Q6bkwUSxEBVh51tNOhdHldAs-EzxSRWN6kmZmlgnIaJAohLuZi9pDRb55zNxJKP-DUqOejKGHiOGW_sKN00zkB6TP7JP1q6rd9X2VSbTdm8mw3bktyR4SM4T02eW1bG0ieY2rOv1q8MwCyY42LmHXVkoVtvcOA0vGxCLFNJHopODGtlawk0xpLtmJ6iTU1jWJcaRQRygjLHVHsn4CsqaurqzbmN9WOVyx6XRY-WjDRxRqLWWinnElL9NFxsXjGcX5URcMnVDNsr7APvjrawkkOMSPWjEKc5To8Ot4BMtWbBbnwq7A6x7txkyXKHH9DoBxpFRZq9S7BBwmoWJKSYruBpnIBGqmUsatjWd29xiwBB7lxD81cZppa9_n28nL7OLn_m9w83Y7J49OEXD8_316_kMkTeX16-bOElhUsx5pZWAra5Fy61Fm0Di-g4kCrFmlklqoyErVSjI1yyx0Wu82z0Y0rE-zoyLUyBeDbKn2CxdPUnKUGiAUhRbSvVHp7Hay2MWOjV-iE1YntBOZ-AN024reybO0clVzb7O0ZF8Lcy6VMPIdbsU1SLY4LLf4IJtR-VGRbopK8aSrvve6_qnoc1srbisDLGuM4k9kqNr5tdiQUAbhxQGUWqUMEx96Fy1URuOaQq2y8QOARZd28LEs8YIjHVBTQBDwMbI51xaqc1nOzd8cZntf-LBQc27BUM1eEUQDvXVe97QZxwbH5eXh3wPbxMVQxM18dAxglYJ_EbII-iNmENmNuSmhax6LJzXZU9OzTip7tV9GtdoovBGLyxcLidcdo0SPV4ATv94Fnbh-pw0e1S_PubSWaJpk27VnZtLey7H-aZX-_LJuhfphuS7fHX8kJHluggFAJxI0l0qqDhHhxGCbZYkx_yE9bNC3pG2SnUVF_vDPYF1b3I2LnMxXPNb6gmGpT2llz0KeAd8ZtsBlncVgfVjOKFMVqq2z2GZfv_KZEO9vlNGlUPdNXXad-nnRa27d9RlZ9i_tR-YR0Og7uppAyDx-7VjpTxz50p84I_-tR-X3q4OsWcXGEa4Fbj2khnRGuEDoOjbUYJ9zNv1NM9u7NByPK_xGi-umM1s67MzrpDXuX3fOLwcXpcDC8vBicd5zEGV30u4Nhf3h-Ohienw1-7vU2Hec_O0G_27-8PL047fd7_QF6Dc43_wNVgRMQ
-->
``` mermaid
%%{init: {'theme': 'forest'
         }
}%%

    stateDiagram-v2

    classDef data fill:cyan
    classDef webui fill:pink
    classDef processing fill:yellow

    state Svelte {

    MsDataUploader --> +page.svelte
    note right of +page.svelte
        Lays out the Page

        Includes Typescript that imports :
          + AdvancedOptions from ./AdvancedOptions.svelte
          + Footer from ./Footer.svelte
          + Header from ./Header.svelte
          + LinksAndDownloads from ./LinksAndDownloads.svelte
          + MassLibraryUploder from ./MassLibraryUploader.svelte
          + MsDataUploader from ./MsDataUploader.svelte

        Calls PGFinder (which runs under WebAssembly) and loads :
          + pgfinderVersion
          + allowedModifications
          + massLibraries
          + fragmentsLibraries (in progress)
          + muropeptidesLibraries (in progress)

        When state is ready :
          + runs analysis calling the pgfinder.postMessage(pyio) from pgfinder.ts
    end note
    AdvancedOptions --> +page.svelte
    Footer --> +page.svelte
    Header --> +page.svelte
    LinksAndDownloads --> +page.svelte
    FragmentDataUploader --> +page.svelte
    +page.svelte --> pgfinder
    pgfinder --> +page.svelte
    web/src/app.d.ts --> FragmentDataUploader
    web/src/app.d.ts --> MsDataUploader
    note left of web/src/app.d.ts
        TypeScript file defining types of different elements.

        Key is Pyio which contains the results of different stages of loading
        and processing data.
    end note

    pyio --> gui.shim
    note right of pyio
    Some Python code written within TypeScript that passes parameters???
    end note
    }
    state pgfinder {
        pgio.theo_masses_reader() --> gui.internal
        pgio.ms_file_reader() --> gui.internal
        gui.internal --> gui.shim
        gui.shim --> run_analysis()
        gui.shim --> load_libraries()
        note right of load_libraries()
        This is meant to load the reference masses and target structures
        and return them to the

        CURRENTLY DOES NOT APPEAR TO WORK
        end note

        load_libraries() --> FragmentDataUploader
        run_analysis() --> Results
    }
    state Results {
        yswsii:Results Files
    }
    state MsDataUploader {
        MsDataUploader.svelte
        note left of MsDataUploader.svelte
        Layout of Mass Uploader Card

        Includes Typescript that allows user to upload file.
        end note
    }
    state FragmentDataUploader {
        FragmentDataUploader.svelte
        note right of FragmentDataUploader.svelte
        Layout of Fragment and Target Structures Card

        Includes Typescript that allows user to upload files.
        end note
    }
    state web/src/app.d.ts {
        VirtFile
        Pyio
        MsgType
        MassLibraryIndex
        FragmentsLibraryIndex
        MuropeptidesLibraryIndexIndex
        ReadyMsg
        ResultMsg
        ErrorMsg
        Msg
    }
    state masses {
        index1.json
        note left of index1.json
        Defines the files with molecular masses, one per species
        along with description displayed in Website
        end note
        c_diff_monomers_complex.csv
        c_diff_monomers_non_redundant.csv
        c_diff_monomers_simple.csv
        e_coli_monomers_complex.csv
        e_coli_monomers_non_redundant.csv
        e_coli_monomers_simple.csv
    }
        state reference_masses {
        index2.json
        note left of index2.json
        Defines the files with reference masses for components used
        in building masses
        end note
        e_coli1.csv
    }
    state target_structures {
        index3.json
        note left of index3.json
        Defines the files with target_structure, one per species
        along with description displayed in Website

        NB - These are currently dummy files and internally have the
        same data.
        end note
        b_subtillis.csv
        e_coli2.csv
        e_faecalis.csv
        e_faecium.csv
        s_aureus.csv
    }
    class masses,reference_masses,target_structures data
    class Svelte,MsDataUploader,FragmentDataUploader webui
    class pgfinder processing
```


[card]: https://developer.mozilla.org/en-US/docs/Web/CSS/Layout_cookbook/Card
[div]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/div
[json]: https://www.json.org/json-en.html
[npm]: https://www.npmjs.com/
[pandas]: https://pandas.pydata.org/
[pathlib]: https://docs.python.org/3/library/pathlib.html
[pgfinder]: https://github.com/Mesnage-Org/pgfinder/
[prettier]: https://prettier.io/
[pw]: https://playwright.dev/
[pyodide]: https://pyodide.org/en/stable/
[pypi]: https://pypi.org
[semver]: https://semver.org/
[svelte]: https://svelte.dev/docs/
[ts]: https://www.typescriptlang.org/
[vite]: https://vitejs.dev/
[wa]: https://webassembly.org/
