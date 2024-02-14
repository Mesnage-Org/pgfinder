<script lang="ts">
	import { base } from '$app/paths';
	import Fa from 'svelte-fa';
	import { faDownload } from '@fortawesome/free-solid-svg-icons';
</script>

<div class="mx-4 my-4">
	<h4 class="h4">Deconvoluted Example Datasets</h4>
	<dl class="list-dl">
		<a href="{base}/data/E. coli WT (Patel et al).ftrs">
			<div class="flex items-stretch hover:variant-soft-surface">
				<div class="badge bg-secondary-500 h-full"><Fa icon={faDownload} size="lg" /></div>
				<span class="flex-auto">
					<dt><i>Escherichia coli</i></dt>
					<dd class="text-xs">Strain BW25113 — Patel et al. 2021</dd>
				</span>
			</div>
		</a>

		<a href="{base}/data/C. difficile WT (Bern et al).ftrs">
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
			<a
				href="https://github.com/Mesnage-Org/pgfinder/tree/master/lib/pgfinder/masses"
				class="anchor"
				target="_blank"
			>
				Browse Built-In Mass Databases
			</a>
		</li>
		<li>
			<a href="https://www.maxquant.org/" class="anchor" target="_blank">Download MaxQuant</a>
		</li>
		<li>
			<a href="https://proteowizard.sourceforge.io/download.html" class="anchor" target="_blank">
				Download ProteoWizard (MSConvert)
			</a>
		</li>
		<!-- <li>How to deconvolute raw data (coming soon!)</li> -->
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
		<a href="https://doi.org/10.7554/eLife.70597" class="anchor" target="_blank">
			https://doi.org/10.7554/eLife.70597
		</a>
	</p>
</div>
