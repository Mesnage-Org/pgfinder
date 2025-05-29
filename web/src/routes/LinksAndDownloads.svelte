<script lang="ts">
  import { base } from "$app/paths";
  import Fa from "svelte-fa";
  import { faDownload } from "@fortawesome/free-solid-svg-icons";
</script>

<div class="mx-4 my-4">
  <h4 class="h4">Deconvoluted Example Datasets</h4>
  <dl class="list-dl">
    <a href="{base}/data/E. coli WT (Patel et al).ftrs">
      <div class="flex items-stretch hover:variant-soft-surface">
        <div class="badge bg-secondary-500 h-full">
          <Fa icon={faDownload} size="lg" />
        </div>
        <span class="flex-auto">
          <dt><i>Escherichia coli</i></dt>
          <dd class="text-xs">Strain BW25113 — Patel et al. 2021</dd>
        </span>
      </div>
    </a>

    <a href="{base}/data/C. difficile WT (Bern et al).ftrs">
      <div class="flex items-stretch hover:variant-soft-surface">
        <div class="badge bg-secondary-500 h-full">
          <Fa icon={faDownload} size="lg" />
        </div>
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
      <a href="https://www.maxquant.org/" class="anchor" target="_blank"
        >Download MaxQuant</a
      >
    </li>
    <li>
      <a
        href="https://proteowizard.sourceforge.io/download.html"
        class="anchor"
        target="_blank"
      >
        Download ProteoWizard (MSConvert)
      </a>
    </li>
    <li>
      <a
        href="https://mesnage-org.github.io/glam/"
        class="anchor"
        target="_blank"
      >
        Glycopeptide Database Builder (GLAM)
      </a>
    </li>
    <!-- <li>How to deconvolute raw data (coming soon!)</li> -->
  </ul>

  <hr class="my-4" />

  <h4 class="h4">Cite Us!</h4>
  <div class="space-y-4">
    <p class="text-xs">
      Alamán-Zárate, M. G. <i>et al.</i> A software tool and strategy for
      peptidoglycomics, the high-resolution analysis of bacterial peptidoglycans
      via LC-MS/MS. <i>Commun Chem</i> <b>8</b>, 1–12 (2025).
      <br />
      <a
        href="https://doi.org/10.1038/s42004-025-01490-6"
        class="anchor"
        target="_blank"
      >
        https://doi.org/10.1038/s42004-025-01490-6
      </a>
    </p>
    <p class="text-xs">
      Patel, A. V. <i>et al.</i> PGFinder, a novel analysis pipeline for the
      consistent, reproducible, and high-resolution structural analysis of
      bacterial peptidoglycans. <i>eLife</i> <b>10</b>, e70597 (2021).
      <br />
      <a
        href="https://doi.org/10.7554/eLife.70597"
        class="anchor"
        target="_blank"
      >
        https://doi.org/10.7554/eLife.70597
      </a>
    </p>
    <p class="text-xs">
      Rady, B. J. &amp; Mesnage, S. PGFinder, an Open-Source Software for
      Peptidoglycomics: The Structural Analysis of Bacterial Peptidoglycan by
      LC-MS. <i>Methods Mol Biol</i> <b>2836</b>, 111–132 (2024).
      <br />
      <a
        href="https://doi.org/10.1007/978-1-0716-4007-4_8"
        class="anchor"
        target="_blank"
      >
        https://doi.org/10.1007/978-1-0716-4007-4_8
      </a>
    </p>
  </div>
</div>
