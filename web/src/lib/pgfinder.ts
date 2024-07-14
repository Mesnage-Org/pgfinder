import type { PyProxy, PythonError } from "pyodide/ffi";
import { loadPyodide, type PyodideInterface } from "pyodide";
import { defaultPGFinderState } from "$lib/constants";

const state: PGFinderState = { ...defaultPGFinderState };
let pyodide: PyodideInterface;

// Maybe someday (once top-level await is even more universal), I should get
// rid of this useless, immediately-called function...
(async () => {
  // NOTE: This version needs to match the version of pyodide installed by npm!
  // These files can also be hosted locally from `/static` if something ever
  // happens to this CDN, but there will be some build-system demons to battle.
  pyodide = await loadPyodide({
    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.1/full/",
  });
  pyodide.registerJsModule("pyio", state);
  await pyodide.loadPackage(["micropip", "sqlite3"]);
  const micropip = pyodide.pyimport("micropip");
  await micropip.install("pgfinder==1.2.0-rc1");
  // If you need to test development version of pgfinder you should build the wheel and copy the resulting .whl to the
  // lib/ directory (adajacent to this file), replace the version below and comment out the above (which loads from
  // PyPI).
  // await micropip.install('./pgfinder-1.2.0rc2.dev39+g75eb8a8.d20240603-py3-none-any.whl');
  await pyodide.runPythonAsync(
    "import pgfinder; from pgfinder.gui.shim import *",
  );

  const version = await pyodide.runPythonAsync("pgfinder.__version__");

  const proxy = await pyodide.runPythonAsync("allowed_modifications()");
  const allowedModifications = proxy.toJs();
  proxy.destroy();

  // Load lib/pgfinder/masses/index.json which details the available mass databases
  const jsonMass = await pyodide.runPythonAsync("mass_library_index()");
  const massLibraries = JSON.parse(jsonMass);

  const msg: PGFReadyMsg = {
    type: "Ready",
    version,
    allowedModifications,
    massLibraries,
  };
  postMessage(msg);
})();

function postResult(proxy: PyProxy) {
  const csvFiles = proxy.toJs();
  proxy.destroy();
  csvFiles.forEach((csv: string, file: string) => {
    const blob = new Blob([csv], { type: "text/csv" });
    const fileparts = file.split(".");
    fileparts[fileparts.length - 1] = "csv";
    const filename = fileparts.join(".");

    const msg: PGFResultMsg = {
      type: "Result",
      filename,
      blob
    };
    postMessage(msg);
  });
}

function postError(error: PythonError) {
  const message = error.message;

  const msg: PGFErrorMsg = {
    type: "Error",
    message
  };
  postMessage(msg);
}

onmessage = async ({ data }) => {
  Object.assign(state, data);
  pyodide.runPythonAsync("run_analysis()").then(postResult).catch(postError);
};
