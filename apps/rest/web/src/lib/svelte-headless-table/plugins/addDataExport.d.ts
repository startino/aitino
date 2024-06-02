/// <reference types="svelte" />
import type { TablePlugin } from '../types/TablePlugin.js';
import { type Readable } from 'svelte/store';
export type DataExportFormat = 'object' | 'json' | 'csv';
type ExportForFormat = {
	object: Record<string, unknown>[];
	json: string;
	csv: string;
};
export type DataExport<F extends DataExportFormat> = ExportForFormat[F];
export interface DataExportConfig<F extends DataExportFormat> {
	childrenKey?: string;
	format?: F;
}
export interface DataExportState<F extends DataExportFormat> {
	exportedData: Readable<DataExport<F>>;
}
export interface DataExportColumnOptions {
	exclude?: boolean;
}
export declare const addDataExport: <Item, F extends DataExportFormat = 'object'>({
	format,
	childrenKey
}?: DataExportConfig<F>) => TablePlugin<Item, DataExportState<F>, DataExportColumnOptions>;
export {};
