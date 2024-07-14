// Defines a worker function for loading reference masses and target structures and using them in calls to smithereens
//
// In due course the default libraries may be incorporated into smithereens and loadad as part of the WebAssembly
// compiled Rust libraries. For now they are static files under $lib/static/data/{reference_masses,target_structures}

import init, { Peptidoglycan, version } from "smithereens";

(async () => {
  const template_index = await fetch("/data/mass_database_templates/index.json");
  const massDatabaseTemplates = JSON.parse(await template_index.text());

  // Initialise wasm and wait for it to finish *before* returning `Ready`
  await init();

  let msg: SmithereensMsg = {
    type: "Ready",
    version: version(),
    massDatabaseTemplates,
  };

  postMessage(msg);
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

function processSingle(structure: string): string {
  try {
    let mass = new Peptidoglycan(structure).monoisotopic_mass();
    return `Monoisotopic Mass: ${mass} Da`;
  } catch (msg) {
    console.error(msg);
    return "Invalid Structure";
  }
}

// FIXME: Need to write this up properly!
async function processBulk(data: any) {
  // Load each of the files
  const muropeptidesPath = await fetch(
    `/data/target_structures/${data.muropeptidesData["name"]}`,
  );
  const muroLibrary = await muropeptidesPath.text();
  // Split the muroLibrary into an array so we can iterate over it
  const muroLibraryArray = muroLibrary.split(/\r?\n/);

  // Loop over the array calculating the mass using Peptidoglycan.monoisotopic_mass() and saving to a dictionary
  const muropeptidesMasses = new Map();
  muroLibraryArray.forEach(function(muropeptide) {
    const muropeptideClean = muropeptide.split(" |")[0];
    if (muropeptideClean != "Structure" && muropeptideClean != "") {
      // Instantiate Smithereens as pg
      const pg = new Peptidoglycan(muropeptide);
      // Calculate mass
      const mass = pg.monoisotopic_mass();
      // Save mass to dictionary
      muropeptidesMasses.set(muropeptide, mass);
    }
  });

  // Convert to CSV
  function CSV(arrayToConvert: Map<string, string>) {
    // Convert Object to Array first
    const array = Object.keys(arrayToConvert).map((key) => {
      return { [key]: arrayToConvert[key as keyof typeof arrayToConvert] };
    });
    // Header
    let result = "Structure,mass\n";
    // Add the rows
    array.forEach(function(obj) {
      result += Object.keys(obj) + "," + Object.values(obj) + "\n";
    });
    return result;
  }
  const csvString = CSV(muropeptidesMasses);
  postResult(csvString, "muropeptide_masses.csv");
}

onmessage = async ({ data: msg }: MessageEvent<SmithereensMsg>) => {
  switch (msg.type) {
    case "Single":
      console.log(processSingle(msg.structure));
      break;
  }
  console.log(msg);
};
