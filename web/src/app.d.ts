declare type VirtFile = { name: string; content: ArrayBuffer };

declare type Pyio = {
	msData: Array<VirtFile> | undefined;
	massLibrary: VirtFile | undefined;
    fragmentsData: Array<VirtFile> | undefined;
    fragmentsLibrary: VirtFile | undefined;
    muropeptidesData: Array<VirtFile> | undefined;
    muropeptidesLibrary: VirtFile | undefined;
	enabledModifications: Array<string>;
	ppmTolerance: number;
	cleanupWindow: number;
	consolidationPpm: number;
};

declare type MsgType = 'Ready' | 'Result';
declare type MassLibraryIndex = {
	[index: string]: {
		[index: string]: {
			File: string;
			Description: string;
		};
	};
};
declare type FragmentsLibraryIndex = {
	[index: string]: {
		File: string;
		Description: string;
	};
};
declare type MuropeptidesLibraryIndex = {
	[index: string]: {
		File: string;
		Description: string;
	};
};
declare type ReadyMsg = {
	pgfinderVersion: string;
	allowedModifications: Array<string>;
	massLibraries: MassLibraryIndex;
};
declare type ResultMsg = {
	filename: string;
	blob: Blob;
};
declare type ErrorMsg = {
	message: string;
};
declare type Msg = {
	type: MsgType;
	content: ReadyMsg | ResultMsg | ErrorMsg;
};
