import type { PyProxy, PythonError } from 'pyodide/ffi';
import { loadPyodide, type PyodideInterface } from 'pyodide';
import { defaultPyio } from '$lib/constants';

const pyio: Pyio = { ...defaultPyio };
let pyodide: PyodideInterface;

// Maybe someday (once top-level await is even more universal), I should get
// rid of this useless, immediately-called function...
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
//	await micropip.install('pgfinder==1.2.0-rc1');
	await micropip.install('/pgfinder-1.2.0rc2.dev36+g456ca69-py3-none-any.whl');
	await pyodide.runPythonAsync('import pgfinder; from pgfinder.gui.shim import *');

	const pgfinderVersion = await pyodide.runPythonAsync('pgfinder.__version__');

	const proxy = await pyodide.runPythonAsync('allowed_modifications()');
	const allowedModifications = proxy.toJs();
	proxy.destroy();

    // Load lib/pgfinder/masses/index.json which details the available mass databases
	const jsonMass = await pyodide.runPythonAsync('mass_library_index()');
	const massLibraries = JSON.parse(jsonMass);

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
