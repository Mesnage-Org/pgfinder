<script lang="ts">
	import { Accordion, AccordionItem, popup } from '@skeletonlabs/skeleton';
	import ModificationSelector from './ModificationSelector.svelte';
	export let enabledModifications: Array<string>;
	export let allowedModifications: Array<string> | undefined;
	export let ppmTolerance: number;
	export let cleanupWindow: number;
	export let consolidationPpm: number;
</script>

<Accordion class="w-full">
	<AccordionItem>
		<svelte:fragment slot="summary">Advanced Options</svelte:fragment>
		<svelte:fragment slot="content">
			<ModificationSelector bind:value={enabledModifications} {allowedModifications} />
			<div class="flex flex-col items-center">
				<h5 class="pb-1 h5">PPM Tolerance</h5>
				<input bind:value={ppmTolerance} class="input" type="number" step="1" min="0" />
			</div>

			<div class="flex flex-col items-center">
				<h5 class="pb-1 h5">Cleanup Window</h5>
				<input
					bind:value={cleanupWindow}
					use:popup={{ event: 'hover', target: 'cleanupTooltip', placement: 'top' }}
					class="input"
					type="number"
					step="0.1"
					min="0"
				/>
				<div class="card p-4 variant-filled-secondary max-w-md" data-popup="cleanupTooltip">
					<p>Set time window for in-source decay and salt adduct cleanup</p>
					<div class="arrow variant-filled-secondary" />
				</div>
			</div>

			<div class="flex flex-col items-center">
				<h5 class="pb-1 h5">Consolidation PPM</h5>
				<input
					bind:value={consolidationPpm}
					use:popup={{ event: 'hover', target: 'consolidationTooltip', placement: 'top' }}
					class="input"
					type="number"
					step="1"
					min="0"
					max={ppmTolerance}
				/>
				<div class="card p-4 variant-filled-secondary max-w-md" data-popup="consolidationTooltip">
					<p>
						During consolidation, structures with the lowest absolute ppm are selected over those
						farther from the theoretical mass — if two or more matches are nearly equidistant from
						the theoretical mass, less than the Consolidation PPM apart, then both matches are
						retained
					</p>
					<div class="arrow variant-filled-secondary" />
				</div>
			</div>
		</svelte:fragment>
	</AccordionItem>
</Accordion>
