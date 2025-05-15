<script lang="ts">
  import { FileUpload } from "@skeletonlabs/skeleton-svelte";

  interface Props {
    structures: File | undefined;
  }

  let { structures = $bindable() }: Props = $props();

  let files: FileList = $state();

  function structuresUploaded() {
    const file = files.item(0);
    if (file) {
      structures = file;
    }
  }
</script>

<div class="flex flex-col items-center space-y-4">
  <FileUpload
    name="structure-list"
    bind:files
    on:change={structuresUploaded}
    accept=".txt"
  >
    {#snippet message()}
      {#if structures === undefined}
        <p><b>Upload a file</b> or drag and drop</p>
      {:else}
        <p>{structures.name}</p>
      {/if}
    {/snippet}
    {#snippet meta()}
      {#if !structures}
        Muropeptide Structures (.txt)
      {/if}
    {/snippet}
  </FileUpload>
</div>
