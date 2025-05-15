<script lang="ts">
  import Tooltip from "../Tooltip.svelte";

  interface Props {
    structure: string;
    validStructure: boolean;
  }

  let { structure = $bindable(), validStructure }: Props = $props();

  // Assign an error style to the input box if the structure is invalid
  let color = $derived(validStructure ? "" : "text-error-400");
  // Show and hide the warning icon
  let warning = $derived(validStructure ? "hidden" : "");
</script>

<div class="flex flex-col gap-1">
  <label class="label">
    <span>Structure</span>
    <div class="relative {color}">
      <input
        bind:value={structure}
        class="input"
        type="text"
        placeholder="gm-AEJA"
      />
      <div class="absolute inset-y-0 right-0 pr-3 flex items-center {warning}">
        <Tooltip type="warn">
          The current structure is invalid — please refer to the PGLang
          documentation and examples
        </Tooltip>
      </div>
    </div>
  </label>
</div>
