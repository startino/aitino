/// <reference types="svelte" />
import type { BodyRow } from '../bodyRows.js';
import type { NewTablePropSet, TablePlugin } from '../types/TablePlugin.js';
import { type Writable } from 'svelte/store';
export interface FlattenConfig {
	initialDepth?: number;
}
export interface FlattenState {
	depth: Writable<number>;
}
export interface FlattenColumnOptions<Item> {}
export type FlattenPropSet = NewTablePropSet<{
	'tbody.tr.td': {
		flatten: (depth: number) => void;
		unflatten: () => void;
	};
}>;
export declare const getFlattenedRows: <
	Item,
	Row extends BodyRow<Item, import('../types/TablePlugin.js').AnyPlugins>
>(
	rows: Row[],
	depth: number
) => Row[];
export declare const addFlatten: <Item>({
	initialDepth
}?: FlattenConfig) => TablePlugin<Item, FlattenState, FlattenColumnOptions<Item>, FlattenPropSet>;
