/* tslint:disable */
/* eslint-disable */
/**
 * @returns {string}
 */
export function version(): string;
/**
 * @param {(Replicate)[]} replicates
 * @returns {string}
 */
export function consolidate(replicates: Replicate[]): string;
/**
 */
export class Peptidoglycan {
  free(): void;
  /**
   * @param {string} structure
   */
  constructor(structure: string);
  /**
   * @returns {number}
   */
  oligomerization_state(): number;
  /**
   * @returns {string}
   */
  monoisotopic_mass(): string;
  /**
   * @returns {string}
   */
  smiles(): string;
  /**
   * @returns {string}
   */
  fragment(): string;
}
/**
 */
export class Replicate {
  free(): void;
  /**
   * @param {number} number
   * @param {string} csv
   */
  constructor(number: number, csv: string);
}

export type InitInput =
  | RequestInfo
  | URL
  | Response
  | BufferSource
  | WebAssembly.Module;

export interface InitOutput {
  readonly memory: WebAssembly.Memory;
  readonly version: (a: number) => void;
  readonly __wbg_peptidoglycan_free: (a: number) => void;
  readonly peptidoglycan_new: (a: number, b: number, c: number) => void;
  readonly peptidoglycan_oligomerization_state: (a: number) => number;
  readonly peptidoglycan_monoisotopic_mass: (a: number, b: number) => void;
  readonly peptidoglycan_smiles: (a: number, b: number) => void;
  readonly peptidoglycan_fragment: (a: number, b: number) => void;
  readonly __wbg_replicate_free: (a: number) => void;
  readonly replicate_new: (a: number, b: number, c: number) => number;
  readonly consolidate: (a: number, b: number, c: number) => void;
  readonly __wbindgen_add_to_stack_pointer: (a: number) => number;
  readonly __wbindgen_export_0: (a: number, b: number, c: number) => void;
  readonly __wbindgen_export_1: (a: number, b: number) => number;
  readonly __wbindgen_export_2: (
    a: number,
    b: number,
    c: number,
    d: number,
  ) => number;
  readonly __wbindgen_export_3: (a: number) => void;
}

export type SyncInitInput = BufferSource | WebAssembly.Module;
/**
 * Instantiates the given `module`, which can either be bytes or
 * a precompiled `WebAssembly.Module`.
 *
 * @param {SyncInitInput} module
 *
 * @returns {InitOutput}
 */
export function initSync(module: SyncInitInput): InitOutput;

/**
 * If `module_or_path` is {RequestInfo} or {URL}, makes a request and
 * for everything else, calls `WebAssembly.instantiate` directly.
 *
 * @param {InitInput | Promise<InitInput>} module_or_path
 *
 * @returns {Promise<InitOutput>}
 */
export default function __wbg_init(
  module_or_path?: InitInput | Promise<InitInput>,
): Promise<InitOutput>;
