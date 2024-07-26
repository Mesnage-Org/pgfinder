<script lang="ts">
  import {
    FileDropzone,
    TabGroup,
    Tab,
    ProgressRadial,
  } from "@skeletonlabs/skeleton";
  import MassDatabaseSelector from "./MassDatabaseSelector.svelte";
  export let value: VirtFile | undefined;
  export let massLibraries: MassLibraryIndex | undefined;

  let files: FileList;
  let customMassLibrary = false;

  async function dataUploaded(): Promise<void> {
    value = { name: files[0].name, content: await files[0].arrayBuffer() };
  }
</script>

<div class="flex flex-col items-center">
  <h5 class="pb-1 h5">Mass Database</h5>
  <TabGroup class="w-full" justify="justify-center">
    <Tab bind:group={customMassLibrary} name="builtInMass" value={false}
      >Built-In</Tab
    >
    <Tab bind:group={customMassLibrary} name="customMassLibrary" value={true}
      >Custom Mass</Tab
    >
    <svelte:fragment slot="panel">
      {#if customMassLibrary}
        <FileDropzone
          name="mass-library"
          bind:files
          on:change={dataUploaded}
          accept=".csv"
        >
          <svelte:fragment slot="message">
            {#if value === undefined}
              <p><b>Upload a file</b> or drag and drop</p>
            {:else}
              <p>{value.name}</p>
            {/if}
          </svelte:fragment>
          <svelte:fragment slot="meta">
            {#if !value}
              PGFinder Mass Library (.csv)
            {/if}
          </svelte:fragment>
        </FileDropzone>
      {:else if massLibraries !== undefined}
        <MassDatabaseSelector bind:value {massLibraries} />
      {:else}
        <div class="flex justify-center">
          <ProgressRadial />
        </div>
      {/if}
    </svelte:fragment>
  </TabGroup>
</div>
