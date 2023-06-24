<script lang="ts">
	import { onMount } from 'svelte';
	import MsDataUploader from './MsDataUploader.svelte';
	import MassLibraryUploader from './MassLibraryUploader.svelte';
	import AdvancedOptions from './AdvancedOptions.svelte';
	import type { PyodideInterface } from 'pyodide';
	import fileDownload from 'js-file-download';
	import { debug } from 'svelte/internal';
	let pgfinderReady = false;
	// FIXME: Need to write a proper typescript definitition for this...
	let pyodide: PyodideInterface;
	type Pyio = {
		msData: Array<VirtFile>;
		massLibrary: VirtFile | undefined;
	};
	let pyio: Pyio = {
		msData: [],
		massLibrary: undefined
	};

	let allowedModifications: Array<string>;
	let massLibraries: Map<string, string>;

	async function initPyodide() {
		// Not being able to use Pyodide as a node module is god-awful...
		// eslint-disable-next-line @typescript-eslint/ban-ts-comment
		// @ts-ignore
		pyodide = await loadPyodide();
		pyodide.registerJsModule('pyio', pyio);
		await pyodide.loadPackage('micropip');
		await pyodide.loadPackage('sqlite3');
		const micropip = pyodide.pyimport('micropip');
		await micropip.install('pgfinder-0.0.4.dev30+g8a8f6ef.d20230624-py3-none-any.whl');
		await pyodide.runPythonAsync('from pgfinder import matching, pgio, validation');

		let proxy = await pyodide.runPythonAsync('validation.allowed_modifications()');
		allowedModifications = proxy.toJs();
		proxy.destroy();

		proxy = await pyodide.runPythonAsync('pgio.mass_libraries()');
		massLibraries = proxy.toJs();
		proxy.destroy();
		pgfinderReady = true;
	}
	onMount(initPyodide);

	async function runPython() {
		// FIXME: Move Python code to separately loaded files?
		// FIXME: The subfunction here should be moved to PGFinder!
		const proxy = await pyodide.runPythonAsync(`
from pyio import msData, massLibrary
theo_masses = pgio.theo_masses_upload_reader(massLibrary.to_py())


def analyze(virt_file):
  ms_data = pgio.ms_upload_reader(virt_file)
  matched = matching.data_analysis(ms_data, theo_masses, 0.5, [], 10)
  return pgio.dataframe_to_csv_metadata(matched, wide = True)

{f['name']: analyze(f) for f in msData.to_py()}`);
		const csvFiles = proxy.toJs();
		proxy.destroy();
		console.log(csvFiles);
		csvFiles.forEach((csv: string, file: string) => {
			const blob = new Blob([csv], { type: 'text/csv' });
			let fileparts = file.split('.');
			fileparts[fileparts.length - 1] = 'csv';
			fileDownload(blob, fileparts.join('.'));
		});
	}
</script>

<div class="h-full flex flex-col justify-center items-center">
	<div class="card">
		<section class="flex flex-col space-y-4 justify-center p-4">
			<MsDataUploader bind:value={pyio.msData} />
			<MassLibraryUploader bind:value={pyio.massLibrary} {massLibraries} />
			<AdvancedOptions />
			<button type="button" class="btn variant-filled" on:click={runPython}>Run Analysis</button>
		</section>
	</div>
</div>
