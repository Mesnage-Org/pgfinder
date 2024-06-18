// Defines a worker function for loading reference masses and target structures and using them in calls to smithereens
//
// In due course the default libraries may be incorporated into smithereens and loadad as part of the WebAssembly
// compiled Rust libraries. For now they are static files under $lib/static/data/{reference_masses,target_structures}

import { defaultSmithereens } from "$lib/constants";
import { onMount } from "svelte";
import init, { Peptidoglycan, pg_to_fragments } from "smithereens";

const smithereens: Smithereens = { ...defaultSmithereens };

(async () => {
  const fraglibrary = await fetch("/data/reference_masses/index.json");
  const fragmentsLibraryIndex: any = JSON.parse(await fraglibrary.text());
  const murolibrary = await fetch("/data/target_structures/index.json");
  const muropeptidesLibraryIndex = JSON.parse(await murolibrary.text());
  console.log(`FragmentsLibraryIndex : `);
  console.log(fragmentsLibraryIndex);
  console.log(`MuropeptidesLibraryIndex : `);
  console.log(muropeptidesLibraryIndex);

  // Initialise wasm and wait for it to finish *before* returning `Ready`
  await init();

  postMessage({
    type: "Ready",
    content: {
      fragmentsLibraryIndex,
      muropeptidesLibraryIndex,
    },
  });
})();

// What type should 'proxy' be?
function postResult(csvString: string, filename: string) {
  const blob = new Blob([csvString as BlobPart], { type: "text/csv" });
  postMessage({
    type: "Result",
    content: {
      filename,
      blob,
    },
  });
}

// What type should 'error' be? Do we need a postError function here?
// function postError(error: string) {
// 	const message = error.message;
// 	postMessage({
// 		type: 'Error',
// 		content: {
// 			message
// 		}
// 	});
// }

onmessage = async ({ data }) => {
  // Load each of the files
  const fragmentsPath = await fetch(
    `/data/reference_masses/${data.fragmentsData["name"]}`,
  );
  const fragLibrary = await fragmentsPath.text();
  console.log(`fragmentsPath`, fragmentsPath);
  console.log(`fragLibrary`, fragLibrary);
  const muropeptidesPath = await fetch(
    `/data/target_structures/${data.muropeptidesData["name"]}`,
  );
  const muroLibrary = await muropeptidesPath.text();
  // Split the muroLibrary into an array so we can iterate over it
  const muroLibraryArray = muroLibrary.split(/\r?\n/);
  console.log(`muropeptidesPath`, muropeptidesPath);
  console.log(`muroLibrary`, muroLibrary);
  console.log(`muroLibraryArray : `, muroLibraryArray);

  // Loop over the array calculating the mass using Peptidoglycan.monoisotopic_mass() and saving to a dictionary
  const muropeptidesMasses = {};
  muroLibraryArray.forEach(function (muropeptide) {
    const muropeptideClean = muropeptide.split(" |")[0];
    if (muropeptideClean != "Structure" && muropeptideClean != "") {
      // Instantiate Smithereens as pg
      const pg = new Peptidoglycan(muropeptide);
      // Calculate mass
      const mass = pg.monoisotopic_mass();
      // Save mass to dictionary
      muropeptidesMasses[muropeptide] = mass;
    }
  });
  console.log(`muropeptidesMasses`, muropeptidesMasses);
  console.log(typeof muropeptidesMasses);

  // Convert to CSV
  function CSV(arrayToConvert) {
    // Convert Object to Array first
    const array = Object.keys(arrayToConvert).map((key) => {
      return { [key]: arrayToConvert[key as keyof typeof arrayToConvert] };
    });
    // Header
    let result = "Structure,mass\n";
    // Add the rows
    array.forEach(function (obj) {
      result += Object.keys(obj) + "," + Object.values(obj) + "\n";
    });
    return result;
  }
  const csvString = CSV(muropeptidesMasses);
  console.log(`csvString :\n`, csvString);
  postResult(csvString, "muropeptide_masses.csv");
};
