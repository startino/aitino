/// <reference types="svelte" />
import type { BodyRow } from '../bodyRows.js';
import type { NewTablePropSet, TablePlugin } from '../types/TablePlugin.js';
import { type RecordSetStore } from '../utils/store.js';
import { type Readable, type Writable } from 'svelte/store';
export interface ExpandedRowsConfig<Item> {
	initialExpandedIds?: Record<string, boolean>;
}
export interface ExpandedRowsState<Item> {
	expandedIds: RecordSetStore<string>;
	getRowState: (row: BodyRow<Item>) => ExpandedRowsRowState;
}
export interface ExpandedRowsRowState {
	isExpanded: Writable<boolean>;
	canExpand: Readable<boolean>;
	isAllSubRowsExpanded: Readable<boolean>;
}
export declare const addExpandedRows: <Item>({
	initialExpandedIds
}?: ExpandedRowsConfig<Item>) => TablePlugin<
	Item,
	ExpandedRowsState<Item>,
	Record<string, never>,
	NewTablePropSet<never>
>;
