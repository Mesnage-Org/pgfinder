<script lang="ts">
	import { Accordion, AccordionItem, popup, type PopupSettings } from '@skeletonlabs/skeleton';
	import ModificationSelector from './ModificationSelector.svelte';
	export let enabledModifications: Array<string>;
	export let allowedModifications: Array<string> | undefined;
	export let ppmTolerance: number;
	export let cleanupWindow: number;

	function tooltip(target: string): PopupSettings {
		return { event: 'hover', target, placement: 'top' };
	}
	const cleanupTooltip: PopupSettings = tooltip('cleanupTooltip');
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
					use:popup={cleanupTooltip}
					class="input"
					type="number"
					step="0.1"
					min="0"
				/>
				<div class="card p-4 variant-filled-secondary" data-popup="cleanupTooltip">
					<p>Set time window for in-source decay and salt adduct cleanup</p>
					<div class="arrow variant-filled-secondary" />
				</div>
			</div>
		</svelte:fragment>
	</AccordionItem>
</Accordion>
