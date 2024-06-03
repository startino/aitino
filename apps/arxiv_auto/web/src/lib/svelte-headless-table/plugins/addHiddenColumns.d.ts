/// <reference types="svelte" />
import type { NewTablePropSet, TablePlugin } from '../types/TablePlugin.js';
import { type Writable } from 'svelte/store';
export interface HiddenColumnsConfig {
	initialHiddenColumnIds?: string[];
}
export interface HiddenColumnsState {
	hiddenColumnIds: Writable<string[]>;
}
export declare const addHiddenColumns: <Item>({
	initialHiddenColumnIds
}?: HiddenColumnsConfig) => TablePlugin<
	Item,
	HiddenColumnsState,
	Record<string, never>,
	NewTablePropSet<never>
>;
