import type { PyProxy, PythonError } from "pyodide/ffi";
import { loadPyodide, type PyodideInterface } from "pyodide";
import { defaultPythonState } from "$lib/constants";
// NOTE: This is a temporary hack for getting the Rust-based cross-replicate consolidation code in here — in the future
// hopefully we won't need to shuffle between languages this way!
import init, { consolidate, Replicate } from "smithereens";

const state: PythonState = { ...defaultPythonState };
let pyodide: PyodideInterface;

// Maybe someday (once top-level await is even more universal), I should get
// rid of this useless, immediately-called function...
(async () => {
  // NOTE: Initialise the Rust WASM and wait for it to finish *before* returning `Ready`
  await init();

  // NOTE: This version needs to match the version of pyodide installed by npm!
  // These files can also be hosted locally from `/static` if something ever
  // happens to this CDN, but there will be some build-system demons to battle.
  pyodide = await loadPyodide({
    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.27.6/full/",
  });
  pyodide.registerJsModule("pyio", state);
  await pyodide.loadPackage(["micropip", "sqlite3"]);
  const micropip = pyodide.pyimport("micropip");
  await micropip.install("pgfinder==1.4.0");
  // If you need to test development version of pgfinder you should build the wheel and copy the resulting .whl to the
  // lib/ directory (adajacent to this file), replace the version below and comment out the above (which loads from
  // PyPI).
  // await micropip.install("./pgfinder-1.3.3.dev4+g97e51ef-py3-none-any.whl");
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
  const csvFiles = stripExtensions(proxy.toJs());
  proxy.destroy();
  downloadFiles(consolidateReplicates(csvFiles));

  function consolidateReplicates(
    csvFiles: IteratorObject<[string, string]>,
  ): [string, string][] {
    const result = Array.from(csvFiles);

    const fileparts = /(?<basename>.+?)(?:_0*(?<replicate>\d+))?$/;
    const needConsolidation = result
      .map(([filename, c]): [{ [key: string]: string }, string] => [
        filename.match(fileparts)!.groups!,
        c,
      ])
      .filter(([{ replicate }]) => replicate !== undefined);

    const groupedReplicates = Map.groupBy(
      needConsolidation,
      ([{ basename }]) => basename,
    );

    for (const [basename, files] of groupedReplicates) {
      const suffix = files.map(([{ replicate }]) => replicate).join(",");
      const filename = `${basename}_${suffix}`;
      const replicates = Array.from(
        files.map(
          ([{ replicate }, csv]) => new Replicate(Number(replicate), csv),
        ),
      );
      // FIXME: This should be an object / class, not a tuple of filename and data...
      result.push([filename, consolidate(replicates)]);
    }

    return result;
  }

  // FIXME: Need to think a bit more about how this iteracts with `consolidateReplicates`
  function stripExtensions(
    csvMap: Map<string, string>,
  ): IteratorObject<[string, string]> {
    return csvMap
      .entries()
      .map(([f, c]): [string, string] => [
        f.split(".").slice(0, -1).join("."),
        c,
      ]);
  }

  function downloadFiles(csvFiles: [string, string][]) {
    for (const [basename, content] of csvFiles) {
      const blob = new Blob([content], { type: "text/csv" });
      const filename = [basename, "csv"].join(".");

      const msg: PGFResultMsg = {
        type: "Result",
        filename,
        blob,
      };
      postMessage(msg);
    }
  }
}

function postError(error: PythonError) {
  const message = error.message;

  const msg: PGFErrorMsg = {
    type: "Error",
    message,
  };
  postMessage(msg);
}

onmessage = async ({ data }) => {
  Object.assign(state, data);
  pyodide.runPythonAsync("run_analysis()").then(postResult).catch(postError);
};
