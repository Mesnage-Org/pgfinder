<script lang="ts">
  import {
    FileDropzone,
    TabGroup,
    Tab,
    ProgressRadial,
  } from "@skeletonlabs/skeleton";
  // Need to define these
  import BuiltinFragmentsSelector from "./BuiltinFragmentsSelector.svelte";
  export let value: VirtFile | undefined;
  export let fragmentsLibraryIndex: FragmentsLibraryIndex | undefined;

  let files: FileList;
  let customFragmentsLibrary = false;

  async function dataUploaded(): Promise<void> {
    value = { name: files[0].name, content: await files[0].arrayBuffer() };
  }
  $: console.log(`FragmentsDataUploader value :`, value);
</script>

<div class="flex flex-col items-center" data-testid="fragmentsDataUploader">
  <h5 class="pb-1 h5">Building block components</h5>
  <p>(list of sugars and amino-acids)</p>
  <TabGroup class="w-full" justify="justify-center">
    <Tab bind:group={customFragmentsLibrary} name="built-in" value={false}
      >Built-In</Tab
    >
    <Tab bind:group={customFragmentsLibrary} name="custom" value={true}
      >Custom</Tab
    >
    <svelte:fragment slot="panel">
      {#if customFragmentsLibrary}
        <FileDropzone
          name="fragments-library"
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
              Fragments (.csv)
            {/if}
          </svelte:fragment>
        </FileDropzone>
      {:else if fragmentsLibraryIndex !== undefined}
        <BuiltinFragmentsSelector bind:value {fragmentsLibraryIndex} />
      {:else}
        <div class="flex justify-center">
          <ProgressRadial />
        </div>
      {/if}
    </svelte:fragment>
  </TabGroup>
</div>
