<script lang="ts">
  import { FileDropzone } from "@skeletonlabs/skeleton";

  export let structures: File | undefined;

  let files: FileList;

  function structuresUploaded() {
    const file = files.item(0);
    if (file) {
      structures = file;
    }
  }
</script>

<div class="flex flex-col items-center space-y-4">
  <FileDropzone
    name="structure-list"
    bind:files
    on:change={structuresUploaded}
    accept=".txt"
  >
    <svelte:fragment slot="message">
      {#if structures === undefined}
        <p><b>Upload a file</b> or drag and drop</p>
      {:else}
        <p>{structures.name}</p>
      {/if}
    </svelte:fragment>
    <svelte:fragment slot="meta">
      {#if !structures}
        Muropeptide Structures (.txt)
      {/if}
    </svelte:fragment>
  </FileDropzone>
</div>
