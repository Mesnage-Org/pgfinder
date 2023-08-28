<script lang="ts">
	import Fa from 'svelte-fa/src/fa.svelte';
	import { faDownload } from '@fortawesome/free-solid-svg-icons';
</script>

<div class="mx-4 my-4">
	<h4 class="h4">Deconvoluted Example Datasets</h4>
	<dl class="list-dl">
		<a href="/pgfinder-gui/data/Ecoli_WT(Patel et al).ftrs">
			<div class="flex items-stretch hover:variant-soft-surface">
				<div class="badge bg-secondary-500 h-full"><Fa icon={faDownload} size="lg" /></div>
				<span class="flex-auto">
					<dt><i>Escherichia coli</i></dt>
					<dd class="text-xs">Strain BW25113 — Patel et al. 2021</dd>
				</span>
			</div>
		</a>

		<a href="/pgfinder-gui/data/Cdiff_WT(Bern et al).ftrs">
			<div class="flex items-stretch hover:variant-soft-surface">
				<div class="badge bg-secondary-500 h-full"><Fa icon={faDownload} size="lg" /></div>
				<span class="flex-auto">
					<dt><i>Clostridium difficile</i></dt>
					<dd class="text-xs">Strain R20291 — Bern et al. 2017</dd>
				</span>
			</div>
		</a>
	</dl>

	<hr class="my-4" />

	<h4 class="h4">Useful Links & Software</h4>
	<ul class="list-disc pl-4">
		<li>
			<a href="https://www.maxquant.org/" class="anchor">Download MaxQuant</a>
		</li>
		<li>
			<a href="https://proteowizard.sourceforge.io/download.html" class="anchor">
				Download ProteoWizard (MSConvert)
			</a>
		</li>
		<li>How to deconvolute raw data (coming soon!)</li>
	</ul>

	<hr class="my-4" />

	<h4 class="h4">Cite Us!</h4>
	<p class="text-xs">
		Ankur V Patel, Robert D Turner, Aline Rifflet, Adelina E Acosta-Martin, Andrew Nichols, Milena M
		Awad, Dena Lyras, Ivo Gomperts Boneca, Marshall Bern, Mark O Collins, Stéphane Mesnage (2021)
		<strong>
			PGFinder, a novel analysis pipeline for the consistent, reproducible, and high-resolution
			structural analysis of bacterial peptidoglycans
		</strong>
		<i>eLife</i> <strong>10</strong>:e70597
		<br />
		<a href="https://doi.org/10.7554/eLife.70597" class="anchor">
			https://doi.org/10.7554/eLife.70597
		</a>
	</p>
</div>
