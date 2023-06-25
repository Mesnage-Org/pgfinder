// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
// and what to do when importing types
declare namespace App {
	// interface Locals {}
	// interface PageData {}
	// interface Error {}
	// interface Platform {}
}

declare type VirtFile = { name: string; content: ArrayBuffer };
declare type Pyio = {
	msData: Array<VirtFile>;
	massLibrary: VirtFile | undefined;
};

declare type MsgType = 'Ready' | 'Result';
declare type ReadyMsg = {
	allowedModifications: Array<string>;
	massLibraries: Map<string, string>;
};
declare type ResultMsg = {
	filename: string;
	blob: Blob;
};
declare type Msg = {
	type: MsgType;
	content: ReadyMsg | ResultMsg;
};
