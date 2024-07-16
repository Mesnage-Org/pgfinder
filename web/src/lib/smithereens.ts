// Defines a worker function for loading reference masses and target structures and using them in calls to smithereens
//
// In due course the default libraries may be incorporated into smithereens and loadad as part of the WebAssembly
// compiled Rust libraries. For now they are static files under $lib/static/data/{reference_masses,target_structures}

import init, { Peptidoglycan, version } from "smithereens";

(async () => {
  // Initialise wasm and wait for it to finish *before* returning `Ready`
  await init();

  const msg: SReady = {
    type: "Ready",
    version: version(),
  };
  postMessage(msg);
})();

function csvBlob(csv: string): Blob {
  return new Blob([csv], { type: "text/csv" });
}

function validate({ structure }: SValidateReq): SValidateRes | SSingleErr {
  try {
    if (structure.length != 0) {
      new Peptidoglycan(structure);
    }
    return {
      type: "ValidateRes",
    };
  } catch (msg) {
    // FIXME: I should eventually do something with this error `msg`!
    return {
      type: "SingleErr",
    };
  }
}

function mass({ structure }: SMassReq): SMassRes | SSingleErr {
  try {
    const mass =
      structure.length != 0
        ? new Peptidoglycan(structure).monoisotopic_mass()
        : "";
    return {
      type: "MassRes",
      mass,
    };
  } catch (msg) {
    // FIXME: I should eventually do something with this error `msg`!
    return {
      type: "SingleErr",
    };
  }
}

function fragment({ structure }: SFragmentReq): SFragmentRes | SSingleErr {
  try {
    const fragments = new Peptidoglycan(structure).fragment();
    const filename = `${structure}.csv`;
    const blob = csvBlob(fragments);
    return {
      type: "FragmentRes",
      filename,
      blob,
    };
  } catch (msg) {
    // FIXME: I should eventually do something more with this error `msg`!
    if (msg instanceof WebAssembly.RuntimeError) {
      // FIXME: This appears to be an OOM error when we use more than 4GB of
      // memory (which 32-bit WASM) can't address — properly report this error
      // to users when an input is long enough to trigger this!
      console.error("Yikes mate — ran out of WASM memory...");
    }
    return {
      type: "SingleErr",
    };
  }
}

async function masses({
  structures,
}: SMassesReq): Promise<SMassesRes | SBulkErr> {
  const loadedStructures = await structures.text();

  let csv = "Structure,Monoisotopic Mass\n";
  const structureList = loadedStructures.match(/[^\r\n]+/g) || [];
  for (const [index, structure] of structureList.entries()) {
    try {
      const pg = new Peptidoglycan(structure);
      const oligoState = pg.oligomerization_state();
      const mass = pg.monoisotopic_mass();
      csv += `"${structure}|${oligoState}",${mass}\n`;
    } catch (msg) {
      // FIXME: I should eventually do something with this error `msg`!
      const line = index + 1;
      return {
        type: "BulkErr",
        structure,
        line,
      };
    }
  }

  const fileparts = structures.name.split(".");
  fileparts[fileparts.length - 1] = "csv";
  const filename = fileparts.join(".");
  const blob = csvBlob(csv);

  return {
    type: "MassesRes",
    filename,
    blob,
  };
}

const dispatchTable = {
  MassReq: mass,
  MassesReq: masses,
  ValidateReq: validate,
  FragmentReq: fragment,
};

onmessage = async ({ data: msg }: MessageEvent<SmithereensReq>) => {
  // NOTE: Typescript isn't clever enough to know this is okay yet
  let response: SmithereensRes = await dispatchTable[msg.type](msg as any);
  postMessage(response);
};
