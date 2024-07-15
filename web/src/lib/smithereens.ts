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

  const msg: SmithereensRes = {
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

function validate({ structure }: SValidateReq): SValidateRes | SSingleErr {
  try {
    if (structure.length != 0) {
      new Peptidoglycan(structure);
    }
    return {
      type: "ValidateRes"
    };
  } catch (msg) {
    // FIXME: I should eventually do something with this error `msg`!
    return {
      type: "SingleErr"
    };
  }
}

function mass({ structure }: SMassReq): SMassRes | SSingleErr {
  try {
    const mass = (structure.length != 0) ? new Peptidoglycan(structure).monoisotopic_mass() : "";
    return {
      type: "MassRes",
      mass
    };
  } catch (msg) {
    // FIXME: I should eventually do something with this error `msg`!
    return {
      type: "SingleErr"
    };
  }
}

function fragment({ structure }: SFragmentReq): SFragmentRes | SSingleErr {
  try {
    const fragments = new Peptidoglycan(structure).fragment();
    const filename = `${structure}.csv`;
    const blob = new Blob([fragments], { type: "text/csv" });
    return {
      type: "FragmentRes",
      filename,
      blob
    };
  } catch (msg) {
    // FIXME: I should eventually do something with this error `msg`!
    return {
      type: "SingleErr"
    };
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

const dispatchTable = {
  "MassReq": mass,
  "ValidateReq": validate,
  "FragmentReq": fragment,
};

onmessage = async ({ data: msg }: MessageEvent<SmithereensReq>) => {
  // FIXME: Refactor this to a switch table that just picks a function, but
  // they are all then applied to the message in the same way!
  console.log(msg);
  // NOTE: Typescript isn't clever enough to know this is okay yet
  let response: SmithereensRes = dispatchTable[msg.type](msg as any);
  postMessage(response);
};
