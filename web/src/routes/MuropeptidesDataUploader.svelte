<script lang="ts">
  import {
    FileDropzone,
    TabGroup,
    Tab,
    ProgressRadial,
  } from "@skeletonlabs/skeleton";
  // Need to define these
  import BuiltinFragmentsSelector from "./BuiltinFragmentsSelector.svelte";
  import BuiltinMuropeptidesSelector from "./BuiltinMuropeptidesSelector.svelte";
  export let value: VirtFile | undefined;
  export let muropeptidesLibraryIndex: MuropeptidesLibraryIndex | undefined;

  let files: FileList;
  let customMuropeptideLibrary = false;

  async function dataUploaded(): Promise<void> {
    value = { name: files[0].name, content: await files[0].arrayBuffer() };
  }
  $: console.log(`MuropeptidesDataUploader value :`, value);
</script>

<div
  class="flex flex-col items-center"
  data-testid="muropeptides-data-uploader"
>
  <h5 class="pb-1 h5">Muropeptide List</h5>
  <TabGroup class="w-full" justify="justify-center">
    <Tab bind:group={customMuropeptideLibrary} name="built-in" value={false}
      >Built-In</Tab
    >
    <Tab bind:group={customMuropeptideLibrary} name="custom" value={true}
      >Custom</Tab
    >
    <svelte:fragment slot="panel">
      {#if customMuropeptideLibrary}
        <FileDropzone
          name="muropeptide-library"
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
              Muropeptide (.csv)
            {/if}
          </svelte:fragment>
        </FileDropzone>
      {:else if muropeptidesLibraryIndex !== undefined}
        <BuiltinMuropeptidesSelector bind:value {muropeptidesLibraryIndex} />
      {:else}
        <div class="flex justify-center">
          <ProgressRadial />
        </div>
      {/if}
    </svelte:fragment>
  </TabGroup>
</div>
