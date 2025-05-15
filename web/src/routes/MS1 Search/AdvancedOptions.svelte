<script lang="ts">
  import { Accordion } from "@skeletonlabs/skeleton-svelte";
  import ModificationSelector from "./ModificationSelector.svelte";
  import Tooltip from "../Tooltip.svelte";
  interface Props {
    enabledModifications: Array<string>;
    allowedModifications: Array<string> | undefined;
    ppmTolerance: number;
    cleanupWindow: number;
    consolidationPpm: number;
    advancedMode: boolean;
  }

  let {
    enabledModifications = $bindable(),
    allowedModifications,
    ppmTolerance = $bindable(),
    cleanupWindow = $bindable(),
    consolidationPpm = $bindable(),
    advancedMode = $bindable(),
  }: Props = $props();
</script>

<Accordion class="w-full">
  <Accordion.Item bind:open={advancedMode}>
    {#snippet summary()}
      Advanced Options
    {/snippet}
    {#snippet content()}
      <div class="grid md:grid-cols-2 md:gap-8">
        <ModificationSelector
          bind:value={enabledModifications}
          {allowedModifications}
        />
        <div
          class="flex flex-col justify-between aspect-square overflow-y-auto"
        >
          <div class="flex flex-col items-center">
            <h5 class="pb-1 h5">PPM Tolerance</h5>
            <input
              bind:value={ppmTolerance}
              class="input"
              type="number"
              step="1"
              min="0"
            />
          </div>

          <div class="flex flex-col items-center">
            <h5 class="pb-1 h5">
              Cleanup Window
              <Tooltip style="inline ml-1" type="info">
                Set time window for in-source decay and salt adduct cleanup
              </Tooltip>
            </h5>
            <input
              bind:value={cleanupWindow}
              class="input"
              type="number"
              step="0.1"
              min="0"
            />
          </div>

          <div class="flex flex-col items-center">
            <h5 class="pb-1 h5">
              Consolidation PPM
              <Tooltip style="inline ml-1" type="info">
                During consolidation, structures with the lowest absolute ppm
                are selected over those farther from the theoretical mass.
                However, if two or more matches have a theoretical mass less
                than the consolidation ppm apart, then those matches are
                retained, leaving several possible matches.
              </Tooltip>
            </h5>
            <input
              bind:value={consolidationPpm}
              class="input"
              type="number"
              step="1"
              min="0"
              max={ppmTolerance}
            />
          </div>
        </div>
      </div>
    {/snippet}
  </Accordion.Item>
</Accordion>
