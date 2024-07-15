declare type VirtFile = { name: string; content: ArrayBuffer };

declare type PythonState = {
  msData: Array<VirtFile> | undefined;
  massLibrary: VirtFile | undefined;
  enabledModifications: Array<string>;
  ppmTolerance: number;
  cleanupWindow: number;
  consolidationPpm: number;
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

declare type SmithereensReq = SMassReq | SValidateReq | SFragmentReq;

declare type SmithereensRes = SReady
  | SSingleErr
  | SMassRes
  | SValidateRes
  | SFragmentRes;

declare type SReady = {
  type: "Ready";
  version: string;
  massDatabaseTemplates: MassDatabaseTemplates;
};

declare type SMassReq = {
  type: "MassReq";
  structure: string;
};

declare type SMassRes = {
  type: "MassRes";
  mass: string;
};

declare type SSingleErr = {
  type: "SingleErr";
};

declare type SValidateReq = {
  type: "ValidateReq";
  structure: string;
}

declare type SValidateRes = {
  type: "ValidateRes";
}

declare type SFragmentReq = {
  type: "FragmentReq";
  structure: string;
};

declare type SFragmentRes = {
  type: "FragmentRes";
  filename: string;
  blob: Blob;
};
