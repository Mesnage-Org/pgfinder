<script lang="ts">
  // Svelte and UI Imports
  import "../app.postcss";
  import {
    AppShell,
    Drawer,
    Modal,
    storePopup,
    initializeStores,
  } from "@skeletonlabs/skeleton";
  import {
    computePosition,
    autoUpdate,
    flip,
    shift,
    offset,
    arrow,
  } from "@floating-ui/dom";

  // Component Imports
  import Footer from "./Footer.svelte";
  import Header from "./Header.svelte";
  import LinksAndDownloads from "./LinksAndDownloads.svelte";
    import Ms1Search from "./MS1 Search/MS1 Search.svelte";

  // Initialize Stores for Drawers and Modals
  initializeStores();

  // Floating UI for Popups
  storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

  // Component state
  // FIXME: Replace this with an object that stores all two / three versions in fields!
  let ms1SearchVersion: string;
</script>

<Modal regionBackdrop="bg-surface-backdrop-token overflow-y-hidden" />

<Drawer>
  <LinksAndDownloads />
</Drawer>

<AppShell>
  <svelte:fragment slot="header">
    <!-- FIXME: Need to handle the different versions!-->
    <Header pgfinderVersion={ms1SearchVersion} />
  </svelte:fragment>

  <div class="h-full flex flex-cols-2 justify-center items-center">
    <Ms1Search bind:version={ms1SearchVersion}/>
  </div>

  <svelte:fragment slot="footer">
    <Footer />
  </svelte:fragment>
</AppShell>
