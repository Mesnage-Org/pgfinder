// Defines a worker function for loading reference masses and target structures and using them in calls to smithereens
//
// In due course the default libraries may be incorporated into smithereens and loadad as part of the WebAssembly
// compiled Rust libraries. For now they are static files under $lib/static/data/{reference_masses,target_structures}

import { downloadZip } from "client-zip";
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

function mass({ structure }: SMassReq): SMassRes | SSingleErr {
  try {
    const [mass, smiles] =
      structure.length != 0
        ? calculate_mass_and_smiles()
        : ["", ""];
    return {
      type: "MassRes",
      mass,
      smiles,
    };
  } catch {
    // FIXME: I should eventually do something with the error message!
    return {
      type: "SingleErr",
    };
  }

    function calculate_mass_and_smiles(): [string, string] {
        const pg = new Peptidoglycan(structure);
        return [pg.monoisotopic_mass(), pg.smiles()];
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
    } catch {
      // FIXME: I should eventually do something with the error message!
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

function validate({ structure }: SValidateReq): SValidateRes | SSingleErr {
  try {
    if (structure.length != 0) {
      new Peptidoglycan(structure);
    }
    return {
      type: "ValidateRes",
    };
  } catch {
    // FIXME: I should eventually do something with the error message!
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

async function fragments({
  structures,
}: SFragmentsReq): Promise<SFragmentsRes | SBulkErr> {
  const loadedStructures = await structures.text();

  const files: File[] = [];
  const structureList = loadedStructures.match(/[^\r\n]+/g) || [];
  for (const [index, structure] of structureList.entries()) {
    try {
      const fragments = new Peptidoglycan(structure).fragment();
      files.push(new File([csvBlob(fragments)], `${structure}.csv`));
    } catch (msg) {
      // FIXME: I should eventually do something more with this error `msg`!
      if (msg instanceof WebAssembly.RuntimeError) {
        // FIXME: This appears to be an OOM error when we use more than 4GB of
        // memory (which 32-bit WASM) can't address — properly report this error
        // to users when an input is long enough to trigger this!
        console.error("Yikes mate — ran out of WASM memory...");
      }
      const line = index + 1;
      return {
        type: "BulkErr",
        structure,
        line,
      };
    }
  }

  const fileparts = structures.name.split(".");
  fileparts[fileparts.length - 1] = "zip";
  const filename = fileparts.join(".");

  const blob = await downloadZip(files).blob();

  return {
    type: "FragmentsRes",
    filename,
    blob,
  };
}

const dispatchTable = {
  MassReq: mass,
  MassesReq: masses,
  ValidateReq: validate,
  FragmentReq: fragment,
  FragmentsReq: fragments,
};

onmessage = async ({ data: msg }: MessageEvent<SmithereensReq>) => {
  // NOTE: Typescript isn't clever enough to know this is okay yet
  /* eslint-disable  @typescript-eslint/no-explicit-any */
  const response: SmithereensRes = await dispatchTable[msg.type](msg as any);
  postMessage(response);
};
