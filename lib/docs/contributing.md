# Contributing

There are a few ways to contribute:

- [Raise an issue](https://github.com/Mesnage-Org/pgfinder/issues) to identify a bug or suggest a new feature.
- Fork the repository and make a pull request to suggest changes to the code.
- If you'd like to contribute a mass database, please do this by [raising an
  issue](https://github.com/Mesnage-Org/pgfinder/issues).

## Repository Structure

Currently, the `pgfinder` repository is split into two major parts: in the `lib` folder is the library (and CLI)
code that forms the heart of PGFinder. The code in this directory is written purely in Python. The other half of this
repository is the `pgfinder-gui` web application — this code lives in the `web` directory. This webapp is written using
[SvelteKit](https://kit.svelte.dev/) and simply wraps PGFinder into a presentable package and passes user inputs to the `pgfinder` Python package
(running in the client's browser via WebAssembly / Pyodide).

As these two halves of the applicaton are written using different languages and frameworks, you'll need different tools
to contribute to each of them.

## Hacking On The `lib` Directory

### Development Installation

The current version when installed from GitHub is a combination of the most recent Git tag combined with the hash of the
current `HEAD` of the branch and how many commits away from the last tag it is.

If you wish to contribute to the development of PGFinder, you should clone (your fork of) this repository, navigate to the
`lib` directory, and install `pgfinder` in editable mode (`pip install -e`) with the following commands (which install
additional dependencies for tests, documentation and linting).

```bash
# Clone the repository
git clone https://github.com/Mesnage-Org/PGFinder.git
cd pgfinder/lib
# Install in editable mode
pip install -e .
# Install extra dependencies
pip install -e ".[dev,docs,tests]"
```

### Testing

To run unit tests suite use [pytest](https://pytest.org)

```bash
# From the `lib` directory...
pytest
```

### Linting (Also Used in `web`)

PGFinder uses [pre-commit](https://pre-commit.com) hooks to ensure code conforms to the [PEP8 Python Style
Guide](https://pep8.org/) using the [ruff](https://duckduckgo.com/?q=ruff+linter&t=opera&ia=images) linter, applies
[black](https://black.readthedocs.io/en/stable/index.html) formatting, and checks for a number of other common mistakes.
These hooks are run on GitHub when Pull Requests are made using [pre-commit.ci](https://pre-commit.ci), and
if you have not run them locally, then your pull request may fail the tests it needs to pass.

`pre-commit` will have been installed as part of the extra dependencies above (they are part of `dev`), but you need to
install `pre-commit` and the hooks locally in your virtual environment. This can be done with the following commands.

``` bash
pre-commit install
pre-commit install-hooks
```

Now when you make a `git commit`, the hooks will run first and report any errors. If the errors can be
corrected automatically, they will be, but you will have to then `git stage` the
modified files again before completing the commit (this gives you an opportunity to review the changes that have been
made, but typically they are ok to accept — they will be `black` formatting or other trivial code-style changes).


### Releasing to PyPI

Releases to the [Python Package Index (PyPI)][pypi] are automated and occur when a new release is made on
GitHub with a tag that begins with `v#.#.#'`. PGFinder uses [semantic verisoning][semver].

## Hacking On the `smitheens` Package

For detailed information on the Smithereens component please refer to the Smithereens section.

## Hacking On The `web` Directory

### Development Installation

To contribute to the PGFinder web interface, we recommend using [`pnpm`](https://pnpm.io/). After navigating to the
`web` directory, it's easy to get a development version of the GUI running using the commands defined in `package.json`.

``` bash
# From the `web` directory...
cd web/
# Install all development dependencies
pnpm install
# Spin up a development version of the GUI
pnpm dev
```

The development server is equipped with hot-reloading, so there is no need to restart it as you make changes. After making
a change and saving the file you were working on, the webpage should reload automatically.

### Testing

To test the GUI's functionality (and that it's correctly interfacing with the `pgfinder` backend), you can run `pnpm test`,
which leverages [Playwright][pw] for end-to-end testing.

``` bash
# Start browser testing in the background
pnpm test
# Start an interactive testing session and open the UI
pnpm test -- --ui
```

### Formatting

To ensure consistent formating throughout the `web` directory, you can run [Prettier][prettier] using the following command:

``` bash
# Run Prettier
pnpm format
```

### Linting

To check for errors or potential improvements to code style, you can run the following commands:

``` bash
# Check for hard-errors (svelte-check)
pnpm check
# Do the same, but automatically recheck when the code is changed
pnpm check:watch
# Check for potential improvements to code style
pnpm lint
```

### Development

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

#### `src/lib`

The `src/lib/` directory contains [TypeScript][ts] files. These are imported automatically via the `$lib` alias as noted
in `index.ts`. Currently PGFinder has three files `constants.ts`, `pgfinder.ts` and `smithereens.ts`

##### `src/lib/constants.ts`

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

##### `src/lib/pgfinder.ts`

This script imports [Pyodide][pyodide], a [WebAssembly][wa] library that allows PGFinder to run in the browser as well
as the constants that are defined in `src/lib/constants.ts`.

``` typescript
import type { PyProxy, PythonError } from 'pyodide/ffi';       // Imports Python modules
import { loadPyodide, type PyodideInterface } from 'pyodide';  // Imports pyodide
import { defaultPyio } from '$lib/constants';                  // Imports src/lib/constants.ts

const pyio: Pyio = { ...defaultPyio };    // Stores constants in pyio
let pyodide: PyodideInterface;            // Aliases PyodideInterface to pyodide
```

##### `src/lib/smithereens`

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


##### A new Card

To define a new card for inclusion you need to

[npm]: https://www.npmjs.com/
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
