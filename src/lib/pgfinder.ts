import type { PyProxy, PythonError } from 'pyodide/ffi';
import { loadPyodide } from 'pyodide';
import { defaultPyio } from '$lib/constants';

const pyio: Pyio = { ...defaultPyio };
const pyodide = await loadPyodide({
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

function postResult(proxy: PyProxy) {
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
}

function postError(error: PythonError) {
	const message = error.message;
	postMessage({
		type: 'Error',
		content: {
			message
		}
	});
}

onmessage = async ({ data }) => {
	Object.assign(pyio, data);
	pyodide.runPythonAsync('run_analysis()').then(postResult).catch(postError);
};
