<script lang="ts">
  import { ListBox, ListBoxItem, ProgressRadial } from "@skeletonlabs/skeleton";
  export let value: Array<string>;
  export let allowedModifications: Array<string> | undefined;
</script>

<div class="flex flex-col items-center aspect-square overflow-y-auto">
  <h5 class="pb-1 h5">Modifications</h5>
  {#if allowedModifications !== undefined}
    <ListBox class="w-full overflow-y-auto" multiple>
      {#each [...allowedModifications] as name}
        <ListBoxItem
          bind:group={value}
          name="enabled-modifications"
          value={name}
        >
          {name}
        </ListBoxItem>
      {/each}
    </ListBox>
  {:else}
    <div class="flex h-full items-center">
      <ProgressRadial />
    </div>
  {/if}
</div>
