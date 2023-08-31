<script lang="ts">
	import { Accordion, AccordionItem, popup } from '@skeletonlabs/skeleton';
	import ModificationSelector from './ModificationSelector.svelte';
	export let enabledModifications: Array<string>;
	export let allowedModifications: Array<string> | undefined;
	export let ppmTolerance: number;
	export let cleanupWindow: number;
	export let consolidationPpm: number;
	export let advancedMode: boolean;
</script>

<Accordion class="w-full">
	<AccordionItem bind:open={advancedMode}>
		<svelte:fragment slot="summary">Advanced Options</svelte:fragment>
		<svelte:fragment slot="content">
			<div class="grid md:grid-cols-2 md:gap-8">
				<ModificationSelector bind:value={enabledModifications} {allowedModifications} />
				<div class="flex flex-col justify-between aspect-square overflow-y-auto">
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
						<div
							class="card p-4 variant-filled-secondary max-w-md"
							data-popup="consolidationTooltip"
						>
							<p>
								During consolidation, structures with the lowest absolute ppm are selected over
								those farther from the theoretical mass. However, if two or more matches have a
								theoretical mass less than the consolidation ppm apart, then those matches are
								retained, leaving several possible matches.
							</p>
							<div class="arrow variant-filled-secondary" />
						</div>
					</div>
				</div>
			</div>
		</svelte:fragment>
	</AccordionItem>
</Accordion>
