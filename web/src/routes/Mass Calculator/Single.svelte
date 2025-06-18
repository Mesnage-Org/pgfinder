<script lang="ts">
  import Tooltip from "../Tooltip.svelte";

  export let structure: string;
  export let validStructure: boolean;
  export let mass: string;
  export let smiles: string;

  let value = structure;
  $: structure = value.trim();
  // Assign an error style to the input box if the structure is invalid
  $: color = validStructure ? "" : "text-error-400";
  // Show and hide the warning icon
  $: warning = validStructure ? "hidden" : "";
</script>

<div class="flex flex-col gap-1">
  <label class="label">
    <span>Structure</span>
    <div class="relative {color}">
      <input bind:value class="input" type="text" placeholder="gm-AEJA" />
      <div class="absolute inset-y-0 right-0 pr-3 flex items-center {warning}">
        <Tooltip type="warn">
          The current structure is invalid — please refer to the PGLang
          documentation and examples
        </Tooltip>
      </div>
    </div>
  </label>
  <label class="label">
    <span>Mass</span>
    <div class="flex items-baseline gap-1">
      <input
        value={mass}
        class="input"
        type="text"
        placeholder="941.407702"
        readonly
      />
      <span>Da</span>
    </div>
  </label>
  <label class="label">
    <span>SMILES</span>
    <div class="flex items-baseline gap-1">
      <input
        value={smiles}
        class="input"
        type="text"
        placeholder="O[C@H]([C@H](O1)CO)[C@H](O)[C@@H](NC(=O)C)[C@@H]1%10.O%10[C@H]([C@H](O)CO)[C@H](O[C@H](C)C%20=O)[C@@H](NC(=O)C)CO.N%20[C@@H](C)C%20=O.N%20[C@@H](C(O)=O)CCC%21=O.N%21[C@@H](CCC[C@@H](N)C(O)=O)C%20=O.N%20[C@H](C)C(O)=O"
        readonly
      />
    </div>
  </label>
</div>
