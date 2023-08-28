<script lang="ts">
	import { FileDropzone, popup } from '@skeletonlabs/skeleton';
	import Fa from 'svelte-fa/src/fa.svelte';
	import { faCircleInfo } from '@fortawesome/free-solid-svg-icons';
	export let value: Array<VirtFile> | undefined;

	let files: FileList;

	async function dataUploaded(): Promise<void> {
		value = await Promise.all(
			[...files].map(async (f: File) => ({ name: f.name, content: await f.arrayBuffer() }))
		);
	}
</script>

<div class="flex flex-col items-center">
	<h5 class="pb-1 h5">
		Deconvoluted Datasets
		<div
			class="inline ml-1 [&>*]:pointer-events-none"
			use:popup={{
				event: 'hover',
				target: `supported-versions`,
				placement: 'top'
			}}
		>
			<Fa icon={faCircleInfo} class="inline" />
		</div>
	</h5>

	<FileDropzone
		class="max-h-48 overflow-auto"
		name="ms-data"
		bind:files
		on:change={dataUploaded}
		accept=".ftrs, .txt"
		multiple
	>
		<svelte:fragment slot="message">
			{#if !value}
				<p><b>Upload a file</b> or drag and drop</p>
			{:else}
				<ol class="list">
					{#each value.map((f) => f.name) as file}
						<li>{file}</li>
					{/each}
				</ol>
			{/if}
		</svelte:fragment>
		<svelte:fragment slot="meta">
			{#if !value}
				Byos (.ftrs) or MaxQuant (.txt)
			{/if}
		</svelte:fragment>
	</FileDropzone>

	<!-- I need to abstract these popups and their settings into a couple of my own components... -->
	<div class="card p-4 variant-filled-secondary max-w-md" data-popup="supported-versions">
		<p class="text-center">
			This version has been tested with .ftrs files from Byos v3.11, v5.1, and v5.2, as well as
			allPeptides.txt files from Maxquant v2.0.1.0 through v2.4.2.0
		</p>
		<div class="arrow variant-filled-secondary" />
	</div>
</div>
