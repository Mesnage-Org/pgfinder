declare type VirtFile = { name: string; content: ArrayBuffer };

declare type PGFinderState = {
  msData: Array<VirtFile> | undefined;
  massLibrary: VirtFile | undefined;
  enabledModifications: Array<string>;
  ppmTolerance: number;
  cleanupWindow: number;
  consolidationPpm: number;
};

declare type SmithereensState = {
  muropeptidesLibraryIndex: VirtFile | undefined;
  muropeptidesData: VirtFile | undefined;
};

declare type MassLibraryIndex = {
  [index: string]: {
    [index: string]: {
      File: string;
      Description: string;
    };
  };
};
declare type MassDatabaseTemplates = {
  [index: string]: {
    File: string;
    Description: string;
  };
};

// PGFinder Worker Message Types ===============================================

declare type PGFinderMsg = PGFReadyMsg | PGFResultMsg | PGFErrorMsg;

declare type PGFReadyMsg = {
  type: "Ready";
  version: string;
  allowedModifications: Array<string>;
  massLibraries: MassLibraryIndex;
};

declare type PGFResultMsg = {
  type: "Result";
  filename: string;
  blob: Blob;
};

declare type PGFErrorMsg = {
  type: "Error";
  message: string;
};

// Smithereens Worker Message Types ============================================

declare type SmithereensMsg = SReadyMsg | SSingleMsg;

declare type SReadyMsg = {
  type: "Ready";
  version: string;
  massDatabaseTemplates: MassDatabaseTemplates;
};

declare type SSingleMsg = {
  type: "Single";
  structure: string;
};
