import { loadPyodide, type PyodideInterface } from 'pyodide';
import { defaultPyio } from '$lib/constants';

let pyodide: PyodideInterface;
const pyio: Pyio = { ...defaultPyio };

// Maybe someday (once top-level await is even more universal), I should get
// rid of this useless, immediately-called function...
(async () => {
	// TODO: Think about a Vite plugin that bundles the node module!
	// That would mean I don't have to serve things from this indexURL?
	pyodide = await loadPyodide({
		indexURL: '/pgfinder-gui/pyodide'
	});
	pyodide.registerJsModule('pyio', pyio);
	await pyodide.loadPackage(['micropip', 'sqlite3']);
	const micropip = pyodide.pyimport('micropip');
	await micropip.install('pgfinder');
	await pyodide.runPythonAsync('import pgfinder; from pgfinder.gui.shim import *');

	const pgfinderVersion = await pyodide.runPythonAsync('pgfinder.__version__');

	const proxy = await pyodide.runPythonAsync('allowed_modifications()');
	const allowedModifications = proxy.toJs();
	proxy.destroy();

	const json = await pyodide.runPythonAsync('mass_library_index()');
	const massLibraries = JSON.parse(json);

	postMessage({
		type: 'Ready',
		content: {
			pgfinderVersion,
			allowedModifications,
			massLibraries
		}
	});
})();

onmessage = async ({ data }) => {
	Object.assign(pyio, data);
	const proxy = await pyodide.runPythonAsync('run_analysis()');
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
