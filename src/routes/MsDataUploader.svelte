<script lang="ts">
	import { FileDropzone } from '@skeletonlabs/skeleton';
	export let value: Array<VirtFile>;

	let files: FileList;

	async function dataUploaded(): Promise<void> {
		value = await Promise.all(
			[...files].map(async (f: File) => ({ name: f.name, content: await f.arrayBuffer() }))
		);
	}
</script>

<div class="flex flex-col items-center">
	<h5 class="pb-1 h5">MS Datasets</h5>
	<FileDropzone name="ms-data" bind:files on:change={dataUploaded} multiple>
		<svelte:fragment slot="message">
			{#if !value.length}
				<p><b>Upload a file</b> or drag and drop</p>
			{:else}
				<ol class="list">
					{#each value.map((f) => f.name) as file}
						<li>{file}</li>
					{/each}
				</ol>
			{/if}
		</svelte:fragment>
	</FileDropzone>
</div>
