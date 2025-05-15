<script lang="ts">
  // Svelte and UI Imports
  import "../app.postcss";
  import {
    computePosition,
    autoUpdate,
    flip,
    shift,
    offset,
    arrow,
  } from "@floating-ui/dom";
  import { defaultVersions } from "$lib/constants";

  // Component Imports
  import Footer from "./Footer.svelte";
  import Header from "./Header.svelte";
  import LinksAndDownloads from "./LinksAndDownloads.svelte";
  import Ms1Search from "./MS1 Search/MS1 Search.svelte";
  import MassCalculator from "./Mass Calculator/Mass Calculator.svelte";
  import FragmentGenerator from "./Fragment Generator/Fragment Generator.svelte";

  // Initialize Stores for Drawers and Modals
  initializeStores();

  // Floating UI for Popups
  storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

  // Component state
  let versions: Versions = $state({ ...defaultVersions });
</script>

<Modal regionBackdrop="bg-surface-50/50 dark:bg-surface-950/50 overflow-y-hidden" />

<Drawer>
  <LinksAndDownloads />
</Drawer>

<AppShell>
  {#snippet header()}
    <Header {versions} />
  {/snippet}

  <div
    class="h-full flex flex-col gap-4 lg:flex-row justify-center items-center"
  >
    <div></div>
    <MassCalculator bind:version={versions.Smithereens} />
    <Ms1Search bind:version={versions.PGFinder} />
    <!-- NOTE: Version is currently tied to that of the `MassCalculator`-->
    <FragmentGenerator />
    <div></div>
  </div>

  {#snippet footer()}
    <Footer />
  {/snippet}
</AppShell>
