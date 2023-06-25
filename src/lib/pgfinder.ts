import { loadPyodide, type PyodideInterface } from 'pyodide';

let pyodide: PyodideInterface;
// FIXME: This initialisation is duplicated... Make it a class with an initialiser?
const pyio: Pyio = {
	msData: undefined,
	massLibrary: undefined,
	enabledModifications: []
};

// Maybe someday (once top-level await is even more universal), I should get
// rid of this useless, immediately-called function...
(async () => {
	// FIXME: Think about a Vite plugin that bundles the node module!
	// That would mean I don't have to serve things from this indexURL?
	pyodide = await loadPyodide({
		indexURL: '/pyodide'
	});
	pyodide.registerJsModule('pyio', pyio);
	await pyodide.loadPackage(['micropip', 'sqlite3']);
	const micropip = pyodide.pyimport('micropip');
	await micropip.install('/pgfinder-0.0.4.dev30+g8a8f6ef.d20230624-py3-none-any.whl');
	await pyodide.runPythonAsync('from pgfinder import matching, pgio, validation');

	let proxy = await pyodide.runPythonAsync('validation.allowed_modifications()');
	const allowedModifications = proxy.toJs();
	proxy.destroy();

	proxy = await pyodide.runPythonAsync('pgio.mass_libraries()');
	const massLibraries = proxy.toJs();
	proxy.destroy();

	postMessage({
		type: 'Ready',
		content: {
			allowedModifications,
			massLibraries
		}
	});
})();

onmessage = async ({ data }) => {
	Object.assign(pyio, data);
	// FIXME: Move Python code to separately loaded files?
	// FIXME: The subfunction here should be moved to PGFinder!
	const proxy = await pyodide.runPythonAsync(`
from pyio import msData, massLibrary, enabledModifications
theo_masses = pgio.theo_masses_upload_reader(massLibrary.to_py())


def analyze(virt_file):
  ms_data = pgio.ms_upload_reader(virt_file)
  matched = matching.data_analysis(ms_data, theo_masses, 0.5, enabledModifications, 10)
  return pgio.dataframe_to_csv_metadata(matched, wide = True)

{f['name']: analyze(f) for f in msData.to_py()}`);
	const csvFiles = proxy.toJs();
	proxy.destroy();
	csvFiles.forEach((csv: string, file: string) => {
		const blob = new Blob([csv], { type: 'text/csv' });
		const fileparts = file.split('.');
		fileparts[fileparts.length - 1] = 'csv';
		const filename = fileparts.join('.');
		postMessage({
			type: 'Result',
			content: {
				filename,
				blob
			}
		});
	});
};
