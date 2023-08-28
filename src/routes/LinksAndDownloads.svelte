<script lang="ts">
	import Fa from 'svelte-fa/src/fa.svelte';
	import { faDownload } from '@fortawesome/free-solid-svg-icons';
</script>

<div class="px-4 py-4">
	<h1 class="h4">Deconvoluted Example Datasets</h1>
	<dl class="list-dl">
		<a href="/pgfinder-gui/data/Ecoli_WT_(Patel et al).ftrs">
			<div class="flex items-stretch hover:variant-soft-surface">
				<div class="badge bg-secondary-500 h-full"><Fa icon={faDownload} size="lg" /></div>
				<span class="flex-auto">
					<dt>Wild-Type <i>Escherichia coli</i></dt>
					<dd class="text-xs">Patel et al. 2021</dd>
				</span>
			</div>
		</a>
	</dl>
</div>
