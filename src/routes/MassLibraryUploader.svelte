<script lang="ts">
	import {
		FileDropzone,
		TabGroup,
		Tab,
		ListBox,
		ListBoxItem,
		ProgressRadial
	} from '@skeletonlabs/skeleton';
	export let value: VirtFile | undefined;
	export let massLibraries: Map<string, string> | undefined;

	let files: FileList;
	let customMassLibrary = false;

	async function dataUploaded(): Promise<void> {
		value = { name: files[0].name, content: await files[0].arrayBuffer() };
	}
</script>

<div class="flex flex-col items-center">
	<h5 class="pb-1 h5">Mass Library</h5>
	<TabGroup justify="justify-center">
		<Tab bind:group={customMassLibrary} name="built-in" value={false}>Built-In</Tab>
		<Tab bind:group={customMassLibrary} name="custom" value={true}>Custom</Tab>
		<svelte:fragment slot="panel">
			{#if customMassLibrary}
				<FileDropzone name="mass-library" bind:files on:change={dataUploaded}>
					<svelte:fragment slot="message">
						{#if value === undefined}
							<p><b>Upload a file</b> or drag and drop</p>
						{:else}
							<p>{value.name}</p>
						{/if}
					</svelte:fragment>
				</FileDropzone>
			{:else if massLibraries !== undefined}
				<ListBox>
					{#each [...massLibraries] as [name, content]}
						<ListBoxItem
							bind:group={value}
							name="mass-library"
							value={{ name: name + '.csv', content }}
						>
							{name}
						</ListBoxItem>
					{/each}
				</ListBox>
			{:else}
				<div class="flex justify-center">
					<ProgressRadial />
				</div>
			{/if}
		</svelte:fragment>
	</TabGroup>
</div>
