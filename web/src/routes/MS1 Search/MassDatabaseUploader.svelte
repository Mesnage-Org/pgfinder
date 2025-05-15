<script lang="ts">
  import {
    Tab, FileUpload, Tabs, ProgressRing } from "@skeletonlabs/skeleton-svelte";
  import MassDatabaseSelector from "./MassDatabaseSelector.svelte";
  interface Props {
    value: VirtFile | undefined;
    massLibraries: MassLibraryIndex | undefined;
  }

  let { value = $bindable(), massLibraries }: Props = $props();

  let files: FileList = $state();
  let customMassLibrary = $state(false);

  async function dataUploaded(): Promise<void> {
    value = { name: files[0].name, content: await files[0].arrayBuffer() };
  }
</script>

<div class="flex flex-col items-center">
  <h5 class="pb-1 h5">Mass Database</h5>
  <Tabs class="w-full" justify="justify-center">
    <Tab bind:group={customMassLibrary} name="builtInMass" value={false}
      >Built-In</Tab
    >
    <Tab bind:group={customMassLibrary} name="customMassLibrary" value={true}
      >Custom Mass</Tab
    >
    {#snippet panel()}
      {#if customMassLibrary}
        <FileUpload
          name="mass-library"
          bind:files
          on:change={dataUploaded}
          accept=".csv"
        >
          {#snippet message()}
            {#if value === undefined}
              <p><b>Upload a file</b> or drag and drop</p>
            {:else}
              <p>{value.name}</p>
            {/if}
          {/snippet}
          {#snippet meta()}
            {#if !value}
              PGFinder Mass Library (.csv)
            {/if}
          {/snippet}
        </FileUpload>
      {:else if massLibraries !== undefined}
        <MassDatabaseSelector bind:value {massLibraries} />
      {:else}
        <div class="flex justify-center">
          <ProgressRing />
        </div>
      {/if}
    {/snippet}
  </Tabs>
</div>
